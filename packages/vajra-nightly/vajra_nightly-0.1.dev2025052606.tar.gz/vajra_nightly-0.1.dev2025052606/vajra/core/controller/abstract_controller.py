from abc import ABC, abstractmethod

from vajra.config import ModelConfig
from vajra.data_structures import (
    RequestOutputQueue,
    SequencePriorityQueue,
    UserSequenceParamQueue,
)
from vajra.metrics_store import EngineMetricsStore


class AbstractController(ABC):
    """Abstract base class defining the interface for Vajra controllers.

    This class defines the common interface that all controller implementations
    must adhere to, ensuring consistency across different parallel strategies.

    Note: In the future, we will have an AbstractControllerConfig
    """

    @abstractmethod
    def __init__(
        self,
        waiting_seq_queue: UserSequenceParamQueue | SequencePriorityQueue,
        output_queue: RequestOutputQueue,
    ) -> None:
        """Initialize the controller with the given configuration.

        Args:
            waiting_seq_queue: Queue to which waiting sequences are sent
            output_queue: Queue to which outputs are sent
        """
        self.waiting_seq_queue = waiting_seq_queue
        self.output_queue = output_queue

    @abstractmethod
    def get_metric_store(self) -> EngineMetricsStore:
        """Get the metrics store for this controller.

        Returns:
            The metrics store containing performance metrics.
        """

    @abstractmethod
    def reset_metrics(self) -> None:
        """Reset all metrics collection."""

    @abstractmethod
    def get_model_config(self) -> ModelConfig:
        """Get the model configuration.

        Returns:
            The model configuration used by this controller.
        """
