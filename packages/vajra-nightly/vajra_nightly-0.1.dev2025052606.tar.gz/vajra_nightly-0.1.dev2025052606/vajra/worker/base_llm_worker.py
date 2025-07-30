"""A GPU LLM worker class."""

import os
import time
from functools import wraps
from typing import Optional, Tuple, cast

import torch
import torch.distributed

from vajra._native.utils.zmq_helper import recv_step_inputs, send_step_outputs
from vajra._native.worker import BaseLLMWorker as BaseLLMWorkerC
from vajra.config import (
    BaseReplicaControllerConfig,
    LlmReplicaControllerConfig,
    MetricsConfig,
    ParallelConfig,
)
from vajra.core.sequence_manager import (
    WorkerSequenceManager,
    WorkerSequenceManagerParams,
)
from vajra.datatypes import (
    CommInfo,
    SamplerOutputs,
    SchedulerOutput,
    Sequence,
    StepOutputs,
)
from vajra.enums import ReplicaControllerType
from vajra.logger import init_logger
from vajra.metrics_store import CpuTimer, MetricType
from vajra.model_executor import set_random_seed
from vajra.model_executor.llm_model_runner import LLMModelRunner
from vajra.model_executor.parallel_utils.parallel_state import (
    get_kv_parallel_rank,
    get_kv_parallel_world_size,
    get_pipeline_model_parallel_rank,
    get_process_group_wrapper,
    get_rank,
    get_tensor_model_parallel_rank,
    initialize_model_parallel,
)
from vajra.model_executor.utils import use_native_backend
from vajra.utils.threading_utils import exit_on_error, synchronized
from vajra.worker.base_worker import BaseWorker
from vajra.worker.cache_engine import CacheEngine

logger = init_logger(__name__)


_READY_ACK_WAIT_TIME = 1


def initialize_execution_loop(method):
    """
    Decorator that handles common initialization steps for worker execution loops:
    1. Sets the CUDA device
    2. Sets the worker_ready_event
    """

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        # Set the CUDA device
        torch.cuda.set_device(self.device)

        # Signal that the worker is ready
        self.worker_ready_event.set()

        return method(self, *args, **kwargs)

    return wrapper


class BaseLLMWorker(BaseWorker):
    """A worker class that executes (a partition of) the model on a GPU.

    Each worker is associated with a single GPU. The worker is responsible for
    maintaining the KV cache and executing the model on the GPU. In case of
    distributed inference, each worker is assigned a partition of the model.
    """

    def __init__(
        self,
        replica_id: int,
        config: BaseReplicaControllerConfig,
        metrics_config: MetricsConfig,
        local_rank: int,
        rank: int,
        comm_info: CommInfo,
    ) -> None:
        super().__init__(
            replica_id=replica_id,
            config=config,
            metrics_config=metrics_config,
            local_rank=local_rank,
            rank=rank,
            comm_info=comm_info,
        )
        assert self.config.get_type() in [
            ReplicaControllerType.LLM_BASE,
            ReplicaControllerType.LLM_PIPELINE_PARALLEL,
        ], "BaseLLMWorker must be initialized with a LlmReplicaControllerConfig"
        self.config = cast(LlmReplicaControllerConfig, self.config)
        self.replica_id = replica_id
        # Setting up BaseLLMWorker specific parts like cache engine, sequence manager
        # Uninitialized cache engine. Will be initialized by
        # self.init_cache_engine().
        self.cache_engine: Optional[CacheEngine] = None
        self.gpu_cache: Optional[list] = None
        # Sequence manager also needs number of blocks for initialization
        self.seq_manager: Optional[WorkerSequenceManager] = None
        # Will be set after model initialization
        self.use_native_execution_backend: Optional[bool] = None
        # Native handle for critical path of worker execution
        self.native_handle: Optional[BaseLLMWorkerC] = None

        self._init_worker_timers()

    def _init_worker_timers(self) -> None:
        self.on_schedule_handling_timer = CpuTimer(
            MetricType.WORKER_ON_SCHEDULE_HANDLING, self.rank
        )
        self.on_step_completed_handling_timer = CpuTimer(
            MetricType.WORKER_ON_STEP_COMPLETE_HANDLING, self.rank
        )

    def _verify_parallel_config(self) -> None:
        assert self.config.parallel_config.pipeline_parallel_size == 1

    @torch.inference_mode()
    @synchronized
    def init_model(self):
        # torch.distributed.all_reduce does not free the input tensor until
        # the synchronization point. This causes the memory usage to grow
        # as the number of all_reduce calls increases. This env var disables
        # this behavior.
        # Related issue:
        # https://discuss.pytorch.org/t/cuda-allocation-lifetime-for-inputs-to-distributed-all-reduce/191573
        os.environ["TORCH_NCCL_AVOID_RECORD_STREAMS"] = "1"
        os.environ["KINETO_LOG_LEVEL"] = "5"
        # os.environ["NCCL_DEBUG"] = "INFO"
        # This env var set by Ray causes exceptions with graph building.
        os.environ.pop("NCCL_ASYNC_ERROR_HANDLING", None)

        logger.info(f"Worker {self.rank} is using device {self.local_rank}")
        self.device = torch.device(f"cuda:{self.local_rank}")
        torch.cuda.set_device(self.device)

        # Initialize the distributed environment.
        _init_distributed_environment(
            self.config.parallel_config,
            self.rank,
            self.comm_info.distributed_init_method,
        )

        self.tensor_model_parallel_rank = get_tensor_model_parallel_rank()
        self.pipeline_model_parallel_rank = get_pipeline_model_parallel_rank()
        self.kv_parallel_rank = get_kv_parallel_rank()

        self.is_tensor_parallel_rank_zero = self.tensor_model_parallel_rank == 0
        self.is_first_pipeline_stage = self.pipeline_model_parallel_rank == 0
        self.is_last_pipeline_stage = (
            self.pipeline_model_parallel_rank
            == self.config.parallel_config.pipeline_parallel_size - 1
        )

        logger.info(
            f"Initializing worker {self.rank} on device {self.device}, "
            f"tensor parallel rank {self.tensor_model_parallel_rank} "
            f"and pipeline parallel rank {self.pipeline_model_parallel_rank} "
            f"and cache parallel rank {self.kv_parallel_rank}."
        )

        # Initialize the model.
        set_random_seed(self.config.model_config.seed)
        self.model_runner = LLMModelRunner(
            self.config,
            self.device,
            self.rank,
        )
        # Set native execution backend based on model
        self.use_native_execution_backend = (
            self.model_runner.use_native_execution_backend
        )

        logger.info(f"Model initialized on worker {self.rank}.")

    def _get_seq_manager_impl(self):
        return WorkerSequenceManager

    def _init_native_handle(self):
        self.native_handle = BaseLLMWorkerC(
            self.replica_id,
            self.rank,
            self.enqueue_socket,
            self.output_socket,
            self.seq_manager,
            self.metrics_store.native_handle,
            self.model_runner.native_handle,
            self.gpu_cache,
            get_process_group_wrapper(),
        )

    @torch.inference_mode()
    @synchronized
    def init_cache_engine(self, num_gpu_blocks: int) -> None:
        torch.cuda.set_device(self.device)

        self.cache_engine = CacheEngine(
            self.config,
            num_gpu_blocks,
        )
        self.gpu_cache = self.cache_engine.gpu_cache

        self.seq_manager = self._get_seq_manager_impl()(
            WorkerSequenceManagerParams(
                enable_sequence_pipeline_parallel=self.config.parallel_config.enable_sequence_pipeline_parallel,
                block_size=self.config.cache_config.block_size,
                num_gpu_blocks=num_gpu_blocks,
                max_model_len=self.config.model_config.max_model_len,
                max_num_tokens_per_kvp_group=self.config.parallel_config.max_num_tokens_per_kvp_group,
                rank=get_rank(),
                kvp_group_id=get_kv_parallel_rank(),
                kvp_parallel_world_size=get_kv_parallel_world_size(),
            ),
        )

        self.metrics_store.reset()

        if self.use_native_execution_backend:
            self._init_native_handle()

        self.execution_thread.start()

    def wait_till_ready(self) -> None:
        self.worker_ready_event.wait()
        time.sleep(_READY_ACK_WAIT_TIME)

    @synchronized
    def get_model_parallel_ranks(self) -> Tuple[int, int, int]:
        return (
            self.tensor_model_parallel_rank,
            self.pipeline_model_parallel_rank,
            self.kv_parallel_rank,
        )

    def on_step_completed(
        self,
        scheduler_output: SchedulerOutput,
        sampler_outputs: Optional[SamplerOutputs],
    ) -> None:
        assert self.seq_manager is not None
        assert sampler_outputs is not None

        self.seq_manager.on_step_completed(
            scheduler_output.seq_schedule_metadata_list, sampler_outputs
        )

    @torch.inference_mode()
    def execute_model(
        self,
        scheduler_output: SchedulerOutput,
    ) -> Optional[SamplerOutputs]:
        assert self.seq_manager is not None

        torch.cuda.synchronize()
        batch_stage_start_time = time.time()

        self.metrics_store.on_batch_stage_start(scheduler_output)

        with self.on_schedule_handling_timer:
            _, seqs, seq_metadata_list = self.seq_manager.on_schedule_worker(
                scheduler_output
            )

        sampler_outputs = self.model_runner.run(
            seqs,
            seq_metadata_list,
            self.gpu_cache,
        )

        assert sampler_outputs is not None

        with self.on_step_completed_handling_timer:
            self.on_step_completed(scheduler_output, sampler_outputs)

        torch.cuda.synchronize()

        batch_stage_end_time = time.time()

        self.metrics_store.on_batch_stage_end(
            self.replica_id,
            seq_metadata_list,
            self.tensor_model_parallel_rank,
            self.pipeline_model_parallel_rank,
            self.kv_parallel_rank,
            batch_stage_start_time,
            batch_stage_end_time,
        )

        return sampler_outputs

    @exit_on_error
    @initialize_execution_loop
    @use_native_backend
    def _execution_loop(self) -> None:
        assert self.seq_manager is not None
        while True:
            step_inputs = recv_step_inputs(self.enqueue_socket)

            for params in step_inputs.new_seq_params:  # type: ignore
                new_seq = Sequence(params)
                self.seq_manager.add_sequence(new_seq)

            output = self.execute_model(step_inputs.scheduler_output)

            if not self.is_tensor_parallel_rank_zero:
                continue

            assert output is not None

            step_outputs = StepOutputs(
                step_inputs.scheduler_output.id,
                output,
            )
            send_step_outputs(self.output_socket, step_outputs)

    @synchronized
    def profile_num_available_blocks(
        self,
        block_size: int,
        gpu_memory_utilization: float,
    ) -> int:
        return self.model_runner.profile_num_available_blocks(
            block_size, gpu_memory_utilization
        )


def _init_distributed_environment(
    parallel_config: ParallelConfig,
    rank: int,
    distributed_init_method: str,
) -> None:
    """Initialize the distributed environment."""
    if torch.distributed.is_initialized():
        torch_world_size = torch.distributed.get_world_size()
        if torch_world_size != parallel_config.world_size:
            raise RuntimeError(
                "torch.distributed is already initialized but the torch world "
                "size does not match parallel_config.world_size "
                f"({torch_world_size} vs. {parallel_config.world_size})."
            )
    else:
        torch.distributed.init_process_group(
            backend="nccl",
            world_size=parallel_config.world_size,
            rank=rank,
            init_method=distributed_init_method,
        )

    initialize_model_parallel(
        parallel_config.tensor_parallel_size,
        parallel_config.pipeline_parallel_size,
        parallel_config.kv_parallel_size,
    )

    # A small all_reduce for warmup.
    torch.distributed.all_reduce(torch.zeros(1).cuda())
