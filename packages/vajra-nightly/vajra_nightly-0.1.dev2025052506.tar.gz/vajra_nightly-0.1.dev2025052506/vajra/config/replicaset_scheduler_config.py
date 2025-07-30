from vajra._native.configs import (
    PullReplicasetSchedulerConfig as PullReplicasetSchedulerConfig_C,
)
from vajra._native.configs import (
    RoundRobinReplicasetSchedulerConfig as RoundRobinReplicasetSchedulerConfig_C,
)
from vajra.config.base_poly_config import BasePolyConfig
from vajra.enums import ReplicasetSchedulerType
from vajra.utils.dataclasses import frozen_dataclass


@frozen_dataclass
class BaseReplicasetSchedulerConfig(BasePolyConfig):
    """Base configuration for replicaset schedulers."""

    @property
    def native_handle(self):
        return self._native_handle  # type: ignore


@frozen_dataclass
class PullReplicasetSchedulerConfig(BaseReplicasetSchedulerConfig):
    """Pull replicaset scheduler configuration."""

    @staticmethod
    def get_type() -> ReplicasetSchedulerType:
        return ReplicasetSchedulerType.PULL

    def __post_init__(self):
        self._native_handle = PullReplicasetSchedulerConfig_C()


@frozen_dataclass
class RoundRobinReplicasetSchedulerConfig(BaseReplicasetSchedulerConfig):
    """Round robin replicaset scheduler configuration."""

    @staticmethod
    def get_type() -> ReplicasetSchedulerType:
        return ReplicasetSchedulerType.ROUND_ROBIN

    def __post_init__(self):
        self._native_handle = RoundRobinReplicasetSchedulerConfig_C()
