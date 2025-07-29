from dataclasses import field

from vajra._native.configs import ParallelConfig as ParallelConfig_C
from vajra.logger import init_logger
from vajra.utils.dataclasses import frozen_dataclass

logger = init_logger(__name__)


@frozen_dataclass
class ParallelConfig:
    pipeline_parallel_size: int = field(
        default=1, metadata={"help": "Number of pipeline parallel groups."}
    )
    tensor_parallel_size: int = field(
        default=1, metadata={"help": "Number of tensor parallel groups."}
    )
    enable_expert_parallel: bool = field(
        default=False, metadata={"help": "Enable expert parallelism."}
    )
    enable_sequence_pipeline_parallel: bool = field(
        default=False, metadata={"help": "Enable sequence pipeline parallelism."}
    )
    enable_chunked_pipeline_comm_opt: bool = field(
        default=False,
        metadata={"help": "Enable chunked pipeline communication optimization."},
    )
    kv_parallel_size: int = field(
        default=1, metadata={"help": "Number of KV parallel groups."}
    )
    max_num_tokens_per_kvp_group: int = field(
        default=0,
        metadata={
            "help": "Maximum number of tokens per KV parallel group. 0 means no limit."
        },
    )

    def __post_init__(self):
        if self.enable_sequence_pipeline_parallel and self.pipeline_parallel_size == 1:
            logger.warning(
                "Sequence pipeline parallelism is enabled but pipeline_parallel_size is 1."
            )
            self.enable_sequence_pipeline_parallel = False

        if self.enable_chunked_pipeline_comm_opt and not (
            self.pipeline_parallel_size > 1 and self.tensor_parallel_size > 1
        ):
            logger.warning(
                "Chunked pipeline communication optimization is enabled but pipeline_parallel_size "
                "or tensor_parallel_size is not greater than 1."
            )
            self.enable_chunked_pipeline_comm_opt = False

        self.world_size = (
            self.pipeline_parallel_size
            * self.tensor_parallel_size
            * self.kv_parallel_size
        )

        self.native_handle = ParallelConfig_C(
            self.pipeline_parallel_size,
            self.tensor_parallel_size,
            self.enable_expert_parallel,
            self.enable_sequence_pipeline_parallel,
            self.enable_chunked_pipeline_comm_opt,
            self.kv_parallel_size,
            self.max_num_tokens_per_kvp_group,
        )
