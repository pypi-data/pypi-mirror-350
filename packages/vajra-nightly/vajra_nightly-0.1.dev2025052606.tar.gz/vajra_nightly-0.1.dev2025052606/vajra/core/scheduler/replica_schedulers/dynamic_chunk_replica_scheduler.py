from typing import Type

from vajra._native.core.scheduler.replica_schedulers import (
    BaseReplicaScheduler as BaseReplicaSchedulerC,
)
from vajra._native.core.scheduler.replica_schedulers import (
    DynamicChunkReplicaScheduler as DynamicChunkReplicaSchedulerC,
)
from vajra.config import (
    BaseReplicaSchedulerConfig,
    CacheConfig,
    ModelConfig,
    ParallelConfig,
)
from vajra.core.scheduler.replica_schedulers.base_replica_scheduler import (
    BaseReplicaScheduler,
)
from vajra.core.scheduler.request_prioritizers import BaseRequestPrioritizer
from vajra.core.scheduler.utils.execution_time_predictor_factory import (
    ExecutionTimePredictorFactory,
)
from vajra.data_structures import SequencePriorityQueue


class DynamicChunkReplicaScheduler(BaseReplicaScheduler):
    def __init__(
        self,
        model_config: ModelConfig,
        scheduler_config: BaseReplicaSchedulerConfig,
        cache_config: CacheConfig,
        parallel_config: ParallelConfig,
        num_gpu_blocks: int,
        waiting_queue: SequencePriorityQueue,
        request_prioritizer: BaseRequestPrioritizer,
    ):
        # Use the factory to get the execution time predictor and its native implementation
        execution_time_predictor = (
            ExecutionTimePredictorFactory.get_execution_time_predictor(
                model_config=self.model_config,
                parallel_config=self.parallel_config,
                cache_config=self.cache_config,
            )
        )
        assert execution_time_predictor is not None
        assert execution_time_predictor._native_execution_time_predictor is not None
        self.execution_time_predictor_capsule = (
            execution_time_predictor._native_execution_time_predictor.as_capsule()
        )

        super().__init__(
            model_config=model_config,
            scheduler_config=scheduler_config,
            cache_config=cache_config,
            parallel_config=parallel_config,
            num_gpu_blocks=num_gpu_blocks,
            waiting_queue=waiting_queue,
            request_prioritizer=request_prioritizer,
        )

    def _get_native_handle_impl(self) -> Type[BaseReplicaSchedulerC]:
        return DynamicChunkReplicaSchedulerC

    def _create_native_handle(self) -> BaseReplicaSchedulerC:
        return self._get_native_handle_impl()(
            model_config=self.model_config.native_handle,
            scheduler_config=self.scheduler_config.native_handle,
            cache_config=self.cache_config.native_handle,
            parallel_config=self.parallel_config.native_handle,
            waiting_queue=self.waiting,
            request_prioritizer=self.request_prioritizer.native_handle,
            execution_time_predictor_capsule=self.execution_time_predictor_capsule,
        )
