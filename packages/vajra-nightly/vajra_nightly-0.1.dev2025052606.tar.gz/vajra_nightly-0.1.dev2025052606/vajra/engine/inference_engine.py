from typing import List, Optional

from vajra._native.engine import InferenceEngine as InferenceEngine_C
from vajra.config import InferenceEngineConfig, ModelConfig
from vajra.core.controller.replicaset_controllers.replicaset_controller_registry import (
    ReplicasetControllerRegistry,
)
from vajra.data_structures import RequestOutputQueue, UserSequenceParamQueue
from vajra.datatypes import RequestOutput, SamplingParams
from vajra.engine.resource_allocator import ResourceAllocator
from vajra.enums import MetricsStoreType
from vajra.logger import init_logger
from vajra.metrics_store import EngineMetricsStore, MetricsStoreHandle
from vajra.utils.logging_utils import print_resource_mapping, print_vajra_banner

logger = init_logger(__name__)


class InferenceEngine:
    """High-level inference engine for Vajra.

    This is the main entry point for using Vajra. It provides a simple interface
    for adding requests and getting outputs from the underlying controller.

    Args:
        config: Engine configuration specifying model, parallel strategy etc.
    """

    def __init__(self, config: InferenceEngineConfig) -> None:
        """Initialize the inference engine with resource allocation"""
        # Handle resource allocation at the engine level
        resource_mapping = config.global_resource_mapping
        if resource_mapping is None:
            resource_allocator = ResourceAllocator()
            resource_mapping = resource_allocator.get_replicaset_resource_mapping(
                config.controller_config.num_replicas,
                config.controller_config.replica_controller_config.parallel_config.world_size,
            )

        print_vajra_banner()
        print_resource_mapping(resource_mapping)

        metrics_store = MetricsStoreHandle.get_or_create_instance(
            MetricsStoreType.ENGINE,
            config.metrics_config,
        )
        assert isinstance(metrics_store, EngineMetricsStore)
        self.metrics_store = metrics_store

        self.native_handle = InferenceEngine_C(metrics_store.native_handle)

        self.waiting_seq_queue: UserSequenceParamQueue = UserSequenceParamQueue()
        self.output_queue: RequestOutputQueue = RequestOutputQueue()

        self.controller = ReplicasetControllerRegistry.get(
            config.controller_config.get_type(),
            config.controller_config,
            resource_mapping,
            self.native_handle.get_waiting_seq_queue(),
            self.native_handle.get_output_queue(),
        )

    def add_request(
        self,
        prompt: str,
        sampling_params: SamplingParams,
        prompt_token_ids: List[int] = [],
        seq_id: Optional[str] = None,
    ) -> None:
        """Add a request to be processed.

        Args:
            prompt: The input text prompt
            sampling_params: Parameters controlling text generation
            prompt_token_ids: Optional pre-tokenized prompt
            seq_id: Optional unique identifier for the request
        """
        self.native_handle.add_request(
            seq_id,
            prompt,
            prompt_token_ids,
            sampling_params,
        )

    def get_outputs(self, block: bool = False) -> List[RequestOutput]:
        """Get any available outputs from processed requests.

        Returns:
            List of RequestOutput objects containing generated text and metadata
        """
        return self.native_handle.get_outputs(block)

    def abort(self, seq_id: str) -> None:
        """Abort a specific request.

        Args:
            seq_id: The unique identifier of the request to abort
        """
        # TODO: Implement abort functionality in controllers
        raise NotImplementedError("Abort functionality not yet implemented")

    def reset_metrics(self) -> None:
        """Reset all metrics collection."""
        self.controller.reset_metrics()

    def plot_metrics(self) -> None:
        """Plot collected metrics."""
        self.controller.get_metric_store().plot()

    def get_model_config(self) -> ModelConfig:
        """Return the model configuration for this replica set."""
        return self.controller.get_model_config()
