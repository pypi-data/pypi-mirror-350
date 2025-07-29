from enum import Enum
from typing import Any

from vajra.config import BaseReplicaControllerConfig
from vajra.core.controller.replica_controllers.base_llm_replica_controller import (
    BaseLLMReplicaController,
)
from vajra.core.controller.replica_controllers.pipeline_parallel_llm_replica_controller import (
    PipelineParallelLLMReplicaController,
)
from vajra.enums import ReplicaControllerType
from vajra.utils.base_registry import BaseRegistry


class ReplicaControllerRegistry(BaseRegistry):
    @classmethod
    def get(
        cls,
        key: Enum,
        replica_id: int,
        config: BaseReplicaControllerConfig,
        *args: Any,
        **kwargs: Any,
    ) -> Any:
        if key not in cls._registry:
            raise ValueError(f"{key} is not registered")

        if (
            key == ReplicaControllerType.LLM_BASE
            and config.parallel_config.pipeline_parallel_size > 1
        ):
            return cls._registry[ReplicaControllerType.LLM_PIPELINE_PARALLEL](
                replica_id, config, *args, **kwargs
            )

        return cls._registry[key](replica_id, config, *args, **kwargs)


ReplicaControllerRegistry.register(
    ReplicaControllerType.LLM_BASE, BaseLLMReplicaController
)
ReplicaControllerRegistry.register(
    ReplicaControllerType.LLM_PIPELINE_PARALLEL, PipelineParallelLLMReplicaController
)
