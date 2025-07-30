from abc import abstractmethod
from typing import List, Tuple, Type

from vajra._native.core.scheduler.replica_schedulers import (
    BaseReplicaScheduler as BaseReplicaSchedulerC,
)
from vajra.config import (
    BaseReplicaSchedulerConfig,
    CacheConfig,
    ModelConfig,
    ParallelConfig,
)
from vajra.core.scheduler.request_prioritizers import BaseRequestPrioritizer
from vajra.data_structures import SequencePriorityQueue
from vajra.datatypes import SchedulerOutput, Sequence
from vajra.logger import init_logger
from vajra.utils.threading_utils import synchronized

logger = init_logger(__name__)

MAX_NUM_SKIPPED_SEQS = 10


class BaseReplicaScheduler:
    def __init__(
        self,
        model_config: ModelConfig,
        scheduler_config: BaseReplicaSchedulerConfig,
        cache_config: CacheConfig,
        parallel_config: ParallelConfig,
        num_gpu_blocks: int,
        waiting_queue: SequencePriorityQueue,
        request_prioritizer: BaseRequestPrioritizer,
    ) -> None:
        self.model_config = model_config
        self.scheduler_config = scheduler_config
        self.cache_config = cache_config
        self.parallel_config = parallel_config
        self.num_gpu_blocks = num_gpu_blocks
        self.waiting = waiting_queue
        self.request_prioritizer = request_prioritizer
        self._native_handle = self._create_native_handle()

    @property
    def native_handle(self) -> BaseReplicaSchedulerC:
        return self._native_handle

    @abstractmethod
    def _get_native_handle_impl(self) -> Type[BaseReplicaSchedulerC]:
        pass

    @abstractmethod
    def _create_native_handle(self) -> BaseReplicaSchedulerC:
        return self._get_native_handle_impl()(
            model_config=self.model_config.native_handle,
            scheduler_config=self.scheduler_config.native_handle,
            cache_config=self.cache_config.native_handle,
            parallel_config=self.parallel_config.native_handle,
            num_gpu_blocks=self.num_gpu_blocks,
            waiting_queue=self.waiting,
            request_prioritizer=self.request_prioritizer.native_handle,
        )

    def reset_state(self) -> None:
        self.native_handle.reset_state()

    def on_stage_completed(self, seqs: List[Sequence]) -> None:
        self.native_handle.on_stage_completed(seqs)

    def on_step_completed(self, seqs: List[Sequence], execution_time: float) -> None:
        self.native_handle.on_step_completed(seqs, execution_time)

    def is_seq_allocated(self, seq_id: str) -> bool:
        return self.native_handle.is_seq_allocated(seq_id)

    @synchronized
    def schedule(self) -> Tuple[SchedulerOutput, List[Sequence]]:
        return self.native_handle.schedule()

    def free_finished_seqs(self) -> None:
        self.native_handle.free_finished_seqs()
