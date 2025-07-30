from dataclasses import field

from vajra._native.configs import (
    LlmReplicaControllerConfig as LlmReplicaControllerConfig_C,
)
from vajra.config.base_poly_config import BasePolyConfig
from vajra.config.cache_config import CacheConfig
from vajra.config.model_config import ModelConfig
from vajra.config.parallel_config import ParallelConfig
from vajra.config.replica_scheduler_config import (
    BaseReplicaSchedulerConfig,
    FixedChunkReplicaSchedulerConfig,
)
from vajra.config.worker_config import WorkerConfig
from vajra.enums import ReplicaControllerType
from vajra.utils.dataclasses import frozen_dataclass


@frozen_dataclass
class BaseReplicaControllerConfig(BasePolyConfig):
    """Base configuration for an LLM replica controller."""

    model_config: ModelConfig = field(default_factory=ModelConfig)
    worker_config: WorkerConfig = field(default_factory=WorkerConfig)
    cache_config: CacheConfig = field(default_factory=CacheConfig)
    parallel_config: ParallelConfig = field(default_factory=ParallelConfig)
    scheduler_config: BaseReplicaSchedulerConfig = field(
        default_factory=FixedChunkReplicaSchedulerConfig
    )

    @property
    def native_handle(self):
        return self._native_handle  # type: ignore


@frozen_dataclass
class LlmReplicaControllerConfig(BaseReplicaControllerConfig):
    """Configuration for an LLM replica controller."""

    @staticmethod
    def get_type() -> ReplicaControllerType:
        return ReplicaControllerType.LLM_BASE

    def __post_init__(self):
        self.model_config.verify_with_parallel_config(self.parallel_config)
        self._native_handle = LlmReplicaControllerConfig_C(
            self.model_config.native_handle,
            self.worker_config.native_handle,
            self.cache_config.native_handle,
            self.parallel_config.native_handle,
            self.scheduler_config.native_handle,
        )
