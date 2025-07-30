from abc import ABC, abstractmethod
from typing import List, Optional, Tuple

import torch
import torch.distributed

from vajra.config import LlmReplicaControllerConfig
from vajra.datatypes import SamplerOutputs, Sequence, SequenceMetadata


class BaseModelRunner(ABC):
    def __init__(
        self,
        config: LlmReplicaControllerConfig,
        device: torch.device,
        rank: int,
    ) -> None:
        """Get the relevant model and load the weights and put on the GPU.
        This will generally rely on the model_loader for this.

        We also setup the sampler and the AttentionWrapper (or equivalent) here.
        """

    @abstractmethod
    def _prepare_inputs(
        self,
        seqs: List[Sequence],
        seq_metadata_list: List[SequenceMetadata],
    ) -> Tuple[torch.Tensor, ...]:
        """Convert the seq_metadata_list into the relevant tensors for the model.
        Depending on the model and the content of the Sequence class, this function
        may perform different types of preprocessing.
        The output of the function is a tuple of tensors that will be fed to the model forward
        We can return a variable number of torch.Tensor objects depending on the specific model
        TODO(ksukrit): Figure out required modifications to the Sequence class and return object
        """

    @abstractmethod
    def run(
        self,
        seqs: List[Sequence],
        seq_metadata_list: List[SequenceMetadata],
        gpu_cache: Optional[List[torch.Tensor]] = None,
    ) -> Optional[SamplerOutputs]:
        """Execute the model forward and return the outputs.
        TODO(ksukrit): Figure out a standard return type for this function.
        """
