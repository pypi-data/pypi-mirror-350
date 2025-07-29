from abc import ABC
from dataclasses import field

from vajra.config.flat_dataclass import create_flat_dataclass
from vajra.config.inference_engine_config import InferenceEngineConfig
from vajra.logger import init_logger
from vajra.utils.dataclasses import frozen_dataclass

logger = init_logger(__name__)


@frozen_dataclass
class BaseEndpointConfig(ABC):
    log_level: str = field(default="info", metadata={"help": "Logging level."})
    inference_engine_config: InferenceEngineConfig = field(
        default_factory=InferenceEngineConfig
    )

    @classmethod
    def create_from_cli_args(cls):
        flat_config = create_flat_dataclass(cls).create_from_cli_args()
        instance = flat_config.reconstruct_original_dataclass()
        object.__setattr__(instance, "__flat_config__", flat_config)
        return instance

    def to_dict(self):
        if not hasattr(self, "__flat_config__"):
            logger.warning("Flat config not found. Returning the original config.")
            return self.__dict__

        return self.__flat_config__.__dict__  # type: ignore
