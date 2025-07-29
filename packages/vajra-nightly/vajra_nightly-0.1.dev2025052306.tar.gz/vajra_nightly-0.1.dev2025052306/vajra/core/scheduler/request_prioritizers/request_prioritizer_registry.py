from vajra.enums import RequestPrioritizerType
from vajra.utils.base_registry import BaseRegistry

from .edf_request_prioritizer import EdfRequestPrioritizer
from .fcfs_request_prioritizer import FcfsRequestPrioritizer
from .lrs_request_prioritizer import LrsRequestPrioritizer


class RequestPrioritizerRegistry(BaseRegistry):
    pass


RequestPrioritizerRegistry.register(RequestPrioritizerType.FCFS, FcfsRequestPrioritizer)
RequestPrioritizerRegistry.register(RequestPrioritizerType.EDF, EdfRequestPrioritizer)
RequestPrioritizerRegistry.register(RequestPrioritizerType.LRS, LrsRequestPrioritizer)
