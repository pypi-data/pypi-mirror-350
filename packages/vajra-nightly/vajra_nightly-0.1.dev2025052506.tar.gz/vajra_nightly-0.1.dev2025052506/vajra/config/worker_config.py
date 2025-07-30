from dataclasses import field

from vajra._native.configs import WorkerConfig as WorkerConfig_C
from vajra.utils.dataclasses import frozen_dataclass


@frozen_dataclass
class WorkerConfig:
    gpu_memory_utilization: float = field(
        default=0.8, metadata={"help": "GPU memory utilization fraction (0.0 to 1.0)."}
    )
    use_native_execution_backend: bool = field(
        default=True,
        metadata={"help": "Use native execution backend for the replica."},
    )

    def __post_init__(self):
        self._verify_args()
        # Create native handler
        self.native_handle = WorkerConfig_C(
            self.gpu_memory_utilization,
            self.use_native_execution_backend,
        )

    def _verify_args(self) -> None:
        if not (0.0 <= self.gpu_memory_utilization <= 1.0):
            raise ValueError(
                f"GPU memory utilization ({self.gpu_memory_utilization}) must be "
                "between 0.0 and 1.0."
            )
