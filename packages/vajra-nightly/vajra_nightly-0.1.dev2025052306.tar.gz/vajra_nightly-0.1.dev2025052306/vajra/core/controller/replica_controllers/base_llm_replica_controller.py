import math
import time
from functools import partial
from typing import Any, Dict, List, Type

from vajra._native.core.controller.replica_controllers import (
    BaseLlmReplicaController as BaseLlmReplicaControllerC,
)
from vajra.config import LlmReplicaControllerConfig
from vajra.core.controller.replica_controllers.base_replica_controller import (
    BaseReplicaController,
)
from vajra.core.scheduler.replica_schedulers import ReplicaSchedulerRegistry
from vajra.core.scheduler.request_prioritizers.base_request_prioritizer import (
    BaseRequestPrioritizer,
)
from vajra.core.sequence_manager import EngineSequenceManager
from vajra.data_structures import (
    RequestOutputQueue,
    SequencePriorityQueue,
    UserSequenceParamQueue,
)
from vajra.datatypes import (
    CommInfo,
    ModelParallelRank,
    ResourceMapping,
)
from vajra.logger import init_logger
from vajra.metrics_store import MetricsStoreHandle
from vajra.metrics_store.engine_metrics_store import EngineMetricsStore
from vajra.transformers_utils.tokenizer import get_tokenizer
from vajra.utils import get_ip, unset_cuda_visible_devices
from vajra.utils.ray_utils import RayWorker, initialize_cluster, ray

logger = init_logger(__name__)

MAX_WORKER_CONCURRENCY = 1
MAX_ZMQ_RETRIES = 5
ZMQ_RETRY_DELAY = 1
SCHEDULER_LOOP_DELAY = 0.01


class BaseLLMReplicaController(BaseReplicaController):
    """An LLM Replica Controller that receives requests and generates texts.

    This is the main class for the Vajra engine. It receives requests
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
            waiting_seq_queue=waiting_seq_queue,
            output_queue=output_queue,
            request_prioritizer=request_prioritizer,
        )

        logger.info(
            f"Initializing an LLM Controller [Replica {replica_id}] with config: "
            f"model={config.model_config.model!r}, "
            f"dtype={config.model_config.torch_dtype}, "
            f"tensor_parallel_size={config.parallel_config.tensor_parallel_size}, "
            f"pipeline_parallel_size={config.parallel_config.pipeline_parallel_size}, "
            f"kv_parallel_size={config.parallel_config.kv_parallel_size}, "
            f"enable_expert_parallel={config.parallel_config.enable_expert_parallel}, "
            f"seed={config.model_config.seed})"
        )

        self._verify_args()

        tokenizer = get_tokenizer(
            config.model_config.model,
            revision=config.model_config.revision,
        )
        self.seq_manager = EngineSequenceManager(
            tokenizer,
            config.parallel_config.enable_sequence_pipeline_parallel,
        )

        metrics_store = MetricsStoreHandle.get_instance()
        assert isinstance(metrics_store, EngineMetricsStore)
        self.metrics_store: EngineMetricsStore = metrics_store

        self.worker_map: Dict[ModelParallelRank, int] = {}

        initialize_cluster()

        self.comm_info = CommInfo(get_ip())

        self._init_workers_ray()

        # Profile the memory usage and initialize the cache.
        self.num_gpu_blocks = self._init_cache()

        # Initialize the worker map.
        self._init_worker_map()

        # Create the scheduler.
        self.scheduler = ReplicaSchedulerRegistry.get(
            config.scheduler_config.get_type(),
            config.model_config,
            config.scheduler_config,
            config.cache_config,
            config.parallel_config,
            self.num_gpu_blocks,
            self.waiting_seq_queue,
            self.request_prioritizer,
        )
        self.new_seq_params_queue = UserSequenceParamQueue()

        self._run_workers("wait_till_ready")

        self.native_handle = self._get_native_handle_provider()(
            self.replica_id,
            self.config.native_handle,
            self.request_prioritizer.native_handle,
            self.comm_info,
            self.waiting_seq_queue,
            self.output_queue,
            self.scheduler.native_handle,
            self.seq_manager,
            self.metrics_store.native_handle,
        )

    def _get_native_handle_provider(self) -> Type[BaseLlmReplicaControllerC]:
        return BaseLlmReplicaControllerC

    def _validate_parallel_config(self) -> None:
        assert self.config.parallel_config.pipeline_parallel_size == 1

    def _get_worker_impl(self):
        # Lazy import the Worker to avoid importing torch.cuda/xformers
        # before CUDA_VISIBLE_DEVICES is set in the Worker
        from vajra.worker.base_llm_worker import (
            BaseLLMWorker,  # pylint: disable=import-outside-toplevel
        )

        return BaseLLMWorker

    def _init_workers_ray(self, **ray_remote_kwargs):
        # Resources must be set by the InferenceEngine before controller initialization
        assert self.resource_mapping is not None

        self.workers: List[RayWorker] = []

        unset_cuda_visible_devices()

        for rank, (node_ip, device_id) in enumerate(self.resource_mapping):
            worker_class = ray.remote(
                num_cpus=1,
                # num_gpus=1, # we don't use ray for managing GPUs
                **ray_remote_kwargs,
            )(RayWorker)

            if node_ip:
                worker_class = worker_class.options(
                    max_concurrency=MAX_WORKER_CONCURRENCY,
                    resources={
                        node_ip: 0.01,
                    },
                )
            else:
                worker_class = worker_class.options(
                    max_concurrency=MAX_WORKER_CONCURRENCY,
                )

            worker = worker_class.remote(self.config.model_config.trust_remote_code)  # type: ignore
            self.workers.append(worker)

        worker_impl = self._get_worker_impl()

        for rank, (node_ip, device_id) in enumerate(self.resource_mapping):
            worker = self.workers[rank]
            comm_info = self.comm_info
            replica_id = self.replica_id
            config = self.config
            metrics_config = self.metrics_store.config
            promise = worker.init_worker.remote(  # type: ignore
                lambda rank=rank, local_rank=device_id: worker_impl(
                    replica_id=replica_id,
                    config=config,
                    metrics_config=metrics_config,
                    local_rank=local_rank,
                    rank=rank,
                    comm_info=comm_info,
                )
            )
            ray.get(promise)

        self._run_workers(
            "init_model",
            get_all_outputs=True,
        )

    def _verify_args(self) -> None:
        self._validate_parallel_config()
        self.config.model_config.verify_with_parallel_config(
            self.config.parallel_config
        )

    def _get_blocks_per_request(self) -> int:
        if self.config.parallel_config.kv_parallel_size == 1:
            return math.ceil(
                self.config.model_config.max_model_len
                / self.config.cache_config.block_size
            )

        return math.ceil(
            self.config.parallel_config.max_num_tokens_per_kvp_group
            / self.config.cache_config.block_size
        )

    def _init_cache(self) -> int:
        """Profiles the memory usage and initializes the KV cache."""
        # Get the maximum number of blocks that can be allocated on GPU.
        num_gpu_blocks_across_workers = self._run_workers(
            "profile_num_available_blocks",
            get_all_outputs=True,
            block_size=self.config.cache_config.block_size,
            gpu_memory_utilization=self.config.worker_config.gpu_memory_utilization,
        )

        # Since we use a shared centralized controller, we take the minimum
        # number of blocks across all workers to make sure all the memory
        # operators can be applied to all workers.
        num_gpu_blocks = min(num_gpu_blocks_across_workers)
        # FIXME(woosuk): Change to debug log.
        logger.info(f"# GPU blocks: {num_gpu_blocks}")

        if num_gpu_blocks <= 0:
            raise ValueError(
                "No available memory for the cache blocks. "
                "Try increasing `gpu_memory_utilization` when "
                "initializing the engine."
            )
        max_blocks_per_request = self._get_blocks_per_request()
        if num_gpu_blocks < max_blocks_per_request:
            raise ValueError(
                f"Not enough available memory to schedule a request will maximum allowed length {self.config.model_config.max_model_len}. "
                f"Need {max_blocks_per_request}, available {num_gpu_blocks} gpu blocks. "
                f"Try decreasing `max_batch_size`, `max_model_len`."
            )
        # Initialize the cache.
        self._run_workers(
            "init_cache_engine",
            num_gpu_blocks=num_gpu_blocks,
            get_all_outputs=True,
        )
        return num_gpu_blocks

    def _init_worker_map(self) -> None:
        model_parallel_ranks = self._run_workers(
            "get_model_parallel_ranks",
            get_all_outputs=True,
        )

        self.worker_map = {mp_rank: i for i, mp_rank in enumerate(model_parallel_ranks)}

    def _run_workers(
        self,
        method: str,
        *args,
        get_all_outputs: bool = False,
        ignore_output: bool = False,
        **kwargs,
    ) -> Any:
        """Runs the given method on all workers."""
        all_outputs = []
        for worker in self.workers:
            executor = partial(worker.execute_method.remote, method)  # type: ignore

            output = executor(*args, **kwargs)
            all_outputs.append(output)

        if ignore_output:
            return

        while True:
            try:
                all_outputs = ray.get(all_outputs, timeout=0)
                break
            except ray.exceptions.GetTimeoutError:  # type: ignore
                time.sleep(0)
                continue

        if get_all_outputs:
            return all_outputs

        # Make sure all workers have the same results.
        output = all_outputs[0]
        for other_output in all_outputs[1:]:
            assert output == other_output
        return output

    def _run_worker(
        self,
        model_parallel_rank: ModelParallelRank,
        method: str,
        *args,
        **kwargs,
    ) -> Any:
        """Runs the given method on all workers."""
        worker = self.workers[self.worker_map[model_parallel_rank]]
        executor = partial(worker.execute_method.remote, method)  # type: ignore

        output = executor(*args, **kwargs)

        while True:
            try:
                output = ray.get(output, timeout=0)
                break
            except ray.exceptions.GetTimeoutError:  # type: ignore
                time.sleep(0)
                continue

        return output

    def _pull_worker_metrics(self) -> None:
        worker_metrics = self._run_workers(
            "get_metrics_store",
            get_all_outputs=True,
        )
        for worker_metric in worker_metrics:
            self.metrics_store.merge(worker_metric)

    def reset_metrics(self) -> None:
        self.scheduler.reset_state()
        self.metrics_store.reset()
        self._run_workers("reset_metrics", get_all_outputs=True)

    def get_metric_store(self) -> EngineMetricsStore:
        self._pull_worker_metrics()
        return self.metrics_store
