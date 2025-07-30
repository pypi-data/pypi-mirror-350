from vajra._native.core.scheduler.replicaset_schedulers import (
    RoundRobinReplicasetScheduler as RoundRobinReplicasetScheduler_C,
)
from vajra.config import RoundRobinReplicasetSchedulerConfig
from vajra.core.scheduler.replicaset_schedulers import BaseReplicasetScheduler
from vajra.data_structures import SequencePriorityQueue
from vajra.logger import init_logger

logger = init_logger(__name__)


class RoundRobinReplicasetScheduler(BaseReplicasetScheduler):
    """Round-robin scheduler that distributes requests across replicas."""

    def __init__(
        self, config: RoundRobinReplicasetSchedulerConfig, num_replicas: int
    ) -> None:
        super().__init__(config, num_replicas)
        self.native_handle = RoundRobinReplicasetScheduler_C(
            config.native_handle,
            num_replicas,
        )

    def get_replica_queue(self, replica_id: int) -> SequencePriorityQueue:
        return self.native_handle.get_replica_queue(replica_id)
