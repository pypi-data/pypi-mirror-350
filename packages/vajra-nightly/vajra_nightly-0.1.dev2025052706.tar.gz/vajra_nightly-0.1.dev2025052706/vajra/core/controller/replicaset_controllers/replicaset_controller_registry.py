from vajra.core.controller.replicaset_controllers.llm_replicaset_controller import (
    LLMReplicasetController,
)
from vajra.enums import ReplicasetControllerType
from vajra.utils.base_registry import BaseRegistry


class ReplicasetControllerRegistry(BaseRegistry):
    pass


ReplicasetControllerRegistry.register(
    ReplicasetControllerType.LLM, LLMReplicasetController
)
