import copy
import pickle

import pytest

from vajra.config import (
    CacheConfig,
    FixedChunkReplicaSchedulerConfig,
    LlmReplicaControllerConfig,
    LlmReplicasetControllerConfig,
    ModelConfig,
    ParallelConfig,
    PullReplicasetSchedulerConfig,
    WorkerConfig,
)
from vajra.enums import ReplicaControllerType


@pytest.mark.parametrize(
    "model_config, worker_config, cache_config, parallel_config, scheduler_config",
    [
        (
            ModelConfig(),
            WorkerConfig(),
            CacheConfig(),
            ParallelConfig(),
            FixedChunkReplicaSchedulerConfig(),
        ),
        (
            ModelConfig(),
            WorkerConfig(),
            CacheConfig(block_size=32),
            ParallelConfig(),
            FixedChunkReplicaSchedulerConfig(),
        ),
    ],
)
@pytest.mark.unit
def test_llm_replica_controller_config_creation(
    model_config,
    worker_config,
    cache_config,
    parallel_config,
    scheduler_config,
):
    """Tests creating valid LlmReplicaControllerConfig objects and accessing their properties."""
    config = LlmReplicaControllerConfig(
        model_config=model_config,
        worker_config=worker_config,
        cache_config=cache_config,
        parallel_config=parallel_config,
        scheduler_config=scheduler_config,
    )
    assert config.model_config == model_config
    assert config.worker_config == worker_config
    assert config.cache_config == cache_config
    assert config.parallel_config == parallel_config
    assert config.scheduler_config == scheduler_config

    assert config.native_handle is not None  # pyright: ignore

    assert config.get_type() == ReplicaControllerType.LLM_BASE


@pytest.mark.parametrize(
    "model_config, worker_config, cache_config, parallel_config, scheduler_config",
    [
        (
            ModelConfig(),
            WorkerConfig(),
            CacheConfig(),
            ParallelConfig(),
            FixedChunkReplicaSchedulerConfig(),
        ),
        (
            ModelConfig(),
            WorkerConfig(),
            CacheConfig(block_size=32),
            ParallelConfig(),
            FixedChunkReplicaSchedulerConfig(),
        ),
    ],
)
@pytest.mark.unit
def test_can_deep_copy_llm_replica_controller_config(
    model_config,
    worker_config,
    cache_config,
    parallel_config,
    scheduler_config,
):
    """Tests deep copying valid LlmReplicaControllerConfig objects and accessing their properties."""
    config = LlmReplicaControllerConfig(
        model_config=model_config,
        worker_config=worker_config,
        cache_config=cache_config,
        parallel_config=parallel_config,
        scheduler_config=scheduler_config,
    )

    config_deep_copy = copy.deepcopy(config)

    assert config.model_config == config_deep_copy.model_config
    assert config.worker_config == config_deep_copy.worker_config
    assert config.cache_config == config_deep_copy.cache_config
    assert config.parallel_config == config_deep_copy.parallel_config
    assert config.scheduler_config == config_deep_copy.scheduler_config
    assert config.scheduler_config.native_handle is not None
    assert config_deep_copy.scheduler_config.native_handle is not None
    assert (
        config.scheduler_config.native_handle.max_batch_size
        == config_deep_copy.scheduler_config.native_handle.max_batch_size
    )
    assert (
        config.scheduler_config.native_handle.max_chunk_size
        == config_deep_copy.scheduler_config.native_handle.max_chunk_size
    )
    assert (
        config.scheduler_config.native_handle.min_chunk_size
        == config_deep_copy.scheduler_config.native_handle.min_chunk_size
    )
    assert (
        config.scheduler_config.native_handle.target_batch_time
        == config_deep_copy.scheduler_config.native_handle.target_batch_time
    )

    assert config is not config_deep_copy


@pytest.mark.parametrize(
    "model_config, worker_config, cache_config, parallel_config, scheduler_config",
    [
        (
            ModelConfig(),
            WorkerConfig(),
            CacheConfig(),
            ParallelConfig(),
            FixedChunkReplicaSchedulerConfig(),
        ),
        (
            ModelConfig(),
            WorkerConfig(),
            CacheConfig(block_size=32),
            ParallelConfig(),
            FixedChunkReplicaSchedulerConfig(),
        ),
    ],
)
@pytest.mark.unit
def test_can_pickle_llm_replica_controller_config(
    model_config,
    worker_config,
    cache_config,
    parallel_config,
    scheduler_config,
):
    """Tests pickling LlmReplicaControllerConfig objects and accessing their properties."""
    config = LlmReplicaControllerConfig(
        model_config=model_config,
        worker_config=worker_config,
        cache_config=cache_config,
        parallel_config=parallel_config,
        scheduler_config=scheduler_config,
    )

    pickled_config = pickle.dumps(config)
    config_from_pickle = pickle.loads(pickled_config)

    assert config.model_config == config_from_pickle.model_config
    assert config.worker_config == config_from_pickle.worker_config
    assert config.cache_config == config_from_pickle.cache_config
    assert config.parallel_config == config_from_pickle.parallel_config
    assert config.scheduler_config == config_from_pickle.scheduler_config
    assert config.scheduler_config.native_handle is not None
    assert config_from_pickle.scheduler_config.native_handle is not None
    assert (
        config.scheduler_config.native_handle.max_batch_size
        == config_from_pickle.scheduler_config.native_handle.max_batch_size
    )
    assert (
        config.scheduler_config.native_handle.max_chunk_size
        == config_from_pickle.scheduler_config.native_handle.max_chunk_size
    )
    assert (
        config.scheduler_config.native_handle.min_chunk_size
        == config_from_pickle.scheduler_config.native_handle.min_chunk_size
    )
    assert (
        config.scheduler_config.native_handle.target_batch_time
        == config_from_pickle.scheduler_config.native_handle.target_batch_time
    )


@pytest.mark.parametrize(
    "num_replicas, num_tokenizer_workers",
    [(1, 5), (2, 10), (4, 20)],
)
@pytest.mark.unit
def test_llm_replicaset_controller_config_creation(num_replicas, num_tokenizer_workers):
    """Tests creating valid LlmReplicasetControllerConfig objects and accessing their properties."""
    cache_config = CacheConfig(block_size=32)
    model_config = ModelConfig()
    worker_config = WorkerConfig()
    parallel_config = ParallelConfig()

    replica_controller_config = LlmReplicaControllerConfig(
        model_config=model_config,
        worker_config=worker_config,
        cache_config=cache_config,
        parallel_config=parallel_config,
    )

    scheduler_config = PullReplicasetSchedulerConfig()

    replicaset_config = LlmReplicasetControllerConfig(
        num_replicas=num_replicas,
        replica_controller_config=replica_controller_config,
        replicaset_scheduler_config=scheduler_config,
        num_tokenizer_workers=num_tokenizer_workers,
    )

    assert replicaset_config.num_replicas == num_replicas
    assert replicaset_config.num_tokenizer_workers == num_tokenizer_workers

    native_handle = replicaset_config.native_handle  # pyright: ignore
    assert native_handle.num_replicas == num_replicas
    assert native_handle.num_tokenizer_workers == num_tokenizer_workers


@pytest.mark.parametrize(
    "num_replicas, num_tokenizer_workers",
    [(1, 5), (2, 10), (4, 20)],
)
@pytest.mark.unit
def test_can_deep_copy_llm_replicaset_controller_config(
    num_replicas, num_tokenizer_workers
):
    """Tests deep copying LlmReplicasetControllerConfig objects and accessing their properties."""
    # Create a custom replica controller config
    cache_config = CacheConfig(block_size=32)
    model_config = ModelConfig()
    worker_config = WorkerConfig()
    parallel_config = ParallelConfig()

    replica_controller_config = LlmReplicaControllerConfig(
        model_config=model_config,
        worker_config=worker_config,
        cache_config=cache_config,
        parallel_config=parallel_config,
    )

    scheduler_config = PullReplicasetSchedulerConfig()

    replicaset_config = LlmReplicasetControllerConfig(
        num_replicas=num_replicas,
        replica_controller_config=replica_controller_config,
        replicaset_scheduler_config=scheduler_config,
        num_tokenizer_workers=num_tokenizer_workers,
    )

    replicaset_config_deep_copy = copy.deepcopy(replicaset_config)

    assert replicaset_config_deep_copy.num_replicas == num_replicas
    assert replicaset_config_deep_copy.num_tokenizer_workers == num_tokenizer_workers

    assert replicaset_config_deep_copy is not replicaset_config
    assert (
        replicaset_config_deep_copy.replica_controller_config
        is not replicaset_config.replica_controller_config
    )
    assert (
        replicaset_config_deep_copy.replica_controller_config.cache_config
        is not replicaset_config.replica_controller_config.cache_config
    )


@pytest.mark.parametrize(
    "num_replicas, num_tokenizer_workers",
    [(1, 5), (2, 10), (4, 20)],
)
@pytest.mark.unit
def test_can_pickle_llm_replicaset_controller_config(
    num_replicas, num_tokenizer_workers
):
    """Tests pickling LlmReplicasetControllerConfig objects and accessing their properties."""
    cache_config = CacheConfig(block_size=32)
    model_config = ModelConfig()
    worker_config = WorkerConfig()
    parallel_config = ParallelConfig()

    replica_controller_config = LlmReplicaControllerConfig(
        model_config=model_config,
        worker_config=worker_config,
        cache_config=cache_config,
        parallel_config=parallel_config,
    )

    scheduler_config = PullReplicasetSchedulerConfig()

    replicaset_config = LlmReplicasetControllerConfig(
        num_replicas=num_replicas,
        replica_controller_config=replica_controller_config,
        replicaset_scheduler_config=scheduler_config,
        num_tokenizer_workers=num_tokenizer_workers,
    )

    pickled_config = pickle.dumps(replicaset_config)
    replicaset_config_from_pickle = pickle.loads(pickled_config)

    assert replicaset_config_from_pickle.num_replicas == num_replicas
    assert replicaset_config_from_pickle.num_tokenizer_workers == num_tokenizer_workers

    assert replicaset_config_from_pickle is not replicaset_config
    assert (
        replicaset_config_from_pickle.replica_controller_config
        is not replicaset_config.replica_controller_config
    )
