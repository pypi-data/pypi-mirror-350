from vajra._native.core.scheduler.request_prioritizers import (
    EdfRequestPrioritizer as EdfRequestPrioritizerC,
)
from vajra.core.scheduler.request_prioritizers.base_request_prioritizer import (
    BaseRequestPrioritizer,
)
from vajra.core.scheduler.utils import ExecutionTimePredictorFactory


class EdfRequestPrioritizer(BaseRequestPrioritizer):
    def _create_native_handle(self) -> EdfRequestPrioritizerC:
        self.execution_time_predictor = (
            ExecutionTimePredictorFactory.get_execution_time_predictor(
                self.model_config, self.cache_config, self.parallel_config
            )
        )
        return EdfRequestPrioritizerC(
            self.config.native_handle,
            self.parallel_config.native_handle,
            self.replica_scheduler_config.native_handle,
            self.execution_time_predictor._native_execution_time_predictor.as_capsule(),
        )
