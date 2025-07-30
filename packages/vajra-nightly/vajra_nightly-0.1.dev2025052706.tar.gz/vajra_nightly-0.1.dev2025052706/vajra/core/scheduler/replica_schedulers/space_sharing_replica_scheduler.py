from typing import Type

from vajra._native.core.scheduler.replica_schedulers import (
    BaseReplicaScheduler as BaseReplicaSchedulerC,
)
from vajra._native.core.scheduler.replica_schedulers import (
    SpaceSharingReplicaScheduler as SpaceSharingReplicaSchedulerC,
)
from vajra.core.scheduler.replica_schedulers.dynamic_chunk_replica_scheduler import (
    DynamicChunkReplicaScheduler,
)

MAX_SPACE_SHARE_FRAC = 0.5


class SpaceSharingReplicaScheduler(DynamicChunkReplicaScheduler):

    def _get_native_handle_impl(self) -> Type[BaseReplicaSchedulerC]:
        return SpaceSharingReplicaSchedulerC
