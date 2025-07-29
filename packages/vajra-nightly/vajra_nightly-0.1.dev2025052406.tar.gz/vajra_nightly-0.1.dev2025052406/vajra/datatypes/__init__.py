from typing import Dict, List, Tuple

from vajra._native.datatypes import (
    BaseSequenceWithPriority,
    CommInfo,
    LogicalTokenBlock,
    PendingStepOutput,
    RequestOutput,
    SamplerOutput,
    SamplingParams,
    SamplingType,
    SchedulerOutput,
    Sequence,
    SequenceMetadata,
    SequenceParams,
    SequenceScheduleMetadata,
    SequenceState,
    SequenceStatus,
    StepInputs,
    StepMicrobatchOutputs,
    StepOutputs,
    UserSequenceParams,
)

GPULocation = Tuple[str, int]  # (node_ip, gpu_id)
ResourceMapping = List[GPULocation]
GlobalResourceMapping = Dict[str, ResourceMapping]

SamplerOutputs = List[SamplerOutput]
ModelParallelRank = Tuple[int, int, int]


__all__ = [
    "LogicalTokenBlock",
    "CommInfo",
    "RequestOutput",
    "SamplerOutput",
    "SamplerOutputs",
    "SamplingParams",
    "SchedulerOutput",
    "SequenceScheduleMetadata",
    "SequenceState",
    "SequenceStatus",
    "Sequence",
    "BaseSequenceWithPriority",
    "StepInputs",
    "StepMicrobatchOutputs",
    "StepOutputs",
    "SamplingType",
    "GPULocation",
    "ResourceMapping",
    "GlobalResourceMapping",
    "SequenceMetadata",
    "SequenceParams",
    "UserSequenceParams",
    "ModelParallelRank",
    "SamplerOutputs",
    "StepOutputs",
    "StepMicrobatchOutputs",
    "StepInputs",
    "CommInfo",
    "PendingStepOutput",
]
