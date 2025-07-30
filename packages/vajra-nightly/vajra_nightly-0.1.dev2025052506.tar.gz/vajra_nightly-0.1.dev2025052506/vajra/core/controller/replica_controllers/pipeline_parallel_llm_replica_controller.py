from dataclasses import dataclass
from typing import List

from typing_extensions import Type

from vajra._native.core.controller.replica_controllers import (
    PipelineParallelLlmReplicaController as PipelineParallelLlmReplicaControllerC,
)
from vajra.config import LlmReplicaControllerConfig
from vajra.core.controller.replica_controllers.base_llm_replica_controller import (
    BaseLLMReplicaController,
)
from vajra.core.scheduler.request_prioritizers import BaseRequestPrioritizer
from vajra.data_structures import RequestOutputQueue, SequencePriorityQueue
from vajra.datatypes import (
    ResourceMapping,
    SchedulerOutput,
    Sequence,
)
from vajra.logger import init_logger

logger = init_logger(__name__)


@dataclass(frozen=True)
class ScheduleStageOutputs:
    ignored_seqs: List[Sequence]
    seqs: List[Sequence]
    scheduler_output: SchedulerOutput
    start_time: float


class PipelineParallelLLMReplicaController(BaseLLMReplicaController):
    """An LLM controller that receives requests and generates texts.

    This controller receives requests
    from clients and generates texts from the LLM. It includes a tokenizer, a
    language model (possibly distributed across multiple GPUs), and GPU memory
    space allocated for intermediate states (aka KV cache). This class utilizes
    iteration-level scheduling and efficient memory management to maximize the
    serving throughput.

    Args:
        config; System Config: The system configuration for the engine.
    """

    def __init__(
        self,
        replica_id: int,
        config: LlmReplicaControllerConfig,
        resource_mapping: ResourceMapping,
        request_prioritizer: BaseRequestPrioritizer,
        waiting_seq_queue: SequencePriorityQueue,
        output_queue: RequestOutputQueue,
    ) -> None:
        super().__init__(
            replica_id=replica_id,
            config=config,
            resource_mapping=resource_mapping,
            request_prioritizer=request_prioritizer,
            waiting_seq_queue=waiting_seq_queue,
            output_queue=output_queue,
        )

    def _get_native_handle_provider(
        self,
    ) -> Type[PipelineParallelLlmReplicaControllerC]:
        return PipelineParallelLlmReplicaControllerC

    def _validate_parallel_config(self) -> None:
        assert self.config.parallel_config.pipeline_parallel_size > 1

    def _get_worker_impl(self):
        # Lazy import the Worker to avoid importing torch.cuda/xformers
        # before CUDA_VISIBLE_DEVICES is set in the Worker
        from vajra.worker.pipeline_parallel_llm_worker import PipelineParallelLLMWorker

        return PipelineParallelLLMWorker
