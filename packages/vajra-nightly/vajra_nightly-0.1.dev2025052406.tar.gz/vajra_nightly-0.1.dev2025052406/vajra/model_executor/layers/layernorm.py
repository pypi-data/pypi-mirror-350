"""Custom normalization layers."""

from typing import Optional

import torch
import torch.nn as nn

from vajra._kernels import rms_norm
from vajra._native.model_executor.layers import RMSNorm as RMSNormC
from vajra.metrics_store import CudaTimer, MetricType
from vajra.model_executor.utils import use_native_backend


class RMSNorm(nn.Module):
    """Root mean square normalization.

    Computes x -> w * x / sqrt(E[x^2] + eps) where w is the learned weight.
    Refer to https://arxiv.org/abs/1910.07467
    """

    def __init__(
        self,
        hidden_size: int,
        eps: float = 1e-6,
        norm_op_name: Optional[MetricType] = None,
        layer_id: Optional[int] = None,
        use_native_execution_backend: Optional[bool] = False,
    ) -> None:
        super().__init__()
        self.weight = nn.Parameter(torch.ones(hidden_size))
        self.variance_epsilon = eps
        self.use_native_execution_backend = use_native_execution_backend

        self._norm_timer = CudaTimer(norm_op_name, layer_id=layer_id)

        if use_native_execution_backend:
            self.native_handle = RMSNormC(self.weight, eps)

    @use_native_backend
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        with self._norm_timer:
            out = torch.empty_like(x)
            rms_norm(
                out,
                x,
                self.weight.data,
                self.variance_epsilon,
            )
            return out
