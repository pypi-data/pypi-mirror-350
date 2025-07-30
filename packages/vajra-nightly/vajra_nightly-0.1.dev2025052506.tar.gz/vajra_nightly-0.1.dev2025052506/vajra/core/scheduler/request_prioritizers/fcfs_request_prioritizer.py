from vajra._native.core.scheduler.request_prioritizers import (
    FcfsRequestPrioritizer as FcfsRequestPrioritizerC,
)
from vajra.core.scheduler.request_prioritizers.base_request_prioritizer import (
    BaseRequestPrioritizer,
)


class FcfsRequestPrioritizer(BaseRequestPrioritizer):

    def _create_native_handle(self) -> FcfsRequestPrioritizerC:
        return FcfsRequestPrioritizerC()
