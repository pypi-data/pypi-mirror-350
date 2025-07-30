from dataclasses import field
from typing import Optional

from vajra._native.configs import MetricsConfig as MetricsConfig_C
from vajra.utils.dataclasses import frozen_dataclass


@frozen_dataclass
class MetricsConfig:
    """Metric configuration."""

    write_metrics: bool = field(
        default=False, metadata={"help": "Whether to write metrics."}
    )
    wandb_project: Optional[str] = field(
        default=None, metadata={"help": "Weights & Biases project name."}
    )
    wandb_group: Optional[str] = field(
        default=None, metadata={"help": "Weights & Biases group name."}
    )
    wandb_run_name: Optional[str] = field(
        default=None, metadata={"help": "Weights & Biases run name."}
    )
    wandb_sweep_id: Optional[str] = field(
        default=None, metadata={"help": "Weights & Biases sweep ID."}
    )
    wandb_run_id: Optional[str] = field(
        default=None, metadata={"help": "Weights & Biases run ID."}
    )
    enable_gpu_op_level_metrics: bool = field(
        default=False, metadata={"help": "Enable operation-level metrics."}
    )
    enable_cpu_op_level_metrics: bool = field(
        default=False, metadata={"help": "Enable CPU operation-level metrics."}
    )
    enable_chrome_trace: bool = field(
        default=False, metadata={"help": "Enable Chrome tracing."}
    )
    keep_individual_batch_metrics: bool = field(
        default=False, metadata={"help": "Keep individual batch metrics."}
    )
    store_png: bool = field(default=False, metadata={"help": "Store PNG plots."})
    output_dir: str = field(
        default=".", metadata={"help": "Base output directory for the vajra engine run"}
    )

    def __post_init__(self):
        # Create native handler
        self.native_handle = MetricsConfig_C(
            self.write_metrics,
            self.wandb_project,
            self.wandb_group,
            self.wandb_run_name,
            self.wandb_sweep_id,
            self.wandb_run_id,
            self.enable_gpu_op_level_metrics,
            self.enable_cpu_op_level_metrics,
            self.enable_chrome_trace,
            self.keep_individual_batch_metrics,
            self.store_png,
            self.output_dir,
        )
