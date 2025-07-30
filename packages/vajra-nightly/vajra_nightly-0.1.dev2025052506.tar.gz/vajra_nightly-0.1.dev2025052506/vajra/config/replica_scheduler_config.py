from dataclasses import field

from vajra._native.configs import (
    DynamicChunkReplicaSchedulerConfig as DynamicChunkReplicaSchedulerConfig_C,
)
from vajra._native.configs import (
    FixedChunkReplicaSchedulerConfig as FixedChunkReplicaSchedulerConfig_C,
)
from vajra._native.configs import (
    SpaceSharingReplicaSchedulerConfig as SpaceSharingReplicaSchedulerConfig_C,
)
from vajra.config.base_poly_config import BasePolyConfig
from vajra.enums import ReplicaSchedulerType
from vajra.utils.dataclasses import frozen_dataclass


@frozen_dataclass
class BaseReplicaSchedulerConfig(BasePolyConfig):
    max_batch_size: int = field(
        default=128,
        metadata={
            "help": "Maximum number of sequences to be processed in a single iteration (batch size)."
        },
    )

    @property
    def native_handle(self):
        return self._native_handle  # type: ignore

    @property
    def max_chunk_size(self) -> int:
        raise NotImplementedError

    @property
    def min_chunk_size(self) -> int:
        raise NotImplementedError

    @property
    def target_batch_time(self) -> float:
        raise NotImplementedError


@frozen_dataclass
class FixedChunkReplicaSchedulerConfig(BaseReplicaSchedulerConfig):
    chunk_size: int = field(
        default=2048,
        metadata={"help": "Chunk size for fixed chunk size scheduler."},
    )

    @property
    def max_chunk_size(self) -> int:
        return self.chunk_size

    @property
    def min_chunk_size(self) -> int:
        return self.chunk_size

    @property
    def target_batch_time(self) -> float:
        return 0  # not applicable to fixed chunk size scheduler

    @staticmethod
    def get_type() -> ReplicaSchedulerType:
        return ReplicaSchedulerType.FIXED_CHUNK

    def __post_init__(self):
        self._native_handle = FixedChunkReplicaSchedulerConfig_C(
            self.max_batch_size,
            self.chunk_size,
        )


@frozen_dataclass
class DynamicChunkReplicaSchedulerConfig(BaseReplicaSchedulerConfig):
    max_chunk_size_param: int = field(
        default=8192,
        metadata={"help": "Maximum chunk size."},
    )
    min_chunk_size_param: int = field(
        default=32,
        metadata={"help": "Minimum chunk size."},
    )
    target_batch_time_param: float = field(
        default=0.05,
        metadata={"help": "Target batch time for dynamic chunking."},
    )

    @property
    def max_chunk_size(self) -> int:
        return self.max_chunk_size_param

    @property
    def min_chunk_size(self) -> int:
        return self.min_chunk_size_param

    @property
    def target_batch_time(self) -> float:
        return self.target_batch_time_param

    @staticmethod
    def get_type() -> ReplicaSchedulerType:
        return ReplicaSchedulerType.DYNAMIC_CHUNK

    def __post_init__(self):
        assert self.max_chunk_size_param >= self.min_chunk_size_param
        assert self.target_batch_time_param > 0

        self._native_handle = DynamicChunkReplicaSchedulerConfig_C(
            self.max_batch_size,
            self.max_chunk_size_param,
            self.min_chunk_size_param,
            self.target_batch_time_param,
        )


@frozen_dataclass
class SpaceSharingReplicaSchedulerConfig(BaseReplicaSchedulerConfig):
    max_chunk_size_param: int = field(
        default=8192,
        metadata={"help": "Maximum chunk size."},
    )
    min_chunk_size_param: int = field(
        default=32,
        metadata={"help": "Minimum chunk size."},
    )
    target_batch_time_param: float = field(
        default=0.05,
        metadata={"help": "Target batch time for ST."},
    )
    long_seq_kv_cache_len_threshold: float = field(
        default=256 * 1024,
        metadata={
            "help": "Minimum KV cache length to be categorized as a long request."
        },
    )

    @property
    def max_chunk_size(self) -> int:
        return self.max_chunk_size_param

    @property
    def min_chunk_size(self) -> int:
        return self.min_chunk_size_param

    @property
    def target_batch_time(self) -> float:
        return self.target_batch_time_param

    @staticmethod
    def get_type() -> ReplicaSchedulerType:
        return ReplicaSchedulerType.SPACE_SHARING

    def __post_init__(self):
        assert self.max_chunk_size_param >= self.min_chunk_size_param
        assert self.target_batch_time_param > 0
        assert self.long_seq_kv_cache_len_threshold > 0

        self._native_handle = SpaceSharingReplicaSchedulerConfig_C(
            self.max_batch_size,
            self.max_chunk_size_param,
            self.min_chunk_size_param,
            self.target_batch_time_param,
            self.long_seq_kv_cache_len_threshold,
        )
