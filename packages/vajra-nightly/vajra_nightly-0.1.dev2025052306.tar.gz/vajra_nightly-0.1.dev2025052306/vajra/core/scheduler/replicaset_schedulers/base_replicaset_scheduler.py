from abc import ABC, abstractmethod

from vajra.config import BaseReplicasetSchedulerConfig
from vajra.data_structures import SequencePriorityQueue


class BaseReplicasetScheduler(ABC):
    """Base scheduler for managing a set of replicas.

    This abstract class defines the interface for replica set schedulers.
    Implementations must provide concrete logic for queue management and
    sequence assignment strategies.

    Args:
        config: Configuration object for the scheduler
        num_replicas: Number of replicas to manage
    """

    def __init__(
        self, config: BaseReplicasetSchedulerConfig, num_replicas: int
    ) -> None:
        self.config = config
        self.num_replicas = num_replicas

    @abstractmethod
    def get_replica_queue(self, replica_id: int) -> SequencePriorityQueue:
        """Get queue for specific replica.

        Args:
            replica_id: ID of the replica

        Returns:
            SequencePriorityQueue associated with the replica
        """
