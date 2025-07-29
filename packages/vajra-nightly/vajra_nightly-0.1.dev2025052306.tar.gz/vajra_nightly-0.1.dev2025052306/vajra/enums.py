from enum import Enum

from vajra._native.enums import (
    MetricsStoreType,
    ReplicaControllerType,
    ReplicaSchedulerType,
    ReplicasetControllerType,
    ReplicasetSchedulerType,
    RequestPrioritizerType,
    TransferBackendType,
)


class RequestGeneratorType(Enum):
    SYNTHETIC = "SYNTHETIC"
    TRACE = "TRACE"


class RequestIntervalGeneratorType(Enum):
    POISSON = "POISSON"
    GAMMA = "GAMMA"
    STATIC = "STATIC"
    TRACE = "TRACE"


class RequestLengthGeneratorType(Enum):
    UNIFORM = "UNIFORM"
    ZIPF = "ZIPF"
    TRACE = "TRACE"
    FIXED = "FIXED"


__all__ = [
    "ReplicasetSchedulerType",
    "ReplicasetControllerType",
    "ReplicaControllerType",
    "ReplicaSchedulerType",
    "RequestPrioritizerType",
    "MetricsStoreType",
    "RequestGeneratorType",
    "RequestIntervalGeneratorType",
    "RequestLengthGeneratorType",
    "TransferBackendType",
]
