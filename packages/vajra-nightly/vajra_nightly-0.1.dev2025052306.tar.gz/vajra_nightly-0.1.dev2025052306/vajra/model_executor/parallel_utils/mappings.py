# Copyright 2023 The Vajra team.
# Adapted from https://github.com/NVIDIA/Megatron-LM/blob/main/megatron/core/tensor_parallel/mappings.py
# Copyright (c) 2022, NVIDIA CORPORATION. All rights reserved.

from typing import Tuple

import torch

from vajra.metrics_store import CudaTimer, MetricType
from vajra.model_executor.parallel_utils.parallel_state import (
    get_kv_parallel_group,
    get_kv_parallel_world_size,
    get_pipeline_model_parallel_group,
    get_pipeline_model_parallel_next_rank,
    get_pipeline_model_parallel_prev_rank,
    get_tensor_model_parallel_group,
    get_tensor_model_parallel_rank,
    get_tensor_model_parallel_world_size,
)

from .utils import split_tensor_along_last_dim


def reduce_from_kv_parallel_region(input_: torch.Tensor) -> torch.Tensor:
    """All-reduce the input tensor across model parallel group."""

    # Bypass the function if we are using only 1 GPU.
    if get_kv_parallel_world_size() == 1:
        return input_

    # All-reduce.
    torch.distributed.all_reduce(input_, group=get_kv_parallel_group())  # type: ignore

    return input_


def reduce_from_tensor_model_parallel_region(input_: torch.Tensor) -> torch.Tensor:
    """All-reduce the input tensor across model parallel group."""

    # Bypass the function if we are using only 1 GPU.
    if get_tensor_model_parallel_world_size() == 1:
        return input_

    # All-reduce.
    torch.distributed.all_reduce(input_, group=get_tensor_model_parallel_group())  # type: ignore

    return input_


def scatter_to_tensor_model_parallel_region(input_: torch.Tensor) -> torch.Tensor:
    """Split the tensor along its last dimension and keep the
    corresponding slice."""

    world_size = get_tensor_model_parallel_world_size()
    # Bypass the function if we are using only 1 GPU.
    if world_size == 1:
        return input_

    # Split along last dimension.
    input_list = split_tensor_along_last_dim(input_, world_size)

    # Note: torch.split does not create contiguous tensors by default.
    rank = get_tensor_model_parallel_rank()
    output = input_list[rank].contiguous()

    return output


def gather_from_group(
    input_: torch.Tensor,
    world_size: int,
    rank: int,
    concat_dim: int,
    group: torch.distributed.ProcessGroup,  # type: ignore
) -> torch.Tensor:
    # Bypass the function if we are using only 1 GPU.
    assert world_size > 1

    tensor_list = [torch.empty_like(input_) for _ in range(world_size)]
    tensor_list[rank] = input_

    torch.distributed.all_gather(tensor_list, input_, group=group)  # type: ignore

    # Note: torch.cat already creates a contiguous tensor.
    output = torch.cat(tensor_list, dim=concat_dim).contiguous()
    return output


def gather_from_tensor_model_parallel_region(input_: torch.Tensor) -> torch.Tensor:
    """Gather tensors and concatenate along the last dimension."""
    world_size = get_tensor_model_parallel_world_size()
    if world_size == 1:
        return input_

    last_dim = input_.dim() - 1
    rank = get_tensor_model_parallel_rank()
    group = get_tensor_model_parallel_group()

    return gather_from_group(input_, world_size, rank, last_dim, group)


def send_to_next_pipeline_stage(
    hidden_states: torch.Tensor, enable_chunked_pipeline_comm_opt: bool = True
) -> None:
    """Send hidden states to the next pipeline stage using partial async send + allgather.
    Instead of sending the full tensor, each rank sends only its partition
    to the next pipeline stage, followed by an allgather to reconstruct
    the full tensor.
    """
    assert get_pipeline_model_parallel_group().size() != 1

    tp_world_size = get_tensor_model_parallel_world_size()
    tp_rank = get_tensor_model_parallel_rank()
    next_rank = get_pipeline_model_parallel_next_rank()

    with CudaTimer(MetricType.NCCL_SEND):
        # Split tensor along last dim if optimization is enabled
        if enable_chunked_pipeline_comm_opt:
            tensor_chunks = split_tensor_along_last_dim(hidden_states, tp_world_size)
            # Send only this rank's chunk
            chunk_to_send = tensor_chunks[tp_rank].contiguous()
            torch.distributed.send(  # type: ignore
                tensor=chunk_to_send,
                dst=next_rank,
                group=get_pipeline_model_parallel_group(),
            )
        else:
            # No splitting needed if optimization disabled
            torch.distributed.send(  # type: ignore
                tensor=hidden_states,
                dst=next_rank,
                group=get_pipeline_model_parallel_group(),
            )


def recv_from_last_pipeline_stage(
    recv_size: Tuple[int, ...],
    dtype: torch.dtype,
    device: torch.device,
    enable_chunked_pipeline_comm_opt: bool = True,
) -> torch.Tensor:
    """Receive hidden states from previous pipeline stage"""
    assert get_pipeline_model_parallel_group().size() != 1

    tp_world_size = get_tensor_model_parallel_world_size()
    prev_rank = get_pipeline_model_parallel_prev_rank()

    with CudaTimer(MetricType.NCCL_RECV):
        if enable_chunked_pipeline_comm_opt:
            # Calculate chunk size
            chunk_size = recv_size[-1] // tp_world_size

            # Create shape tuple for the chunk tensor
            chunk_shape = recv_size[:-1] + (chunk_size,)

            # Receive this rank's chunk
            chunk = torch.empty(size=chunk_shape, dtype=dtype, device=device)
            torch.distributed.recv(  # type: ignore
                tensor=chunk,
                src=prev_rank,
                group=get_pipeline_model_parallel_group(),
            )
            output_tensor = gather_from_tensor_model_parallel_region(chunk)
            return output_tensor
        else:
            # Fallback: receive full tensor
            output_tensor = torch.empty(size=recv_size, dtype=dtype, device=device)

            torch.distributed.recv(  # type: ignore
                tensor=output_tensor,
                src=prev_rank,
                group=get_pipeline_model_parallel_group(),
            )

            return output_tensor
