# coding=utf-8
# Adapted from
# https://github.com/huggingface/transformers/blob/v4.28.0/src/transformers/models/llama/modeling_llama.py
# Copyright 2023 The Vajra team.
# Copyright 2022 EleutherAI and the HuggingFace Inc. team. All rights reserved.
#
# This code is based on EleutherAI's GPT-NeoX library and the GPT-NeoX
# and OPT implementations in this library. It has been modified from its
# original forms to accommodate minor architectural differences compared
# to GPT-NeoX and OPT used by the Meta AI team that trained the model.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Inference-only LLaMA model compatible with HuggingFace weights.

The input of the model is flattened to a 1D tensor of tokens.
"""
from typing import Any, Dict, List, Optional

import torch.distributed
from torch import nn
from transformers.models.llama import LlamaConfig

from vajra._native.model_executor.models.llama import LlamaAttention as LlamaAttentionC
from vajra._native.model_executor.models.llama import (
    LlamaDecoderLayer as LlamaDecoderLayerC,
)
from vajra._native.model_executor.models.llama import LlamaMLP as LlamaMLPC
from vajra._native.model_executor.models.llama import LlamaModel as LlamaModelC
from vajra.config import LlmReplicaControllerConfig
from vajra.metrics_store import CudaTimer, MetricType
from vajra.model_executor.layers.activation import SiluAndMul
from vajra.model_executor.layers.attention import AttentionWrapper
from vajra.model_executor.layers.layernorm import RMSNorm
from vajra.model_executor.layers.rotary_embedding import get_rope
from vajra.model_executor.models.base_model import BaseModel
from vajra.model_executor.parallel_utils import (
    ColumnParallelLinear,
    RowParallelLinear,
    VocabParallelEmbedding,
)
from vajra.model_executor.parallel_utils.parallel_state import (
    get_pipeline_model_parallel_rank,
    get_pipeline_model_parallel_world_size,
    get_tensor_model_parallel_world_size,
    is_pipeline_first_stage,
    is_pipeline_last_stage,
)
from vajra.model_executor.utils import use_native_backend
from vajra.model_executor.weight_loader import (
    TransformerAutoWeightsLoader,
)


class LlamaMLP(nn.Module):

    def __init__(
        self,
        hidden_size: int,
        intermediate_size: int,
        hidden_act: str,
        layer_id: int,
        use_native_execution_backend: bool,
    ) -> None:
        super().__init__()

        self.use_native_execution_backend = use_native_execution_backend

        self.gate_up_proj = ColumnParallelLinear(
            hidden_size,
            2 * intermediate_size,
            bias=False,
            gather_output=False,
            linear_op_metric=MetricType.MLP_UP_PROJ,
            communication_op_metric=MetricType.MLP_UP_PROJ_ALL_GATHER,
            layer_id=layer_id,
            use_native_execution_backend=use_native_execution_backend,
        )
        self.down_proj = RowParallelLinear(
            intermediate_size,
            hidden_size,
            bias=False,
            input_is_parallel=True,
            linear_op_metric=MetricType.MLP_DOWN_PROJ,
            communication_op_metric=MetricType.MLP_DOWN_PROJ_ALL_REDUCE,
            layer_id=layer_id,
            use_native_execution_backend=use_native_execution_backend,
        )
        if hidden_act != "silu":
            raise ValueError(
                f"Unsupported activation: {hidden_act}. "
                "Only silu is supported for now."
            )
        self.act_fn = SiluAndMul()

        self._mlp_activation_timer = CudaTimer(
            MetricType.MLP_ACTIVATION, layer_id=layer_id
        )

        if use_native_execution_backend:
            self.native_handle = LlamaMLPC(
                layer_id,
                self.gate_up_proj.native_handle,
                self.down_proj.native_handle,
            )

    @use_native_backend
    def forward(self, x):
        gate_up = self.gate_up_proj(x)
        with self._mlp_activation_timer:
            x = self.act_fn(gate_up)
        x = self.down_proj(x)
        return x


class LlamaAttention(nn.Module):

    def __init__(
        self,
        hidden_size: int,
        num_heads: int,
        num_kv_heads: int,
        layer_id: int,
        use_native_execution_backend: bool,
        rope_theta: float = 10000,
        rope_scaling: Optional[Dict[str, Any]] = None,
        max_position_embeddings: int = 8192,
    ) -> None:
        super().__init__()

        self.hidden_size = hidden_size
        tp_size = get_tensor_model_parallel_world_size()
        self.total_num_heads = num_heads
        assert self.total_num_heads % tp_size == 0
        self.num_heads = self.total_num_heads // tp_size
        self.total_num_kv_heads = num_kv_heads
        assert self.total_num_kv_heads % tp_size == 0
        self.num_kv_heads = self.total_num_kv_heads // tp_size
        self.head_dim = hidden_size // self.total_num_heads
        self.q_size = self.num_heads * self.head_dim
        self.kv_size = self.num_kv_heads * self.head_dim
        self.scaling = self.head_dim**-0.5
        self.rope_theta = rope_theta
        self.max_position_embeddings = max_position_embeddings
        self.layer_id = layer_id
        self.use_native_execution_backend = use_native_execution_backend

        self.qkv_proj = ColumnParallelLinear(
            hidden_size,
            (self.total_num_heads + 2 * self.total_num_kv_heads) * self.head_dim,
            bias=False,
            gather_output=False,
            linear_op_metric=MetricType.ATTN_PRE_PROJ,
            communication_op_metric=MetricType.ATTN_PRE_PROJ_ALL_GATHER,
            layer_id=layer_id,
            use_native_execution_backend=use_native_execution_backend,
        )
        self.o_proj = RowParallelLinear(
            self.total_num_heads * self.head_dim,
            hidden_size,
            bias=False,
            input_is_parallel=True,
            linear_op_metric=MetricType.ATTN_POST_PROJ,
            communication_op_metric=MetricType.ATTN_POST_PROJ_ALL_REDUCE,
            layer_id=layer_id,
            use_native_execution_backend=use_native_execution_backend,
        )
        self.rotary_emb = get_rope(
            head_size=self.head_dim,
            rotary_dim=self.head_dim,
            max_position=self.max_position_embeddings,
            base=int(self.rope_theta),
            is_neox_style=True,
            rope_scaling=rope_scaling,
            use_native_execution_backend=use_native_execution_backend,
        )
        self._attn_rope_timer = CudaTimer(
            MetricType.ATTN_ROPE,
            layer_id=layer_id,
        )

        if use_native_execution_backend:
            # TODO(Amey): Remove type ignore once the native handle is added
            self.native_handle = LlamaAttentionC(
                self.q_size,
                self.kv_size,
                self.scaling,
                layer_id,
                self.qkv_proj.native_handle,
                self.o_proj.native_handle,
                self.rotary_emb.native_handle,
            )

    @use_native_backend
    def forward(
        self,
        positions: torch.Tensor,
        hidden_states: torch.Tensor,
        kv_cache: torch.Tensor,
    ) -> torch.Tensor:
        qkv = self.qkv_proj(hidden_states)

        q, k, v = qkv.split([self.q_size, self.kv_size, self.kv_size], dim=-1)
        with self._attn_rope_timer:
            q, k = self.rotary_emb(positions, q, k)

        attn_output = AttentionWrapper.get_or_create_thread_local_instance().forward(
            q,
            k,
            v,
            kv_cache,
            self.layer_id,
        )

        output = self.o_proj(attn_output)
        return output


class LlamaDecoderLayer(nn.Module):

    def __init__(
        self,
        config: LlamaConfig,
        layer_id: int,
        use_native_execution_backend: bool,
    ) -> None:
        super().__init__()
        self.layer_id = layer_id
        self.hidden_size = config.hidden_size
        self.use_native_execution_backend = use_native_execution_backend
        # Requires transformers > 4.32.0
        rope_theta = getattr(config, "rope_theta", 10000)
        rope_scaling = getattr(config, "rope_scaling", None)
        max_position_embeddings = getattr(config, "max_position_embeddings", 8192)
        self.self_attn = LlamaAttention(
            hidden_size=self.hidden_size,
            num_heads=config.num_attention_heads,
            num_kv_heads=config.num_key_value_heads,
            layer_id=layer_id,
            use_native_execution_backend=use_native_execution_backend,
            rope_theta=rope_theta,
            rope_scaling=rope_scaling,
            max_position_embeddings=max_position_embeddings,
        )
        self.mlp = LlamaMLP(
            hidden_size=self.hidden_size,
            intermediate_size=config.intermediate_size,
            hidden_act=config.hidden_act,
            layer_id=layer_id,
            use_native_execution_backend=use_native_execution_backend,
        )
        self.input_layernorm = RMSNorm(
            config.hidden_size,
            eps=config.rms_norm_eps,
            norm_op_name=MetricType.INPUT_LAYERNORM,
            layer_id=layer_id,
            use_native_execution_backend=use_native_execution_backend,
        )
        self.post_attention_layernorm = RMSNorm(
            config.hidden_size,
            eps=config.rms_norm_eps,
            norm_op_name=MetricType.POST_ATTENTION_LAYERNORM,
            layer_id=layer_id,
            use_native_execution_backend=use_native_execution_backend,
        )

        if use_native_execution_backend:
            self.native_handle = LlamaDecoderLayerC(
                layer_id,
                self.self_attn.native_handle,
                self.mlp.native_handle,
                self.input_layernorm.native_handle,
                self.post_attention_layernorm.native_handle,
            )

    @use_native_backend
    def forward(
        self,
        positions: torch.Tensor,
        hidden_states: torch.Tensor,
        kv_cache: torch.Tensor,
    ) -> torch.Tensor:
        # Self Attention
        residual = hidden_states
        hidden_states = self.input_layernorm(hidden_states)
        hidden_states = self.self_attn(
            positions=positions,
            hidden_states=hidden_states,
            kv_cache=kv_cache,
        )
        hidden_states = residual + hidden_states

        # Fully Connected
        residual = hidden_states

        hidden_states = self.post_attention_layernorm(hidden_states)

        hidden_states = self.mlp(hidden_states)
        hidden_states = residual + hidden_states

        return hidden_states


class LlamaModel(nn.Module):

    def __init__(
        self,
        config: LlamaConfig,
        use_native_execution_backend: bool,
    ) -> None:
        super().__init__()
        self.config = config
        self.padding_idx = config.pad_token_id
        self.vocab_size = config.vocab_size
        self.use_native_execution_backend = use_native_execution_backend

        self.embed_tokens = None
        if is_pipeline_first_stage():
            vocab_size = ((config.vocab_size + 63) // 64) * 64
            self.embed_tokens = VocabParallelEmbedding(
                vocab_size,
                config.hidden_size,
                linear_op_metric=MetricType.EMBED_LINEAR,
                communication_op_metric=MetricType.EMBED_ALL_REDUCE,
                use_native_execution_backend=use_native_execution_backend,
            )

        num_layers = (
            config.num_hidden_layers // get_pipeline_model_parallel_world_size()
        )
        layer_offset = get_pipeline_model_parallel_rank() * num_layers
        self.layers = nn.ModuleList(
            [
                LlamaDecoderLayer(
                    config,
                    layer_id=layer_id + layer_offset,
                    use_native_execution_backend=use_native_execution_backend,
                )
                for layer_id in range(num_layers)
            ]
        )

        self.norm = None
        if is_pipeline_last_stage():
            self.norm = RMSNorm(
                config.hidden_size,
                eps=config.rms_norm_eps,
                use_native_execution_backend=use_native_execution_backend,
            )

        if use_native_execution_backend:
            self.native_handle = LlamaModelC(
                self.embed_tokens.native_handle if self.embed_tokens else None,
                [layer.native_handle for layer in self.layers],
                self.norm.native_handle if self.norm else None,
            )

    @use_native_backend
    def forward(
        self,
        positions: torch.Tensor,
        hidden_states: torch.Tensor,
        kv_caches: List[torch.Tensor],
    ) -> torch.Tensor:
        if self.embed_tokens:
            hidden_states = self.embed_tokens(hidden_states)

        for i in range(len(self.layers)):
            layer = self.layers[i]
            hidden_states = layer(
                positions,
                hidden_states,
                kv_caches[i],
            )

        if self.norm:
            hidden_states = self.norm(hidden_states)

        return hidden_states


class LlamaForCausalLM(BaseModel):

    def __init__(
        self,
        replica_controller_config: LlmReplicaControllerConfig,
    ) -> None:
        super().__init__(replica_controller_config)
        assert isinstance(self.config, LlamaConfig)

        self.model = LlamaModel(
            self.config, use_native_execution_backend=self._use_native_execution_backend
        )

        vocab_size = ((self.config.vocab_size + 63) // 64) * 64

        if is_pipeline_last_stage():
            self.lm_head = ColumnParallelLinear(
                self.config.hidden_size,
                vocab_size,
                bias=False,
                gather_output=True,
            )

        if self._use_native_execution_backend:
            assert self.model.native_handle is not None
            self.native_handle = self.model.native_handle

    def is_native_execution_backend_supported(self) -> bool:
        return True

    @property
    def use_native_execution_backend(self) -> bool:
        return self._use_native_execution_backend

    @use_native_backend
    def forward(
        self,
        positions: torch.Tensor,
        hidden_states: torch.Tensor,
        kv_caches: List[torch.Tensor],
    ) -> torch.Tensor:
        hidden_states = self.model(positions, hidden_states, kv_caches)
        return hidden_states

    def load_weights(
        self,
        model_name_or_path: str,
        cache_dir: Optional[str] = None,
        load_format: str = "auto",
        revision: Optional[str] = None,
    ):
        _column_parallel_layers: List[str] = []
        _row_parallel_layers = ["o_proj", "down_proj"]
        loader = TransformerAutoWeightsLoader(
            self,
            _column_parallel_layers,
            _row_parallel_layers,
            skip_prefixes=[],
        )
        loader.load_weights_from_path(
            model_name_or_path,
            cache_dir,
            load_format,
            revision,
        )
