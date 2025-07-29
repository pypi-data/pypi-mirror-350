from vajra.config import BaseReplicaControllerConfig, ModelConfig
from vajra.core.controller.abstract_controller import AbstractController
from vajra.core.scheduler.request_prioritizers.base_request_prioritizer import (
    BaseRequestPrioritizer,
)
from vajra.data_structures import RequestOutputQueue, SequencePriorityQueue
from vajra.datatypes import (
    ResourceMapping,
)
from vajra.logger import init_logger

logger = init_logger(__name__)


class BaseReplicaController(AbstractController):
    """Base controller class that implements common functionality for all replica controllers.

    This class provides the foundation for different types of replica controllers,
    implementing common functionality and defining the interface that all replica
    controllers must implement.

    Args:
        config: System Config: The system configuration for the engine.
    """

    def __init__(
        self,
        replica_id: int,
        config: BaseReplicaControllerConfig,
        resource_mapping: ResourceMapping,
        request_prioritizer: BaseRequestPrioritizer,
        waiting_seq_queue: SequencePriorityQueue,
        output_queue: RequestOutputQueue,
    ) -> None:
        super().__init__(
            waiting_seq_queue=waiting_seq_queue,
            output_queue=output_queue,
        )
        self.config = config
        self.replica_id = replica_id
        self.resource_mapping = resource_mapping
        self.request_prioritizer = request_prioritizer

    def get_model_config(self) -> ModelConfig:
        """Get the model configuration."""
        return self.config.model_config
