from abc import ABC, abstractmethod
from typing import Generic, Optional, Tuple, TypeVar

from vajra.benchmark.config import BaseRequestLengthGeneratorConfig

T = TypeVar("T", bound=BaseRequestLengthGeneratorConfig)


class BaseRequestLengthGenerator(ABC, Generic[T]):

    def __init__(self, config: T):
        self.config = config

    @abstractmethod
    def get_next_num_tokens(self) -> Tuple[Optional[float], Optional[float]]:
        pass
