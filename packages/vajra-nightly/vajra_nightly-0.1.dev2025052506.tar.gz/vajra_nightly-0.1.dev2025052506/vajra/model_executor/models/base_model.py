from abc import abstractmethod
from typing import Optional

from torch import nn
from transformers.configuration_utils import PretrainedConfig

from vajra.config import LlmReplicaControllerConfig
from vajra.model_executor.parallel_utils.layers import ColumnParallelLinear


class BaseModel(nn.Module):

    def __init__(
        self,
        replica_controller_config: LlmReplicaControllerConfig,
    ) -> None:
        super().__init__()
        self._config: PretrainedConfig = (
            replica_controller_config.model_config.hf_config
        )
        self._use_native_execution_backend: bool = (
            replica_controller_config.worker_config.use_native_execution_backend
        )
        self._enable_expert_parallel: bool = (
            replica_controller_config.parallel_config.enable_expert_parallel
        )
        # NOTE(Amey): Keeping this as a direct access property so that we don't mess up weight loading
        self.lm_head: Optional[ColumnParallelLinear] = None

    @property
    def use_native_execution_backend(self) -> bool:
        return self._use_native_execution_backend

    @property
    def config(self) -> PretrainedConfig:
        return self._config

    @property
    def enable_expert_parallel(self) -> bool:
        return self._enable_expert_parallel

    @abstractmethod
    def is_native_execution_backend_supported(self) -> bool:
        pass

    @abstractmethod
    def load_weights(
        self,
        model_name_or_path: str,
        cache_dir: Optional[str] = None,
        load_format: str = "auto",
        revision: Optional[str] = None,
    ):
        pass
