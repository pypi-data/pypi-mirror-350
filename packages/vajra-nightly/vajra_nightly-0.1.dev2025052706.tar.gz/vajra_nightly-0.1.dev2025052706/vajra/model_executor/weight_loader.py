"""Utility classes for loading model weights."""

import glob
import json
import os
from typing import Any, Iterator, List, Optional, Tuple

import filelock
import numpy as np
import torch
from huggingface_hub import snapshot_download
from safetensors import safe_open
from tqdm.auto import tqdm

from vajra.logger import init_logger
from vajra.model_executor.models.base_model import BaseModel
from vajra.model_executor.parallel_utils.parallel_state import (
    get_pipeline_model_parallel_rank,
    get_pipeline_model_parallel_world_size,
    get_tensor_model_parallel_rank,
    get_tensor_model_parallel_world_size,
)
from vajra.model_executor.weight_utils import (
    convert_pyslice_to_tensor,
)

logger = init_logger(__name__)


class _Disabledtqdm(tqdm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, disable=True)


def _get_lock(model_name_or_path: str, cache_dir: Optional[str] = None):
    lock_dir = cache_dir if cache_dir is not None else "/tmp"
    lock_file_name = model_name_or_path.replace("/", "-") + ".lock"
    lock = filelock.FileLock(os.path.join(lock_dir, lock_file_name))
    return lock


def _prepare_hf_model_weights(
    model_name_or_path: str,
    cache_dir: Optional[str] = None,
    use_safetensors: bool = False,
    fall_back_to_pt: bool = True,
    revision: Optional[str] = None,
) -> Tuple[str, List[str], bool]:
    # Download model weights from huggingface.
    is_local = os.path.isdir(model_name_or_path)
    if use_safetensors:
        allow_patterns = ["*.safetensors"]
    else:
        # Some quantized models use .pt files for storing the weights.
        allow_patterns = ["*.bin", "*.pt"]
    if not is_local:
        # Use file lock to prevent multiple processes from
        # downloading the same model weights at the same time.
        with _get_lock(model_name_or_path, cache_dir):
            hf_folder = snapshot_download(
                model_name_or_path,
                allow_patterns=allow_patterns,
                cache_dir=cache_dir,
                tqdm_class=_Disabledtqdm,  # type: ignore
                revision=revision,
            )
    else:
        hf_folder = model_name_or_path
    hf_weights_files: List[str] = []
    for pattern in allow_patterns:
        hf_weights_files += glob.glob(os.path.join(hf_folder, pattern))
    if not use_safetensors:
        hf_weights_files = [
            x for x in hf_weights_files if not x.endswith("training_args.bin")
        ]

    if len(hf_weights_files) == 0 and use_safetensors and fall_back_to_pt:
        return _prepare_hf_model_weights(
            model_name_or_path,
            cache_dir=cache_dir,
            use_safetensors=False,
            fall_back_to_pt=False,
            revision=revision,
        )

    if len(hf_weights_files) == 0:
        raise RuntimeError(f"Cannot find any model weights with `{model_name_or_path}`")

    return hf_folder, hf_weights_files, use_safetensors


def _hf_model_weights_iterator(
    model_name_or_path: str,
    cache_dir: Optional[str] = None,
    load_format: str = "auto",
    revision: Optional[str] = None,
) -> Iterator[Tuple[str, torch.Tensor]]:
    use_safetensors = False
    use_np_cache = False
    fall_back_to_pt = False
    if load_format == "auto":
        use_safetensors = True
        fall_back_to_pt = True
    elif load_format == "safetensors":
        use_safetensors = True
    elif load_format == "pt":
        pass
    elif load_format == "npcache":
        use_np_cache = True
    else:
        raise ValueError(f"Unknown load_format: {load_format}")

    hf_folder, hf_weights_files, use_safetensors = _prepare_hf_model_weights(
        model_name_or_path,
        cache_dir=cache_dir,
        use_safetensors=use_safetensors,
        fall_back_to_pt=fall_back_to_pt,
        revision=revision,
    )

    if use_np_cache:
        # Currently np_cache only support *.bin checkpoints
        assert use_safetensors is False

        # Convert the model weights from torch tensors to numpy arrays for
        # faster loading.
        np_folder = os.path.join(hf_folder, "np")
        os.makedirs(np_folder, exist_ok=True)
        weight_names_file = os.path.join(np_folder, "weight_names.json")
        # Use file lock to prevent multiple processes from
        # dumping the same model weights to numpy at the same time.
        with _get_lock(model_name_or_path, cache_dir):
            if not os.path.exists(weight_names_file):
                weight_names = []
                for bin_file in hf_weights_files:
                    state = torch.load(bin_file, map_location="cpu")
                    for name, param in state.items():
                        param_path = os.path.join(np_folder, name)
                        with open(param_path, "wb") as f:
                            np.save(f, param.cpu().detach().numpy())
                        weight_names.append(name)
                with open(weight_names_file, "w") as f:
                    json.dump(weight_names, f)

        with open(weight_names_file, "r") as f:
            weight_names = json.load(f)

        for name in weight_names:
            param_path = os.path.join(np_folder, name)
            with open(param_path, "rb") as f:
                param = np.load(f)
            yield name, torch.from_numpy(param)
    elif use_safetensors:
        for st_file in hf_weights_files:
            with safe_open(st_file, framework="pt") as f:
                for name in f.keys():
                    param = f.get_slice(name)
                    yield name, param
    else:
        for bin_file in hf_weights_files:
            state = torch.load(bin_file, map_location="cpu")
            for name, param in state.items():
                yield name, param
            del state
            torch.cuda.empty_cache()


def _load_padded_tensor_parallel_vocab(
    param: torch.Tensor,
    loaded_weight: Any,  # `torch.Tensor` or `PySafeSlice`
    tensor_model_parallel_rank: int,
) -> None:
    shard_size = param.shape[0]
    start_idx = tensor_model_parallel_rank * shard_size
    end_idx = (tensor_model_parallel_rank + 1) * shard_size
    loaded_weight = loaded_weight[start_idx:end_idx]
    loaded_weight = convert_pyslice_to_tensor(loaded_weight)
    param[: loaded_weight.shape[0]].copy_(loaded_weight)


def _default_weight_loader(
    param: torch.Tensor, loaded_weight: torch.Tensor, *args, **kwargs
) -> None:
    """Default weight loader."""
    if param.numel() == 1 and loaded_weight.numel() == 1:
        # Sometimes scalar values aren't considered tensors with shapes
        # so if both param and loaded_weight are a scalar,
        # "broadcast" instead of copy
        param.data.fill_(loaded_weight.item())
    else:
        loaded_weight = convert_pyslice_to_tensor(loaded_weight)
        assert param.size() == loaded_weight.size(), (
            f"Attempted to load weight ({loaded_weight.size()}) "
            f"into parameter ({param.size()})"
        )

        param.data.copy_(loaded_weight)


class TransformerAutoWeightsLoader:
    def __init__(
        self,
        module: BaseModel,
        column_parallel_layers=None,
        row_parallel_layers=None,
        skip_prefixes: Optional[List[str]] = None,
    ):
        self.config = module.config
        self.state_dict = module.state_dict()
        self.named_parameters = dict(module.named_parameters())
        self._column_parallel_layers = column_parallel_layers or []
        self._row_parallel_layers = row_parallel_layers or []
        self.skip_prefixes = skip_prefixes

    def load_weights_from_path(
        self,
        model_name_or_path: str,
        cache_dir: Optional[str] = None,
        load_format: str = "auto",
        revision: Optional[str] = None,
        expert_params_mapping=None,
    ):
        """
        Load weights from a model path or name with tensor parallelism
        and pipeline parallelism support.

        Args:
            model_name_or_path: Local path or model name from HuggingFace hub
            cache_dir: Directory to cache downloaded models
            load_format: Format to load weights in ("auto", "safetensors", "pytorch")
            revision: Git revision to use when loading from hub
        """
        self.load_weights(
            _hf_model_weights_iterator(
                model_name_or_path,
                cache_dir,
                load_format,
                revision,
            ),
            get_tensor_model_parallel_rank(),
            get_tensor_model_parallel_world_size(),
            get_pipeline_model_parallel_rank(),
            get_pipeline_model_parallel_world_size(),
            expert_params_mapping=expert_params_mapping,
        )

    def load_weights(
        self,
        weights: Iterator[Tuple[str, torch.Tensor]],
        tp_rank,
        tp_size,
        pp_rank,
        pp_size,
        layers_per_stage=None,
        expert_params_mapping=None,
    ):
        """
        Load weights from an iterator of (name, tensor) pairs with tensor parallelism
        and pipeline parallelism support.

        Args:
            weights: Iterator of (name, tensor) pairs
            attention_weight_specs: List of (weight_name, shard_size, offset) tuples
            tp_rank: Tensor parallel rank (defaults to current rank)
            pp_rank: Pipeline parallel rank (defaults to current rank)
            pp_size: Pipeline parallel size (defaults to current world size)
            layers_per_stage: Number of layers per pipeline stage (calculated from config if None)
        """
        if layers_per_stage is None and self.config is not None:
            assert self.config.num_hidden_layers % pp_size == 0
            layers_per_stage = self.config.num_hidden_layers // pp_size

        first_layer_id = layers_per_stage * pp_rank
        last_layer_id = layers_per_stage * (pp_rank + 1) - 1

        # Define weight patterns for parallel loading
        weight_suffixes = ["weight"]
        column_parallel_weights = []
        for layer in self._column_parallel_layers:
            for suffix in weight_suffixes:
                column_parallel_weights.append(f"{layer}.{suffix}")

        row_parallel_weights = []
        for layer in self._row_parallel_layers:
            for suffix in weight_suffixes:
                row_parallel_weights.append(f"{layer}.{suffix}")

        # Load weights
        self._load_weights_internal(
            weights,
            tp_rank,
            tp_size,
            pp_rank,
            pp_size,
            first_layer_id,
            last_layer_id,
            column_parallel_weights,
            row_parallel_weights,
            expert_params_mapping=expert_params_mapping,
        )

    def _load_weights_internal(
        self,
        weights,
        tp_rank,
        tp_size,
        pp_rank,
        pp_size,
        first_layer_id,
        last_layer_id,
        column_parallel_weights,
        row_parallel_weights,
        expert_params_mapping=None,
    ):
        """Internal implementation of weight loading logic"""
        for name, loaded_weight in weights:
            if self.skip_prefixes and any(
                name.startswith(prefix) for prefix in self.skip_prefixes
            ):
                continue
            if self._should_skip_weight(name, pp_rank, pp_size):
                continue

            if "model.layers" in name:
                layer_id = int(name.split(".")[2])
                if layer_id < first_layer_id or layer_id > last_layer_id:
                    continue

                new_layer_id = layer_id - first_layer_id
                name = name.replace(str(layer_id), str(new_layer_id))

            if self._handle_moe_weights(
                name,
                loaded_weight,
                tp_size,
                tp_rank,
                expert_params_mapping,
            ):
                continue

            if self._handle_attention_weights(
                name,
                loaded_weight,
                tp_size,
                tp_rank,
            ):
                continue

            # Handle MLP gate/up weights
            if self._handle_gate_up_weights(
                name, loaded_weight, self.state_dict, tp_rank
            ):
                continue

            # Handle all other weights
            param = self.named_parameters[name]

            weight_loader_method = getattr(
                param, "weight_loader", _default_weight_loader
            )

            if self._handle_embed_and_lm_head_weights(
                name, param, loaded_weight, tp_rank
            ):
                continue

            if self._handle_row_parallel_weights(
                param,
                name,
                loaded_weight,
                row_parallel_weights,
                tp_rank,
                weight_loader_method,
            ):
                continue

            if self._handle_column_parallel_weights(
                param,
                name,
                loaded_weight,
                column_parallel_weights,
                tp_rank,
                weight_loader_method,
            ):
                continue

            weight_loader_method(param, loaded_weight)

    def _should_skip_weight(
        self,
        name,
        pp_rank,
        pp_size,
    ) -> bool:
        if "rotary_emb.inv_freq" in name:
            return True

        if pp_rank != 0 and "embed_tokens" in name:
            return True

        if pp_rank != pp_size - 1 and (
            "lm_head" in name or name == "model.norm.weight"
        ):
            return True

        return False

    def _handle_moe_weights(
        self, name, loaded_weight, tp_size, tp_rank, expert_params_mapping
    ):
        if expert_params_mapping is None:
            return False
        for mapping in expert_params_mapping:
            param_name, weight_name, expert_id, shard_id = mapping
            if weight_name not in name:
                continue
            name = name.replace(weight_name, param_name)
            if (
                name.endswith(".bias") or name.endswith("_bias")
            ) and name not in self.named_parameters:
                continue
            param = self.named_parameters[name]
            weight_loader = getattr(param, "weight_loader")
            weight_loader(
                param, loaded_weight, name, shard_id=shard_id, expert_id=expert_id
            )
            return True
        return False

    # TODO
    def _handle_embed_and_lm_head_weights(self, name, param, loaded_weight, tp_rank):
        if "embed_tokens" in name or "lm_head" in name:
            _load_padded_tensor_parallel_vocab(param, loaded_weight, tp_rank)
            return True
        return False

    def _handle_attention_weights(
        self,
        name,
        loaded_weight,
        tp_size,
        tp_rank,
    ) -> bool:
        """Handle attention-specific weight loading"""
        q_proj_shard_size = self.config.hidden_size // tp_size
        kv_proj_shard_size = (
            self.config.hidden_size
            // self.config.num_attention_heads
            * self.config.num_key_value_heads
            // tp_size
        )
        attention_weight_specs = [
            # (weight_name, shard_size, offset)
            ("q_proj", q_proj_shard_size, 0),
            ("k_proj", kv_proj_shard_size, q_proj_shard_size),
            ("v_proj", kv_proj_shard_size, q_proj_shard_size + kv_proj_shard_size),
        ]
        for weight_name, shard_size, offset in attention_weight_specs:
            if weight_name not in name:
                continue
            param = self.named_parameters[name.replace(weight_name, "qkv_proj")]
            weight_loader_method = getattr(
                param, "weight_loader", _default_weight_loader
            )
            weight_loader_method(
                param,
                name,
                loaded_weight,
                tp_rank,
                shard_size=shard_size,
                param_slice_offset=offset,
            )
            return True
        return False

    # TODO
    def _handle_gate_up_weights(self, name, loaded_weight, state_dict, tp_rank):
        """Handle MLP gate/up weight loading"""
        for stride_id, weight_name in enumerate(["gate_proj", "up_proj"]):
            if weight_name not in name:
                continue
            param = state_dict[name.replace(weight_name, "gate_up_proj")]

            shard_size = param.shape[0] // 2
            loaded_weight = loaded_weight[
                shard_size * tp_rank : shard_size * (tp_rank + 1)
            ]
            param_slice = param.data[
                shard_size * stride_id : shard_size * (stride_id + 1)
            ]
            assert param_slice.shape == loaded_weight.shape
            param_slice.copy_(loaded_weight)
            return True
        return False

    def _handle_row_parallel_weights(
        self,
        param,
        param_name,
        loaded_weight,
        row_parallel_weight_names,
        tp_rank,
        weight_loader_method,
    ):
        for p in row_parallel_weight_names:
            if p in param_name:
                weight_loader_method(param, param_name, loaded_weight, tp_rank)
                return True
        return False

    def _handle_column_parallel_weights(
        self,
        param,
        param_name,
        loaded_weight,
        column_parallel_weight_names,
        tp_rank,
        weight_loader_method,
    ):
        for p in column_parallel_weight_names:
            if p in param_name:
                weight_loader_method(param, param_name, loaded_weight, tp_rank)
                return True
        return False
