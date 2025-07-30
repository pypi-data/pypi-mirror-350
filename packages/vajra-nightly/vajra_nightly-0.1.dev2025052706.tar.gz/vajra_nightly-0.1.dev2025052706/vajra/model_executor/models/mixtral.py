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
"""Inference-only Mixtral model compatible with HuggingFace weights.

The input of the model is flattened to a 1D tensor of tokens.
"""
from typing import Any, Dict, List, Optional

import torch.distributed
from torch import nn
from transformers.models.mixtral.configuration_mixtral import MixtralConfig

from vajra.config import LlmReplicaControllerConfig
from vajra.logger import init_logger
from vajra.metrics_store import CudaTimer, MetricType
from vajra.model_executor.layers.attention import AttentionWrapper
from vajra.model_executor.layers.ep_moe.layer import EPMoE
from vajra.model_executor.layers.fused_moe.layer import FusedMoE
from vajra.model_executor.layers.layernorm import RMSNorm
from vajra.model_executor.layers.rotary_embedding import get_rope
from vajra.model_executor.models.base_model import BaseModel
from vajra.model_executor.parallel_utils import (
    ColumnParallelLinear,
    ReplicatedLinear,
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

logger = init_logger(__name__)


class MixtralMoE(nn.Module):
    """A tensor-parallel MoE implementation for Mixtral that shards each expert
    across all ranks.

    Each expert's weights are sharded across all ranks and a fused MoE
    kernel is used for the forward pass, and finally we reduce the outputs
    across ranks.
    """

    def __init__(
        self,
        num_experts: int,
        top_k: int,
        hidden_size: int,
        intermediate_size: int,
        layer_id: int,
        enable_expert_parallel: bool = True,
    ) -> None:
        super().__init__()
        self.hidden_size = hidden_size

        # Gate always runs at half / full precision for now.
        self.gate = ReplicatedLinear(
            hidden_size, num_experts, bias=False, layer_id=layer_id
        )

        MOELayer = EPMoE if enable_expert_parallel else FusedMoE
        self.experts = MOELayer(
            num_experts=num_experts,
            top_k=top_k,
            hidden_size=hidden_size,
            intermediate_size=intermediate_size,
            reduce_results=True,
            renormalize=True,
            layer_id=layer_id,
        )

    def forward(self, hidden_states: torch.Tensor) -> torch.Tensor:
        # NOTE: hidden_states can have either 1D or 2D shape.
        orig_shape = hidden_states.shape
        hidden_states = hidden_states.view(-1, self.hidden_size)
        # router_logits: (num_tokens, n_experts)
        router_logits = self.gate(hidden_states)
        final_hidden_states = self.experts(hidden_states, router_logits)
        return final_hidden_states.view(orig_shape)


class MixtralAttention(nn.Module):

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


class MixtralDecoderLayer(nn.Module):

    def __init__(
        self,
        config: MixtralConfig,
        layer_id: int,
        use_native_execution_backend: bool,
        enable_expert_parallel: bool,
    ) -> None:
        super().__init__()
        self.layer_id = layer_id
        self.hidden_size = config.hidden_size
        self.use_native_execution_backend = use_native_execution_backend
        # Requires transformers > 4.32.0
        rope_theta = getattr(config, "rope_theta", 10000)
        rope_scaling = getattr(config, "rope_scaling", None)
        max_position_embeddings = getattr(config, "max_position_embeddings", 8192)
        self.self_attn = MixtralAttention(
            hidden_size=self.hidden_size,
            num_heads=config.num_attention_heads,
            num_kv_heads=config.num_key_value_heads,
            layer_id=layer_id,
            use_native_execution_backend=use_native_execution_backend,
            rope_theta=rope_theta,
            rope_scaling=rope_scaling,
            max_position_embeddings=max_position_embeddings,
        )
        self.block_sparse_moe = MixtralMoE(
            num_experts=config.num_local_experts,
            top_k=config.num_experts_per_tok,
            hidden_size=config.hidden_size,
            intermediate_size=config.intermediate_size,
            layer_id=layer_id,
            enable_expert_parallel=enable_expert_parallel,
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

        hidden_states = self.block_sparse_moe(hidden_states)
        hidden_states = residual + hidden_states

        return hidden_states


class MixtralModel(nn.Module):

    def __init__(
        self,
        config: MixtralConfig,
        use_native_execution_backend: bool,
        enable_expert_parallel: bool,
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
                MixtralDecoderLayer(
                    config,
                    layer_id=layer_id + layer_offset,
                    use_native_execution_backend=use_native_execution_backend,
                    enable_expert_parallel=enable_expert_parallel,
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

    @use_native_backend
    def forward(
        self,
        hidden_states: torch.Tensor,
        positions: torch.Tensor,
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


class MixtralForCausalLM(BaseModel):

    def __init__(self, replica_controller_config: LlmReplicaControllerConfig) -> None:
        super().__init__(replica_controller_config)

        assert isinstance(self.config, MixtralConfig)

        self.model = MixtralModel(
            self.config,
            use_native_execution_backend=self._use_native_execution_backend,
            enable_expert_parallel=self.enable_expert_parallel,
        )

        vocab_size = ((self.config.vocab_size + 63) // 64) * 64

        if is_pipeline_last_stage():
            self.lm_head = ColumnParallelLinear(
                self.config.hidden_size,
                vocab_size,
                bias=False,
                gather_output=True,
            )

    def is_native_execution_backend_supported(self) -> bool:
        return False

    @use_native_backend
    def forward(
        self,
        hidden_states: torch.Tensor,
        positions: torch.Tensor,
        kv_caches: List[torch.Tensor],
    ) -> torch.Tensor:
        hidden_states = self.model(hidden_states, positions, kv_caches)
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

        MOELayer = EPMoE if self.enable_expert_parallel else FusedMoE
        expert_params_mapping = MOELayer.make_expert_params_mapping(
            ckpt_gate_proj_name="w1",
            ckpt_down_proj_name="w2",
            ckpt_up_proj_name="w3",
            num_experts=self.config.num_local_experts,
        )
        loader.load_weights_from_path(
            model_name_or_path,
            cache_dir,
            load_format,
            revision,
            expert_params_mapping=expert_params_mapping,
        )
