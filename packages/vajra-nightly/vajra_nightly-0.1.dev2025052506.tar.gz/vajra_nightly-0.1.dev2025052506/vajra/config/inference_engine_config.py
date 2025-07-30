from dataclasses import field
from typing import Optional

from vajra.config.metrics_config import MetricsConfig
from vajra.config.replicaset_controller_config import (
    BaseReplicasetControllerConfig,
    LlmReplicasetControllerConfig,
)
from vajra.datatypes import GlobalResourceMapping
from vajra.utils.dataclasses import frozen_dataclass


@frozen_dataclass
class InferenceEngineConfig:
    """Configuration for the inference engine."""

    controller_config: BaseReplicasetControllerConfig = field(
        default_factory=LlmReplicasetControllerConfig,
        metadata={"help": "Configuration for the LLM replica set controller"},
    )
    metrics_config: MetricsConfig = field(default_factory=MetricsConfig)
    global_resource_mapping: Optional[GlobalResourceMapping] = field(
        default_factory=lambda: None,
        metadata={
            "help": "Resource mapping for the replica set as a dictionary of replica_id to list of (node_ip, device_id) tuples"
        },
    )
