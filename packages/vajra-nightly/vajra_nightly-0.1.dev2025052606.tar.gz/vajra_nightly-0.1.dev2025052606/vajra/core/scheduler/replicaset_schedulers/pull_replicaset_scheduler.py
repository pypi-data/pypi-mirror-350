from vajra._native.core.scheduler.replicaset_schedulers import (
    PullReplicasetScheduler as PullReplicasetScheduler_C,
)
from vajra.config import PullReplicasetSchedulerConfig
from vajra.core.scheduler.replicaset_schedulers import BaseReplicasetScheduler
from vajra.data_structures import SequencePriorityQueue
from vajra.logger import init_logger

logger = init_logger(__name__)


class PullReplicasetScheduler(BaseReplicasetScheduler):
    """Pull-based scheduler where replicas pull work from a global queue."""

    def __init__(
        self, config: PullReplicasetSchedulerConfig, num_replicas: int
    ) -> None:
        super().__init__(config, num_replicas)
        self.native_handle = PullReplicasetScheduler_C(
            config.native_handle,
            num_replicas,
        )

    def get_replica_queue(self, replica_id: int) -> SequencePriorityQueue:
        return self.native_handle.get_replica_queue(replica_id)
