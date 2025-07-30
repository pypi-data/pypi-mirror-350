from dataclasses import field

from vajra._native.configs import (
    EdfRequestPrioritizerConfig as EdfRequestPrioritizerConfig_C,
)
from vajra._native.configs import (
    FcfsRequestPrioritizerConfig as FcfsRequestPrioritizerConfig_C,
)
from vajra._native.configs import (
    LrsRequestPrioritizerConfig as LrsRequestPrioritizerConfig_C,
)
from vajra.config.base_poly_config import BasePolyConfig
from vajra.enums import RequestPrioritizerType
from vajra.utils.dataclasses import frozen_dataclass


@frozen_dataclass
class BaseRequestPrioritizerConfig(BasePolyConfig):
    """Base configuration for request prioritizers."""

    @property
    def native_handle(self):
        return self._native_handle  # type: ignore


@frozen_dataclass
class FcfsRequestPrioritizerConfig(BaseRequestPrioritizerConfig):
    """FCFS request prioritizer configuration."""

    @staticmethod
    def get_type() -> RequestPrioritizerType:
        return RequestPrioritizerType.FCFS

    def __post_init__(self):
        self._native_handle = FcfsRequestPrioritizerConfig_C()


@frozen_dataclass
class EdfRequestPrioritizerConfig(BaseRequestPrioritizerConfig):
    deadline_multiplier: float = field(
        default=1.5,
        metadata={"help": "Deadline multiplier for EDF."},
    )
    min_deadline: float = field(
        default=0.5,
        metadata={"help": "Minimum deadline for EDF."},
    )

    @staticmethod
    def get_type() -> RequestPrioritizerType:
        return RequestPrioritizerType.EDF

    def __post_init__(self):
        self._native_handle = EdfRequestPrioritizerConfig_C(
            self.deadline_multiplier,
            self.min_deadline,
        )


@frozen_dataclass
class LrsRequestPrioritizerConfig(BaseRequestPrioritizerConfig):
    deadline_multiplier: float = field(
        default=1.5,
        metadata={"help": "Deadline multiplier for LRS."},
    )
    min_deadline: float = field(
        default=0.5,
        metadata={"help": "Minimum deadline for LRS."},
    )

    @staticmethod
    def get_type() -> RequestPrioritizerType:
        return RequestPrioritizerType.LRS

    def __post_init__(self):
        self._native_handle = LrsRequestPrioritizerConfig_C(
            self.deadline_multiplier,
            self.min_deadline,
        )
