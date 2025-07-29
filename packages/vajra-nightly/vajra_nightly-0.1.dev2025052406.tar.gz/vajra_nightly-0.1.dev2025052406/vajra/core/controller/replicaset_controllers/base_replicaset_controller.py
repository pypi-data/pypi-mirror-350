from vajra.config import BaseReplicasetControllerConfig
from vajra.core.controller.abstract_controller import AbstractController
from vajra.data_structures import RequestOutputQueue, UserSequenceParamQueue
from vajra.datatypes import (
    GlobalResourceMapping,
)


class BaseReplicasetController(AbstractController):
    """Base class for all replica set controllers that manage multiple replicas."""

    def __init__(
        self,
        config: BaseReplicasetControllerConfig,
        global_resource_mapping: GlobalResourceMapping,
        waiting_seq_queue: UserSequenceParamQueue,
        output_queue: RequestOutputQueue,
    ) -> None:
        """
        Initialize the controller with the given configuration.
        Args:
            config: System configuration specifying model, parallel strategy etc.
            global_resource_mapping: Mapping of resources to replicas
            waiting_seq_queue: Queue to which waiting sequences are sent
            output_queue: Queue to which outputs are sent
        """
        super().__init__(
            waiting_seq_queue,
            output_queue,
        )
        self.config = config
        self.global_resource_mapping = global_resource_mapping
        self.replica_controller_config = config.replica_controller_config
