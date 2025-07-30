import copy
import pickle
from typing import Any, cast

import pytest

from vajra.config import (
    DynamicChunkReplicaSchedulerConfig,
    FixedChunkReplicaSchedulerConfig,
    SpaceSharingReplicaSchedulerConfig,
)
from vajra.enums import ReplicaSchedulerType

EPSILON = 1e-5


# Fixed Chunk Replica Scheduler Config Tests
@pytest.mark.parametrize(
    "max_batch_size, chunk_size",
    [(64, 1024), (128, 2048), (256, 4096)],
)
@pytest.mark.unit
def test_valid_fixed_chunk_config_creation(max_batch_size, chunk_size):
    """Tests creating valid FixedChunkReplicaSchedulerConfig objects and accessing their properties."""
    config = FixedChunkReplicaSchedulerConfig(
        max_batch_size=max_batch_size, chunk_size=chunk_size
    )
    config_c = cast(Any, config.native_handle)
    assert config.max_batch_size == config_c.max_batch_size
    assert config.min_chunk_size == config_c.min_chunk_size
    assert config.max_chunk_size == chunk_size
    assert config.get_type() == ReplicaSchedulerType.FIXED_CHUNK


@pytest.mark.parametrize(
    "max_batch_size, chunk_size",
    [(64, 1024), (128, 2048), (256, 4096)],
)
@pytest.mark.unit
def test_can_deep_copy_fixed_chunk_config(max_batch_size, chunk_size):
    """Tests deep copying valid FixedChunkReplicaSchedulerConfig objects and accessing their properties."""
    config = FixedChunkReplicaSchedulerConfig(
        max_batch_size=max_batch_size, chunk_size=chunk_size
    )
    config_deep_copy = copy.deepcopy(config)
    assert config.max_batch_size == config_deep_copy.max_batch_size
    assert config.chunk_size == config_deep_copy.chunk_size
    assert config.max_chunk_size == config_deep_copy.max_chunk_size


@pytest.mark.parametrize(
    "max_batch_size, chunk_size",
    [(64, 1024), (128, 2048), (256, 4096)],
)
@pytest.mark.unit
def test_can_pickle_fixed_chunk_config(max_batch_size, chunk_size):
    """Tests pickling FixedChunkReplicaSchedulerConfig objects and accessing their properties."""
    config = FixedChunkReplicaSchedulerConfig(
        max_batch_size=max_batch_size, chunk_size=chunk_size
    )
    pickled_config = pickle.dumps(config)
    config_from_pickle = pickle.loads(pickled_config)
    assert config.max_batch_size == config_from_pickle.max_batch_size
    assert config.chunk_size == config_from_pickle.chunk_size
    assert config.max_chunk_size == config_from_pickle.max_chunk_size


# Dynamic Chunk Replica Scheduler Config Tests
@pytest.mark.parametrize(
    "max_batch_size, max_chunk_size, min_chunk_size, target_batch_time",
    [
        (64, 4096, 16, 0.04),
        (128, 8192, 32, 0.05),
        (256, 16384, 64, 0.06),
    ],
)
@pytest.mark.unit
def test_valid_dynamic_chunk_config_creation(
    max_batch_size, max_chunk_size, min_chunk_size, target_batch_time
):
    """Tests creating valid DynamicChunkReplicaSchedulerConfig objects and accessing their properties."""
    config = DynamicChunkReplicaSchedulerConfig(
        max_batch_size=max_batch_size,
        max_chunk_size_param=max_chunk_size,
        min_chunk_size_param=min_chunk_size,
        target_batch_time_param=target_batch_time,
    )
    config_c = cast(Any, config.native_handle)
    assert config.max_batch_size == config_c.max_batch_size
    assert config.max_chunk_size == config_c.max_chunk_size
    assert config.min_chunk_size == config_c.min_chunk_size
    assert abs(config.target_batch_time - config_c.target_batch_time) < EPSILON
    assert config.max_chunk_size == max_chunk_size
    assert config.get_type() == ReplicaSchedulerType.DYNAMIC_CHUNK


@pytest.mark.parametrize(
    "max_batch_size, max_chunk_size, min_chunk_size, target_batch_time",
    [
        (64, 4096, 16, 0.04),
        (128, 8192, 32, 0.05),
        (256, 16384, 64, 0.06),
    ],
)
@pytest.mark.unit
def test_can_deep_copy_dynamic_chunk_config(
    max_batch_size, max_chunk_size, min_chunk_size, target_batch_time
):
    """Tests deep copying valid DynamicChunkReplicaSchedulerConfig objects and accessing their properties."""
    config = DynamicChunkReplicaSchedulerConfig(
        max_batch_size=max_batch_size,
        max_chunk_size_param=max_chunk_size,
        min_chunk_size_param=min_chunk_size,
        target_batch_time_param=target_batch_time,
    )
    config_deep_copy = copy.deepcopy(config)
    assert config.max_batch_size == config_deep_copy.max_batch_size
    assert config.max_chunk_size == config_deep_copy.max_chunk_size
    assert config.min_chunk_size == config_deep_copy.min_chunk_size
    assert abs(config.target_batch_time - config_deep_copy.target_batch_time) < EPSILON
    assert config.max_chunk_size == config_deep_copy.max_chunk_size


@pytest.mark.parametrize(
    "max_batch_size, max_chunk_size, min_chunk_size, target_batch_time",
    [
        (64, 4096, 16, 0.04),
        (128, 8192, 32, 0.05),
        (256, 16384, 64, 0.06),
    ],
)
@pytest.mark.unit
def test_can_pickle_dynamic_chunk_config(
    max_batch_size, max_chunk_size, min_chunk_size, target_batch_time
):
    """Tests pickling DynamicChunkReplicaSchedulerConfig objects and accessing their properties."""
    config = DynamicChunkReplicaSchedulerConfig(
        max_batch_size=max_batch_size,
        max_chunk_size_param=max_chunk_size,
        min_chunk_size_param=min_chunk_size,
        target_batch_time_param=target_batch_time,
    )
    pickled_config = pickle.dumps(config)
    config_from_pickle = pickle.loads(pickled_config)
    assert config.max_batch_size == config_from_pickle.max_batch_size
    assert config.max_chunk_size == config_from_pickle.max_chunk_size
    assert config.min_chunk_size == config_from_pickle.min_chunk_size
    assert (
        abs(config.target_batch_time - config_from_pickle.target_batch_time) < EPSILON
    )
    assert config.max_chunk_size == config_from_pickle.max_chunk_size


# Space Sharing Replica Scheduler Config Tests
@pytest.mark.parametrize(
    "max_batch_size, max_chunk_size, min_chunk_size, target_batch_time",
    [
        (64, 4096, 16, 0.04),
        (128, 8192, 32, 0.05),
        (256, 16384, 64, 0.06),
    ],
)
@pytest.mark.unit
def test_valid_space_sharing_config_creation(
    max_batch_size,
    max_chunk_size,
    min_chunk_size,
    target_batch_time,
):
    """Tests creating valid SpaceSharingReplicaSchedulerConfig objects and accessing their properties."""
    config = SpaceSharingReplicaSchedulerConfig(
        max_batch_size=max_batch_size,
        max_chunk_size_param=max_chunk_size,
        min_chunk_size_param=min_chunk_size,
        target_batch_time_param=target_batch_time,
    )
    config_c = cast(Any, config.native_handle)
    assert config.max_batch_size == config_c.max_batch_size
    assert config.max_chunk_size == config_c.max_chunk_size
    assert config.min_chunk_size == config_c.min_chunk_size
    assert abs(config.target_batch_time - config_c.target_batch_time) < EPSILON
    assert config.max_chunk_size == max_chunk_size
    assert config.get_type() == ReplicaSchedulerType.SPACE_SHARING


@pytest.mark.parametrize(
    "max_batch_size, max_chunk_size, min_chunk_size, target_batch_time",
    [
        (64, 4096, 16, 0.04),
        (128, 8192, 32, 0.05),
        (256, 16384, 64, 0.06),
    ],
)
@pytest.mark.unit
def test_can_deep_copy_space_sharing_config(
    max_batch_size,
    max_chunk_size,
    min_chunk_size,
    target_batch_time,
):
    """Tests deep copying valid SpaceSharingReplicaSchedulerConfig objects and accessing their properties."""
    config = SpaceSharingReplicaSchedulerConfig(
        max_batch_size=max_batch_size,
        max_chunk_size_param=max_chunk_size,
        min_chunk_size_param=min_chunk_size,
        target_batch_time_param=target_batch_time,
    )
    config_deep_copy = copy.deepcopy(config)
    assert config.max_batch_size == config_deep_copy.max_batch_size
    assert config.max_chunk_size == config_deep_copy.max_chunk_size
    assert config.min_chunk_size == config_deep_copy.min_chunk_size
    assert abs(config.target_batch_time - config_deep_copy.target_batch_time) < EPSILON
    assert config.max_chunk_size == config_deep_copy.max_chunk_size


@pytest.mark.parametrize(
    "max_batch_size, max_chunk_size, min_chunk_size, target_batch_time",
    [
        (64, 4096, 16, 0.04),
        (128, 8192, 32, 0.05),
        (256, 16384, 64, 0.06),
    ],
)
@pytest.mark.unit
def test_can_pickle_space_sharing_config(
    max_batch_size,
    max_chunk_size,
    min_chunk_size,
    target_batch_time,
):
    """Tests pickling SpaceSharingReplicaSchedulerConfig objects and accessing their properties."""
    config = SpaceSharingReplicaSchedulerConfig(
        max_batch_size=max_batch_size,
        max_chunk_size_param=max_chunk_size,
        min_chunk_size_param=min_chunk_size,
        target_batch_time_param=target_batch_time,
    )
    pickled_config = pickle.dumps(config)
    config_from_pickle = pickle.loads(pickled_config)
    assert config.max_batch_size == config_from_pickle.max_batch_size
    assert config.max_chunk_size == config_from_pickle.max_chunk_size
    assert config.min_chunk_size == config_from_pickle.min_chunk_size
    assert (
        abs(config.target_batch_time - config_from_pickle.target_batch_time) < EPSILON
    )
    assert config.max_chunk_size == config_from_pickle.max_chunk_size


# Additional Space Sharing Replica Scheduler Config Tests
@pytest.mark.parametrize(
    "max_batch_size, max_chunk_size, min_chunk_size, target_batch_time",
    [
        (64, 4096, 16, 0.04),
        (128, 8192, 32, 0.05),
        (256, 16384, 64, 0.06),
    ],
)
@pytest.mark.unit
def test_valid_space_sharing_config_additional(
    max_batch_size,
    max_chunk_size,
    min_chunk_size,
    target_batch_time,
):
    """Tests creating valid SpaceSharingReplicaSchedulerConfig objects and accessing their properties."""
    config = SpaceSharingReplicaSchedulerConfig(
        max_batch_size=max_batch_size,
        max_chunk_size_param=max_chunk_size,
        min_chunk_size_param=min_chunk_size,
        target_batch_time_param=target_batch_time,
    )
    config_c = cast(Any, config.native_handle)
    assert config.max_batch_size == config_c.max_batch_size
    assert config.max_chunk_size == config_c.max_chunk_size
    assert config.min_chunk_size == config_c.min_chunk_size
    assert abs(config.target_batch_time - config_c.target_batch_time) < EPSILON
    assert config.max_chunk_size == max_chunk_size
    assert config.get_type() == ReplicaSchedulerType.SPACE_SHARING


@pytest.mark.parametrize(
    "max_batch_size, max_chunk_size, min_chunk_size, target_batch_time",
    [
        (64, 4096, 16, 0.04),
        (128, 8192, 32, 0.05),
        (256, 16384, 64, 0.06),
    ],
)
@pytest.mark.unit
def test_can_deep_copy_space_sharing_config_additional(
    max_batch_size,
    max_chunk_size,
    min_chunk_size,
    target_batch_time,
):
    """Tests deep copying valid SpaceSharingReplicaSchedulerConfig objects and accessing their properties."""
    config = SpaceSharingReplicaSchedulerConfig(
        max_batch_size=max_batch_size,
        max_chunk_size_param=max_chunk_size,
        min_chunk_size_param=min_chunk_size,
        target_batch_time_param=target_batch_time,
    )
    config_deep_copy = copy.deepcopy(config)
    assert config.max_batch_size == config_deep_copy.max_batch_size
    assert config.max_chunk_size == config_deep_copy.max_chunk_size
    assert config.min_chunk_size == config_deep_copy.min_chunk_size
    assert abs(config.target_batch_time - config_deep_copy.target_batch_time) < EPSILON
    assert config.max_chunk_size == config_deep_copy.max_chunk_size


@pytest.mark.parametrize(
    "max_batch_size, max_chunk_size, min_chunk_size, target_batch_time",
    [
        (64, 4096, 16, 0.04),
        (128, 8192, 32, 0.05),
        (256, 16384, 64, 0.06),
    ],
)
@pytest.mark.unit
def test_can_pickle_space_sharing_config_additional(
    max_batch_size,
    max_chunk_size,
    min_chunk_size,
    target_batch_time,
):
    """Tests pickling SpaceSharingReplicaSchedulerConfig objects and accessing their properties."""
    config = SpaceSharingReplicaSchedulerConfig(
        max_batch_size=max_batch_size,
        max_chunk_size_param=max_chunk_size,
        min_chunk_size_param=min_chunk_size,
        target_batch_time_param=target_batch_time,
    )
    pickled_config = pickle.dumps(config)
    config_from_pickle = pickle.loads(pickled_config)
    assert config.max_batch_size == config_from_pickle.max_batch_size
    assert config.max_chunk_size == config_from_pickle.max_chunk_size
    assert config.min_chunk_size == config_from_pickle.min_chunk_size
    assert (
        abs(config.target_batch_time - config_from_pickle.target_batch_time) < EPSILON
    )
    assert config.max_chunk_size == config_from_pickle.max_chunk_size
