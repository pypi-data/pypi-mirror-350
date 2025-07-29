from abc import ABC, abstractmethod

from vajra._native.core.scheduler.request_prioritizers import (
    BaseRequestPrioritizer as BaseRequestPrioritizerC,
)
from vajra.config import (
    BaseReplicaSchedulerConfig,
    BaseRequestPrioritizerConfig,
    CacheConfig,
    ModelConfig,
    ParallelConfig,
)
from vajra.datatypes import BaseSequenceWithPriority, Sequence


class BaseRequestPrioritizer(ABC):
    def __init__(
        self,
        config: BaseRequestPrioritizerConfig,
        model_config: ModelConfig,
        cache_config: CacheConfig,
        parallel_config: ParallelConfig,
        replica_scheduler_config: BaseReplicaSchedulerConfig,
    ) -> None:
        self.config = config
        self.model_config = model_config
        self.cache_config = cache_config
        self.parallel_config = parallel_config
        self.replica_scheduler_config = replica_scheduler_config

        self.native_handle: BaseRequestPrioritizerC = self._create_native_handle()

    @abstractmethod
    def _create_native_handle(self) -> BaseRequestPrioritizerC:
        pass

    def get_seq_with_priority(self, seq: Sequence) -> BaseSequenceWithPriority:
        return self.native_handle.get_seq_with_priority(seq)
