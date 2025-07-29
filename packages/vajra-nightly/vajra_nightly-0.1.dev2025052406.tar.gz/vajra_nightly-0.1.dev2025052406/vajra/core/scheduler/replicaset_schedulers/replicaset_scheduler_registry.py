from vajra.core.scheduler.replicaset_schedulers.pull_replicaset_scheduler import (
    PullReplicasetScheduler,
)
from vajra.core.scheduler.replicaset_schedulers.round_robin_replicaset_scheduler import (
    RoundRobinReplicasetScheduler,
)
from vajra.enums import ReplicasetSchedulerType
from vajra.utils.base_registry import BaseRegistry


class ReplicasetSchedulerRegistry(BaseRegistry):
    pass


ReplicasetSchedulerRegistry.register(
    ReplicasetSchedulerType.ROUND_ROBIN, RoundRobinReplicasetScheduler
)
ReplicasetSchedulerRegistry.register(
    ReplicasetSchedulerType.PULL, PullReplicasetScheduler
)
