from dataclasses import field

from vajra._native.configs import (
    LlmReplicasetControllerConfig as LlmReplicasetControllerConfig_C,
)
from vajra.config.base_poly_config import BasePolyConfig
from vajra.config.replica_controller_config import (
    BaseReplicaControllerConfig,
    LlmReplicaControllerConfig,
)
from vajra.config.replicaset_scheduler_config import (
    BaseReplicasetSchedulerConfig,
    PullReplicasetSchedulerConfig,
)
from vajra.config.request_prioritizer_config import (
    BaseRequestPrioritizerConfig,
    FcfsRequestPrioritizerConfig,
)
from vajra.enums import ReplicasetControllerType
from vajra.utils.dataclasses import frozen_dataclass


@frozen_dataclass
class BaseReplicasetControllerConfig(BasePolyConfig):
    """Base configuration for an LLM replica set controller."""

    num_replicas: int = field(default=1, metadata={"help": "Number of replicas."})
    replica_controller_config: BaseReplicaControllerConfig = field(
        default_factory=LlmReplicaControllerConfig,
        metadata={"help": "Replica configuration for the replica set"},
    )
    request_prioritizer_config: BaseRequestPrioritizerConfig = field(
        default_factory=FcfsRequestPrioritizerConfig,
        metadata={"help": "Request prioritizer configuration for the replica set"},
    )
    replicaset_scheduler_config: BaseReplicasetSchedulerConfig = field(
        default_factory=PullReplicasetSchedulerConfig,
        metadata={"help": "Replicaset scheduler configuration for the replica set"},
    )

    @property
    def native_handle(self):
        return self._native_handle  # type: ignore


@frozen_dataclass
class LlmReplicasetControllerConfig(BaseReplicasetControllerConfig):
    """Configuration for an LLM replica set controller."""

    num_tokenizer_workers: int = field(
        default=10, metadata={"help": "Number of tokenizer workers."}
    )

    @staticmethod
    def get_type() -> ReplicasetControllerType:
        return ReplicasetControllerType.LLM

    def __post_init__(self):
        assert isinstance(self.replica_controller_config, LlmReplicaControllerConfig)

        self._native_handle = LlmReplicasetControllerConfig_C(
            self.num_replicas,
            self.replica_controller_config.native_handle,
            self.request_prioritizer_config.native_handle,
            self.replicaset_scheduler_config.native_handle,
            self.num_tokenizer_workers,
        )
