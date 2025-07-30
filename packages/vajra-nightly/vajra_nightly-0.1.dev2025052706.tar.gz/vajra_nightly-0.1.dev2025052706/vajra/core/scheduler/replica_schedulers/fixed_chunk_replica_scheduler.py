from typing import Type

from vajra._native.core.scheduler.replica_schedulers import (
    BaseReplicaScheduler as BaseReplicaSchedulerC,
)
from vajra._native.core.scheduler.replica_schedulers import (
    FixedChunkReplicaScheduler as FixedChunkReplicaSchedulerC,
)
from vajra.core.scheduler.replica_schedulers.base_replica_scheduler import (
    BaseReplicaScheduler,
)


class FixedChunkReplicaScheduler(BaseReplicaScheduler):

    def _get_native_handle_impl(self) -> Type[BaseReplicaSchedulerC]:
        return FixedChunkReplicaSchedulerC
