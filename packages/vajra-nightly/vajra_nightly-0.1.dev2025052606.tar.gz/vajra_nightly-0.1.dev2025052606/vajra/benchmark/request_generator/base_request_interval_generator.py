from abc import ABC, abstractmethod
from typing import Generic, Optional, TypeVar

from vajra.benchmark.config import BaseRequestIntervalGeneratorConfig

T = TypeVar("T", bound=BaseRequestIntervalGeneratorConfig)


class BaseRequestIntervalGenerator(ABC, Generic[T]):

    def __init__(self, config: T):
        self.config = config

    @abstractmethod
    def get_next_inter_request_time(self) -> Optional[float]:
        pass
