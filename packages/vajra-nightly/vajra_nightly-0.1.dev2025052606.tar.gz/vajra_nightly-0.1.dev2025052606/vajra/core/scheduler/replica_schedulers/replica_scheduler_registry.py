from vajra.enums import ReplicaSchedulerType
from vajra.utils.base_registry import BaseRegistry

from .dynamic_chunk_replica_scheduler import DynamicChunkReplicaScheduler
from .fixed_chunk_replica_scheduler import FixedChunkReplicaScheduler
from .space_sharing_replica_scheduler import SpaceSharingReplicaScheduler


class ReplicaSchedulerRegistry(BaseRegistry):
    pass


ReplicaSchedulerRegistry.register(
    ReplicaSchedulerType.FIXED_CHUNK, FixedChunkReplicaScheduler
)
ReplicaSchedulerRegistry.register(
    ReplicaSchedulerType.DYNAMIC_CHUNK, DynamicChunkReplicaScheduler
)
ReplicaSchedulerRegistry.register(
    ReplicaSchedulerType.SPACE_SHARING, SpaceSharingReplicaScheduler
)
