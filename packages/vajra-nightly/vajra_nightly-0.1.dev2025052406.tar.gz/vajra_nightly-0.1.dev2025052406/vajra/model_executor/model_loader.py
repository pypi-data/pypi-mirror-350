"""Utilities for selecting and loading models."""

import contextlib
from typing import Type

import torch
from transformers.configuration_utils import PretrainedConfig

from vajra.config import LlmReplicaControllerConfig, ModelConfig
from vajra.model_executor.models import *  # pylint: disable=wildcard-import
from vajra.model_executor.models.base_model import BaseModel
from vajra.model_executor.weight_utils import initialize_dummy_weights

# TODO(woosuk): Lazy-load the model classes.
_MODEL_REGISTRY = {
    "LlamaForCausalLM": LlamaForCausalLM,
    "LLaMAForCausalLM": LlamaForCausalLM,
    "InternLMForCausalLM": LlamaForCausalLM,
    "MistralForCausalLM": LlamaForCausalLM,
    "MixtralForCausalLM": MixtralForCausalLM,
}


@contextlib.contextmanager
def _set_default_torch_dtype(dtype: torch.dtype):
    """Sets the default torch dtype to the given dtype."""
    old_dtype = torch.get_default_dtype()
    torch.set_default_dtype(dtype)
    yield
    torch.set_default_dtype(old_dtype)


def _get_model_architecture(config: PretrainedConfig) -> Type[BaseModel]:
    architectures = getattr(config, "architectures", [])
    for arch in architectures:
        if arch in _MODEL_REGISTRY:
            return _MODEL_REGISTRY[arch]
    raise ValueError(
        f"Model architectures {architectures} are not supported for now. "
        f"Supported architectures: {list(_MODEL_REGISTRY.keys())}"
    )


def get_model(replica_controller_config: LlmReplicaControllerConfig) -> BaseModel:
    model_config: ModelConfig = replica_controller_config.model_config
    model_class = _get_model_architecture(model_config.hf_config)

    with _set_default_torch_dtype(model_config.torch_dtype):
        # Create a model instance.
        # The weights will be initialized as empty tensors.
        with torch.device("cuda"):
            model = model_class(replica_controller_config=replica_controller_config)
        if model_config.load_format == "dummy":
            # NOTE(woosuk): For accurate performance evaluation, we assign
            # random values to the weights.
            initialize_dummy_weights(model)
        else:
            # Load the weights from the cached or downloaded files.
            model.load_weights(  # type: ignore
                model_config.model,
                model_config.download_dir,
                model_config.load_format,
                model_config.revision,
            )
    model.eval()
    return model
