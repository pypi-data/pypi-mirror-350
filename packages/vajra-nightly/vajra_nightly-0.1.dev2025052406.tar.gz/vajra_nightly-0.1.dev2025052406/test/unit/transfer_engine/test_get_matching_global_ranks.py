import pytest
import torch.distributed

from vajra._native.configs import ReplicaResourceConfig, TransferEngineConfig
from vajra._native.enums import TransferBackendType, TransferOperationRanksType
from vajra._native.transfer_engine.interface import BaseTransferEngine
from vajra.config import ModelConfig, ParallelConfig


@pytest.fixture(scope="module")
def model_config():
    model_config = ModelConfig(
        model="meta-llama/Meta-Llama-3-8B", override_num_layers=12
    )
    return model_config


def create_parallel_config(pipeline_parallel_size, tensor_parallel_size):
    parallel_config = ParallelConfig(
        pipeline_parallel_size=pipeline_parallel_size,
        tensor_parallel_size=tensor_parallel_size,
        kv_parallel_size=1,
        enable_sequence_pipeline_parallel=False,
        enable_chunked_pipeline_comm_opt=False,
    )
    return parallel_config


def create_replica_resource_config(parallel_config, model_config):
    return ReplicaResourceConfig(
        parallel_config.native_handle, model_config.native_handle
    )


def create_transfer_engine(
    transfer_backend_type, global_rank, replica_resource_mapping
):
    transfer_engine_config = TransferEngineConfig(
        transfer_backend_type,
        global_rank,
        replica_resource_mapping,
        torch.distributed.group.WORLD,
    )
    transfer_engine = BaseTransferEngine.create_from(transfer_engine_config)
    return transfer_engine


@pytest.mark.parametrize(
    "global_rank, current_tp_size, current_pp_size, other_tp_size, other_pp_size, num_layers, layer_id, expected_ranks",
    [
        # tp 1 -> tp 1
        (0, 1, 1, 1, 1, 12, 0, [1]),
        # tp 4 -> tp 1
        (0, 4, 1, 1, 1, 12, 0, [4]),
        (1, 4, 1, 1, 1, 12, 0, [4]),
        (2, 4, 1, 1, 1, 12, 0, [4]),
        (3, 4, 1, 1, 1, 12, 0, [4]),
        # tp 8 -> tp 1
        (4, 8, 1, 1, 1, 12, 0, [8]),
        (6, 8, 1, 1, 1, 12, 0, [8]),
        (6, 8, 1, 1, 1, 12, 0, [8]),
        # tp 2 -> tp 2
        (0, 2, 1, 2, 1, 12, 0, [2]),
        (1, 2, 1, 2, 1, 12, 0, [3]),
        # tp 4 -> tp 2
        (0, 4, 1, 2, 1, 12, 0, [4]),
        (1, 4, 1, 2, 1, 12, 0, [4]),
        (2, 4, 1, 2, 1, 12, 0, [5]),
        (3, 4, 1, 2, 1, 12, 0, [5]),
        # tp 8 -> tp 2
        (0, 8, 1, 2, 1, 12, 0, [8]),
        (1, 8, 1, 2, 1, 12, 0, [8]),
        (2, 8, 1, 2, 1, 12, 0, [8]),
        (3, 8, 1, 2, 1, 12, 0, [8]),
        (4, 8, 1, 2, 1, 12, 0, [9]),
        (5, 8, 1, 2, 1, 12, 0, [9]),
        (6, 8, 1, 2, 1, 12, 0, [9]),
        (7, 8, 1, 2, 1, 12, 0, [9]),
        # tp 1 -> tp 2
        (0, 1, 1, 2, 1, 12, 0, [1, 2]),
        # tp 1 -> tp 4
        (0, 1, 1, 4, 1, 12, 0, [1, 2, 3, 4]),
        # tp 2 -> tp 4
        (0, 2, 1, 4, 1, 12, 0, [2, 3]),
        (1, 2, 1, 4, 1, 12, 0, [4, 5]),
        # tp 2 -> tp 8
        (0, 2, 1, 8, 1, 12, 0, [2, 3, 4, 5]),
        (1, 2, 1, 8, 1, 12, 0, [6, 7, 8, 9]),
        # tp 1 pp 2 -> tp 1 pp 2
        (0, 1, 2, 1, 2, 12, 0, [2]),
        (0, 1, 2, 1, 2, 12, 5, [2]),
        (1, 1, 2, 1, 2, 12, 6, [3]),
        (1, 1, 2, 1, 2, 12, 11, [3]),
        # tp 1 pp 4 -> tp 1 pp 4
        (0, 1, 4, 1, 4, 12, 0, [4]),
        (1, 1, 4, 1, 4, 12, 5, [5]),
        (2, 1, 4, 1, 4, 12, 6, [6]),
        (3, 1, 4, 1, 4, 12, 11, [7]),
        # tp 2 -> tp 8 pp 2
        (0, 2, 1, 8, 2, 12, 0, [2, 3, 4, 5]),
        (1, 2, 1, 8, 2, 12, 0, [6, 7, 8, 9]),
        (1, 2, 1, 8, 2, 12, 2, [6, 7, 8, 9]),
        (0, 2, 1, 8, 2, 12, 8, [10, 11, 12, 13]),
        (1, 2, 1, 8, 2, 12, 9, [14, 15, 16, 17]),
        # tp 2 pp 2 -> tp 8 pp 2
        (0, 2, 2, 8, 2, 12, 0, [4, 5, 6, 7]),
        (1, 2, 2, 8, 2, 12, 0, [8, 9, 10, 11]),
        (2, 2, 2, 8, 2, 12, 6, [12, 13, 14, 15]),
        # tp 2 pp 4 -> tp 8 pp 2
        (7, 2, 4, 8, 2, 12, 10, [20, 21, 22, 23]),
        (4, 2, 4, 8, 2, 12, 8, [16, 17, 18, 19]),
        (5, 2, 4, 8, 2, 12, 8, [20, 21, 22, 23]),
    ],
)
@pytest.mark.unit
def test_get_matching_other_global_ranks_parameterized(
    model_config,
    global_rank,
    current_tp_size,
    current_pp_size,
    other_tp_size,
    other_pp_size,
    num_layers,
    layer_id,
    expected_ranks,
):
    """Tests get_matching_other_global_ranks with various TP and PP configurations, mocking distributed. All calls are from replica 0 to 1."""

    current_parallel_config = create_parallel_config(current_pp_size, current_tp_size)
    other_parallel_config = create_parallel_config(other_pp_size, other_tp_size)

    current_replica_config = create_replica_resource_config(
        current_parallel_config, model_config
    )
    other_replica_config = create_replica_resource_config(
        other_parallel_config, model_config
    )

    replica_resource_mapping = [current_replica_config, other_replica_config]

    transfer_engine = create_transfer_engine(
        TransferBackendType.TORCH, global_rank, replica_resource_mapping
    )

    actual_ranks = transfer_engine.get_matching_other_global_ranks(1, layer_id)

    assert actual_ranks == expected_ranks


@pytest.mark.parametrize(
    "global_rank, other_replica_id, world_size",
    [
        (1, 0, 8),
        (2, 0, 8),
        (3, 0, 8),
        (4, 0, 8),
        (5, 0, 8),
        (6, 0, 8),
        (7, 0, 8),
        (7, 3, 8),
        (6, 3, 8),
        (5, 3, 8),
        (4, 3, 8),
        (2, 3, 8),
        (1, 3, 8),
        (0, 3, 8),
        (0, 7, 8),
        (7, 0, 8),
        (7, 6, 8),
        (7, 1, 8),
    ],
)
@pytest.mark.unit
def test_get_matching_other_global_ranks_many_replicas(
    model_config, global_rank, other_replica_id, world_size
):
    """Tests get_matching_other_global_ranks, mocking distributed. All calls use replica size = 1 to just test the global offset across many replicas."""

    replica_resource_mapping = []
    for _ in range(world_size):
        parallel_config = create_parallel_config(1, 1)
        replica_resource_config = create_replica_resource_config(
            parallel_config, model_config
        )
        replica_resource_mapping.append(replica_resource_config)

    transfer_engine = create_transfer_engine(
        TransferBackendType.TORCH, global_rank, replica_resource_mapping
    )

    actual_ranks = transfer_engine.get_matching_other_global_ranks(other_replica_id, 0)

    assert actual_ranks == [other_replica_id]


@pytest.mark.parametrize(
    "other_tp_degree, other_pp_degree, layer_id, transfer_operation_ranks_type, expected_ranks",
    [
        (1, 1, 1, TransferOperationRanksType.ALL, [1]),
        (1, 1, 1, TransferOperationRanksType.SINGLE, [1]),
        (1, 4, 9, TransferOperationRanksType.ALL, [1, 2, 3, 4]),
        (2, 4, 9, TransferOperationRanksType.ALL, [1, 2, 3, 4, 5, 6, 7, 8]),
        (4, 1, 9, TransferOperationRanksType.ALL, [1, 2, 3, 4]),
        (4, 1, 9, TransferOperationRanksType.SINGLE, [1]),
        (1, 4, 10, TransferOperationRanksType.SINGLE, [1]),
        (1, 4, 5, TransferOperationRanksType.SINGLE, [1]),
        (2, 4, 0, TransferOperationRanksType.SINGLE, [1]),
        (2, 4, 7, TransferOperationRanksType.SINGLE, [1]),
    ],
)
@pytest.mark.unit
def test_get_all_or_single_other_global_ranks(
    model_config,
    other_tp_degree,
    other_pp_degree,
    layer_id,
    transfer_operation_ranks_type,
    expected_ranks,
):
    """Tests get_matching_other_global_ranks, to get all the global ranks from another replica id or a single one,
    the first tp degree in the last pp layer."""

    replica_resource_mapping = []
    parallel_config = create_parallel_config(1, 1)
    replica_resource_config = create_replica_resource_config(
        parallel_config, model_config
    )
    replica_resource_mapping.append(replica_resource_config)
    other_parallel_config = create_parallel_config(other_pp_degree, other_tp_degree)
    other_replica_resource_config = create_replica_resource_config(
        other_parallel_config, model_config
    )
    replica_resource_mapping.append(other_replica_resource_config)

    transfer_engine = create_transfer_engine(
        TransferBackendType.TORCH, 0, replica_resource_mapping
    )

    actual_ranks = transfer_engine.get_matching_other_global_ranks(
        1, layer_id, transfer_operation_ranks_type
    )

    assert actual_ranks == expected_ranks
