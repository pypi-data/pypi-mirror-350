from typing import Optional

from vajra._native.metrics_store import CpuTimer as CpuTimerC
from vajra._native.metrics_store import MetricType

from .metrics_store_handle import MetricsStoreHandle


class CpuTimer:

    def __init__(self, metric_type: MetricType, rank: Optional[int] = None):
        self.native_handle = CpuTimerC(
            metric_type,
            MetricsStoreHandle.get_instance().native_handle,
        )

    def __enter__(self):
        self.native_handle.start()
        return self

    def __exit__(self, *_):
        self.native_handle.stop()
