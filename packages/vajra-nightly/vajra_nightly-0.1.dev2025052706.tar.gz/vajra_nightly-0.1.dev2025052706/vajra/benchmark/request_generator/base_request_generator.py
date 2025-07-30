from abc import ABC, abstractmethod
from typing import Generic, List, TypeVar

from vajra.benchmark.config import BaseRequestGeneratorConfig
from vajra.benchmark.entities import Request

T = TypeVar("T", bound=BaseRequestGeneratorConfig)


class BaseRequestGenerator(ABC, Generic[T]):

    def __init__(self, config: T):
        self.config = config

    @abstractmethod
    def generate_requests(self) -> List[Request]:
        pass

    def generate(self) -> List[Request]:
        requests = self.generate_requests()
        return requests
