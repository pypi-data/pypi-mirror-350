from typing import Optional

from vajra._native.enums import ZmqConstants
from vajra._native.utils import ZmqSocket
from vajra._native.utils.zmq_helper import (
    recv_step_inputs,
    send_step_microbatch_outputs,
    send_step_outputs,
)
from vajra._native.worker import PipelineParallelLLMWorker as PipelineParallelLLMWorkerC
from vajra.datatypes import (
    SamplerOutputs,
    SchedulerOutput,
    Sequence,
    StepInputs,
    StepMicrobatchOutputs,
    StepOutputs,
)
from vajra.logger import init_logger
from vajra.model_executor.parallel_utils.parallel_state import get_process_group_wrapper
from vajra.model_executor.utils import use_native_backend
from vajra.utils.threading_utils import exit_on_error
from vajra.worker.base_llm_worker import BaseLLMWorker, initialize_execution_loop

logger = init_logger(__name__)


class PipelineParallelLLMWorker(BaseLLMWorker):
    """A worker class that executes (a partition of) the model on a GPU.

    Each worker is associated with a single GPU. The worker is responsible for
    maintaining the KV cache and executing the model on the GPU. In case of
    distributed inference, each worker is assigned a partition of the model.
    """

    def _init_zmq_sockets(self):
        super()._init_zmq_sockets()
        self.microbatch_socket = ZmqSocket(self.zmq_context, ZmqConstants.PUSH)
        self.microbatch_socket.connect(
            f"tcp://{self.comm_info.engine_ip_address}:{self.comm_info.microbatch_socket_port}"
        )

    def _init_native_handle(self):
        self.native_handle = PipelineParallelLLMWorkerC(
            self.replica_id,
            self.rank,
            self.enqueue_socket,
            self.output_socket,
            self.seq_manager,
            self.metrics_store.native_handle,
            self.model_runner.native_handle,
            self.gpu_cache,
            get_process_group_wrapper(),
            self.microbatch_socket,
        )

    def _verify_parallel_config(self) -> None:
        assert self.config.parallel_config.pipeline_parallel_size > 1

    def on_step_completed(
        self,
        scheduler_output: SchedulerOutput,
        sampler_outputs: Optional[SamplerOutputs],
    ) -> None:
        assert self.seq_manager
        # in pipeline parallel case, each stage won't have sampler output
        # so we need to do the book keeping update later, here we just want to update the stuff for
        # this stage completion
        self.seq_manager.on_stage_completed(scheduler_output)

    @exit_on_error
    @initialize_execution_loop
    @use_native_backend
    def _execution_loop(self) -> None:
        assert self.seq_manager
        while True:
            step_inputs: StepInputs = recv_step_inputs(self.enqueue_socket)

            for params in step_inputs.new_seq_params:  # type: ignore
                new_seq = Sequence(params)
                self.seq_manager.add_sequence(new_seq)

            for pending_step_output in step_inputs.pending_step_outputs:  # type: ignore
                self.seq_manager.on_step_completed(
                    pending_step_output.scheduler_output.seq_schedule_metadata_list,
                    pending_step_output.sampler_outputs,
                )

            output = self.execute_model(step_inputs.scheduler_output)

            if not self.is_tensor_parallel_rank_zero:
                continue

            if self.is_last_pipeline_stage:
                assert output

                logger.debug(
                    f"Worker {self.rank} sending output to engine: {output} for {step_inputs.scheduler_output}",
                )
                step_outputs = StepOutputs(
                    step_inputs.scheduler_output.id,
                    output,
                )
                send_step_outputs(self.output_socket, step_outputs)
            elif self.is_first_pipeline_stage:
                logger.debug(
                    f"Worker {self.rank} sending microbatch signal for {step_inputs.scheduler_output}",
                )
                step_microbatch_outputs = StepMicrobatchOutputs(
                    step_inputs.scheduler_output.id
                )
                send_step_microbatch_outputs(
                    self.microbatch_socket, step_microbatch_outputs
                )
