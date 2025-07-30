from vajra._native.core.scheduler.request_prioritizers import (
    LrsRequestPrioritizer as LrsRequestPrioritizerC,
)
from vajra.core.scheduler.request_prioritizers.base_request_prioritizer import (
    BaseRequestPrioritizer,
)
from vajra.core.scheduler.utils import ExecutionTimePredictorFactory


class LrsRequestPrioritizer(BaseRequestPrioritizer):
    def _create_native_handle(self) -> LrsRequestPrioritizerC:
        self.execution_time_predictor = (
            ExecutionTimePredictorFactory.get_execution_time_predictor(
                self.model_config, self.cache_config, self.parallel_config
            )
        )
        return LrsRequestPrioritizerC(
            self.config.native_handle,
            self.parallel_config.native_handle,
            self.replica_scheduler_config.native_handle,
            self.execution_time_predictor._native_execution_time_predictor.as_capsule(),
        )
