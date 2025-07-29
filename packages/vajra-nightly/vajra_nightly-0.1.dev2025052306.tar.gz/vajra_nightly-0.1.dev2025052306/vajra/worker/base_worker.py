"""A GPU worker class."""

import time
from abc import ABC, abstractmethod
from threading import Event, Thread
from typing import Optional

import torch
import torch.distributed

from vajra._native.enums import ZmqConstants
from vajra._native.utils import ZmqContext, ZmqSocket
from vajra.config import BaseReplicaControllerConfig, MetricsConfig
from vajra.datatypes import CommInfo, SamplerOutputs, SchedulerOutput
from vajra.enums import MetricsStoreType
from vajra.logger import init_logger
from vajra.metrics_store import MetricsStoreHandle, WorkerMetricsStore
from vajra.utils.threading_utils import exit_on_error, synchronized

logger = init_logger(__name__)


_READY_ACK_WAIT_TIME = 1


class BaseWorker(ABC):
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
        # TODO(ksukrit): Add a custom config for the worker
        # Not: the cache config is partially initialized at this point, ie. it doesn't have
        # information about the number of blocks, it will get updated after profiling
        self.config = config
        self.local_rank = local_rank
        self.rank = rank
        self.comm_info = comm_info
        self._verify_parallel_config()
        metrics_store = MetricsStoreHandle.get_or_create_instance(
            MetricsStoreType.WORKER,
            metrics_config,
            model_num_layers=self.config.model_config.get_total_num_layers(),
            rank=self.rank,
        )
        assert isinstance(metrics_store, WorkerMetricsStore)
        self.metrics_store = metrics_store

        self._init_zmq_sockets()

        self.worker_ready_event = Event()
        self.execution_thread = Thread(target=self._execution_loop, daemon=True)

    def _init_zmq_sockets(self) -> None:
        """These sockets will remain consistent across the workers
        additional sockets can be added as needed by the worker (see PipelineParallelLLMWorker)

        In the overridden function call `super()._init_zmq_sockets()`
        to initialize these sockets and then add any new sockets as needed
        """
        self.zmq_context = ZmqContext()
        self.enqueue_socket = ZmqSocket(self.zmq_context, ZmqConstants.SUB)
        self.enqueue_socket.connect(
            f"tcp://{self.comm_info.engine_ip_address}:{self.comm_info.enqueue_socket_port}"
        )
        self.enqueue_socket.setsockopt_string(ZmqConstants.SUBSCRIBE, "")
        self.output_socket = ZmqSocket(self.zmq_context, ZmqConstants.PUSH)
        self.output_socket.connect(
            f"tcp://{self.comm_info.engine_ip_address}:{self.comm_info.output_socket_port}"
        )

    def _verify_parallel_config(self) -> None:
        assert self.config.parallel_config.pipeline_parallel_size == 1

    @torch.inference_mode()
    @synchronized
    @abstractmethod
    def init_model(self):
        """Initialize the model on the GPU.
        First setup the distributed env, get the different ranks for different parallelism
        (tensor, pipeline, kv) and then initialize the model.

        This function should also initialize the model runner.
        """

    def wait_till_ready(self) -> None:
        self.worker_ready_event.wait()
        time.sleep(_READY_ACK_WAIT_TIME)

    @torch.inference_mode()
    @abstractmethod
    def execute_model(
        self,
        scheduler_output: SchedulerOutput,
    ) -> Optional[SamplerOutputs]:
        """Executes the model on the GPU.
        This function will do the following :
        1. Call the on_schedule method for the sequence manager
        2. Call the model_runner run method
        3. Call the on_step_completed method for the sequence manager
        4. Report batch/step level metrics to the WorkerMetricsStore
        5. Return the sampler outputs
        """

    @exit_on_error
    @abstractmethod
    def _execution_loop(self) -> None:
        """The main execution loop of the worker.
        This will pull StepInputs (or worker specific StepInput) from enqueue socket,
        Call execute model on these inputs and send the outputs to the output socket.
        """

    def get_metrics_store(self) -> WorkerMetricsStore:
        return self.metrics_store

    @synchronized
    def reset_metrics(self) -> None:
        self.metrics_store.reset()
