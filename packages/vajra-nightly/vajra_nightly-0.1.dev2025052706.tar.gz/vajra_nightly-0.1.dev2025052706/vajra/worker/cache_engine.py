"""CacheEngine class for managing the KV cache."""

from typing import List

import torch

from vajra.config import LlmReplicaControllerConfig, ModelConfig, ParallelConfig
from vajra.logger import init_logger
from vajra.model_executor.layers.attention import AttentionWrapper  # type: ignore

logger = init_logger(__name__)


class CacheEngine:
    """Manages the KV cache.

    This class is responsible for initializing and managing the GPU KV cache.
    """

    def __init__(
        self,
        config: LlmReplicaControllerConfig,
        num_gpu_blocks: int,
    ) -> None:
        self.head_size = config.model_config.get_head_size()
        self.num_layers = config.model_config.get_num_layers(config.parallel_config)
        self.num_heads = config.model_config.get_num_kv_heads(config.parallel_config)

        self.block_size: int = config.cache_config.block_size
        self.num_gpu_blocks: int = num_gpu_blocks

        # Initialize the cache.
        self.gpu_cache = self.allocate_gpu_cache()

    def allocate_gpu_cache(self) -> List[torch.Tensor]:
        gpu_cache: List[torch.Tensor] = []

        for _ in range(self.num_layers):
            gpu_blocks = AttentionWrapper.get_cache_block(self.num_gpu_blocks)
            gpu_cache.append(gpu_blocks)
        return gpu_cache

    @staticmethod
    def get_cache_block_size(
        block_size: int,
        model_config: ModelConfig,
        parallel_config: ParallelConfig,
    ) -> int:
        head_size = model_config.get_head_size()
        num_heads = model_config.get_num_kv_heads(parallel_config)
        num_layers = model_config.get_num_layers(parallel_config)

        key_cache_block = block_size * num_heads * head_size
        value_cache_block = key_cache_block
        total = num_layers * (key_cache_block + value_cache_block)
        dtype_size = _get_dtype_size(model_config.torch_dtype)
        return dtype_size * total


def _get_dtype_size(dtype: torch.dtype) -> int:
    return torch.tensor([], dtype=dtype).element_size()
