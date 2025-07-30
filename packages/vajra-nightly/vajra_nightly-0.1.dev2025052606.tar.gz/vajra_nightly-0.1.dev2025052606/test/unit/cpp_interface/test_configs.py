import copy
import pickle

import pytest

from vajra._native.configs import ReplicaResourceConfig
from vajra.config import (
    CacheConfig,
    MetricsConfig,
    ModelConfig,
    ParallelConfig,
    WorkerConfig,
)


@pytest.mark.parametrize(
    "model, num_layers",
    [("meta-llama/Meta-Llama-3-8B", 12), ("meta-llama/Meta-Llama-3-70B", 24)],
)
@pytest.mark.unit
def test_valid_model_config_creation(model, num_layers):
    """Tests creating valid ModelConfig objects and accessing their properties."""
    model_config = ModelConfig(model=model, override_num_layers=num_layers)
    model_config_c = model_config.native_handle
    assert model_config.model == model_config_c.model


@pytest.mark.parametrize(
    "tensor_parallel_size, pipeline_parallel_size, kv_parallel_size",
    [(1, 1, 1), (4, 2, 1)],
)
@pytest.mark.unit
def test_valid_parallel_config_creation(
    tensor_parallel_size, pipeline_parallel_size, kv_parallel_size
):
    """Tests creating valid ParallelConfig objects and accessing their properties."""
    parallel_config = ParallelConfig(
        pipeline_parallel_size=pipeline_parallel_size,
        tensor_parallel_size=tensor_parallel_size,
        kv_parallel_size=kv_parallel_size,
        enable_sequence_pipeline_parallel=True,
    )
    parallel_config_c = parallel_config.native_handle
    assert pipeline_parallel_size == parallel_config_c.pipeline_parallel_size
    assert tensor_parallel_size == parallel_config_c.tensor_parallel_size
    assert kv_parallel_size == parallel_config_c.kv_parallel_size


@pytest.mark.parametrize(
    "model, num_layers, tensor_parallel_size, pipeline_parallel_size, kv_parallel_size",
    [
        ("meta-llama/Meta-Llama-3-8B", 12, 1, 1, 1),
        ("meta-llama/Meta-Llama-3-70B", 24, 4, 2, 1),
    ],
)
@pytest.mark.unit
def test_valid_replica_parallel_config_creation(
    model,
    num_layers,
    tensor_parallel_size,
    pipeline_parallel_size,
    kv_parallel_size,
):
    """Tests creating valid ReplicaResourceConfig objects and accessing their properties."""
    parallel_config = ParallelConfig(
        pipeline_parallel_size=pipeline_parallel_size,
        tensor_parallel_size=tensor_parallel_size,
        kv_parallel_size=kv_parallel_size,
        enable_sequence_pipeline_parallel=True,
    )
    model_config = ModelConfig(model=model, override_num_layers=num_layers)
    model_config_c = model_config.native_handle
    parallel_config_c = parallel_config.native_handle

    replica_parallel_config = ReplicaResourceConfig(parallel_config_c, model_config_c)
    assert pipeline_parallel_size == replica_parallel_config.pipeline_parallel_size
    assert tensor_parallel_size == replica_parallel_config.tensor_parallel_size
    assert kv_parallel_size == replica_parallel_config.kv_parallel_size
    assert parallel_config.world_size == replica_parallel_config.world_size
    assert num_layers == replica_parallel_config.total_num_layers
    assert (
        num_layers / pipeline_parallel_size == replica_parallel_config.local_num_layers
    )


@pytest.mark.parametrize(
    "tensor_parallel_size, pipeline_parallel_size, kv_parallel_size",
    [(1, 1, 1), (4, 2, 1)],
)
@pytest.mark.unit
def test_can_deep_copy_parallel_config(
    tensor_parallel_size, pipeline_parallel_size, kv_parallel_size
):
    """Tests deep copying valid ParallelConfig objects and accessing their properties."""
    parallel_config = ParallelConfig(
        pipeline_parallel_size=pipeline_parallel_size,
        tensor_parallel_size=tensor_parallel_size,
        kv_parallel_size=kv_parallel_size,
        enable_sequence_pipeline_parallel=True,
    )
    parallel_config_deep_copy = copy.deepcopy(parallel_config)
    assert pipeline_parallel_size == parallel_config_deep_copy.pipeline_parallel_size
    assert tensor_parallel_size == parallel_config_deep_copy.tensor_parallel_size
    assert kv_parallel_size == parallel_config_deep_copy.kv_parallel_size


@pytest.mark.parametrize(
    "model, num_layers",
    [("meta-llama/Meta-Llama-3-8B", 12), ("meta-llama/Meta-Llama-3-70B", 24)],
)
@pytest.mark.unit
def test_can_deep_copy_model_config(model, num_layers):
    """Tests deep copying valid ModelConfig objects and accessing their properties."""
    model_config = ModelConfig(model=model, override_num_layers=num_layers)
    model_config_deep_copy = copy.deepcopy(model_config)
    assert model_config.model == model_config_deep_copy.model


@pytest.mark.parametrize(
    "tensor_parallel_size, pipeline_parallel_size, kv_parallel_size",
    [(1, 1, 1), (4, 2, 1)],
)
@pytest.mark.unit
def test_can_pickle_parallel_config(
    tensor_parallel_size, pipeline_parallel_size, kv_parallel_size
):
    """Tests pickling ParallelConfig objects and accessing their properties."""
    parallel_config = ParallelConfig(
        pipeline_parallel_size=pipeline_parallel_size,
        tensor_parallel_size=tensor_parallel_size,
        kv_parallel_size=kv_parallel_size,
        enable_sequence_pipeline_parallel=True,
    )

    # Pickle the object
    pickled_config = pickle.dumps(parallel_config)

    # Unpickle the object
    parallel_config_from_pickle = pickle.loads(pickled_config)

    assert pipeline_parallel_size == parallel_config_from_pickle.pipeline_parallel_size
    assert tensor_parallel_size == parallel_config_from_pickle.tensor_parallel_size
    assert kv_parallel_size == parallel_config_from_pickle.kv_parallel_size


@pytest.mark.parametrize(
    "model, num_layers",
    [("meta-llama/Meta-Llama-3-8B", 12), ("meta-llama/Meta-Llama-3-70B", 24)],
)
@pytest.mark.unit
def test_can_pickle_model_config(model, num_layers):
    """Tests pickling ModelConfig objects and accessing their properties."""
    model_config = ModelConfig(model=model, override_num_layers=num_layers)

    # Pickle the object
    pickled_config = pickle.dumps(model_config)

    # Unpickle the object
    model_config_from_pickle = pickle.loads(pickled_config)

    assert model_config.model == model_config_from_pickle.model


@pytest.mark.parametrize(
    "block_size",
    [16, 32, 64],
)
@pytest.mark.unit
def test_valid_cache_config_creation(block_size):
    """Tests creating valid CacheConfig objects and accessing their properties."""
    cache_config = CacheConfig(block_size=block_size)
    cache_config_c = cache_config.native_handle
    assert cache_config.block_size == cache_config_c.block_size


@pytest.mark.parametrize(
    "block_size",
    [16, 32, 64],
)
@pytest.mark.unit
def test_can_deep_copy_cache_config(block_size):
    """Tests deep copying valid CacheConfig objects and accessing their properties."""
    cache_config = CacheConfig(block_size=block_size)
    cache_config_deep_copy = copy.deepcopy(cache_config)
    assert cache_config.block_size == cache_config_deep_copy.block_size


@pytest.mark.parametrize(
    "block_size",
    [16, 32, 64],
)
@pytest.mark.unit
def test_can_pickle_cache_config(block_size):
    """Tests pickling CacheConfig objects and accessing their properties."""
    cache_config = CacheConfig(block_size=block_size)
    pickled_config = pickle.dumps(cache_config)
    cache_config_from_pickle = pickle.loads(pickled_config)
    assert cache_config.block_size == cache_config_from_pickle.block_size


@pytest.mark.parametrize(
    "write_metrics, wandb_project, enable_gpu_op_level_metrics",
    [
        (False, None, False),
        (True, "test-project", True),
        (True, "ml-project", False),
    ],
)
@pytest.mark.unit
def test_valid_metrics_config_creation(
    write_metrics, wandb_project, enable_gpu_op_level_metrics
):
    """Tests creating valid MetricsConfig objects and accessing their properties."""
    metrics_config = MetricsConfig(
        write_metrics=write_metrics,
        wandb_project=wandb_project,
        enable_gpu_op_level_metrics=enable_gpu_op_level_metrics,
    )
    metrics_config_c = metrics_config.native_handle
    assert metrics_config.write_metrics == metrics_config_c.write_metrics
    assert metrics_config.wandb_project == metrics_config_c.wandb_project
    assert (
        metrics_config.enable_gpu_op_level_metrics
        == metrics_config_c.enable_gpu_op_level_metrics
    )


@pytest.mark.parametrize(
    "write_metrics, wandb_project, wandb_run_name",
    [
        (False, None, None),
        (True, "test-project", "test-run"),
        (True, "ml-project", "experiment-1"),
    ],
)
@pytest.mark.unit
def test_can_deep_copy_metrics_config(write_metrics, wandb_project, wandb_run_name):
    """Tests deep copying valid MetricsConfig objects and accessing their properties."""
    metrics_config = MetricsConfig(
        write_metrics=write_metrics,
        wandb_project=wandb_project,
        wandb_run_name=wandb_run_name,
    )
    metrics_config_deep_copy = copy.deepcopy(metrics_config)
    assert metrics_config.write_metrics == metrics_config_deep_copy.write_metrics
    assert metrics_config.wandb_project == metrics_config_deep_copy.wandb_project
    assert metrics_config.wandb_run_name == metrics_config_deep_copy.wandb_run_name


@pytest.mark.parametrize(
    "write_metrics, enable_chrome_trace, store_png",
    [
        (False, False, False),
        (True, True, True),
        (True, False, True),
    ],
)
@pytest.mark.unit
def test_can_pickle_metrics_config(write_metrics, enable_chrome_trace, store_png):
    """Tests pickling MetricsConfig objects and accessing their properties."""
    metrics_config = MetricsConfig(
        write_metrics=write_metrics,
        enable_chrome_trace=enable_chrome_trace,
        store_png=store_png,
    )

    # Pickle the object
    pickled_config = pickle.dumps(metrics_config)

    # Unpickle the object
    metrics_config_from_pickle = pickle.loads(pickled_config)

    assert metrics_config.write_metrics == metrics_config_from_pickle.write_metrics
    assert (
        metrics_config.enable_chrome_trace
        == metrics_config_from_pickle.enable_chrome_trace
    )
    assert metrics_config.store_png == metrics_config_from_pickle.store_png


@pytest.mark.parametrize(
    "gpu_memory_utilization, use_native_execution_backend",
    [(0.5, False), (0.8, True), (1.0, False)],
)
@pytest.mark.unit
def test_valid_worker_config_creation(
    gpu_memory_utilization, use_native_execution_backend
):
    """Tests creating valid WorkerConfig objects and accessing their properties."""
    worker_config = WorkerConfig(
        gpu_memory_utilization=gpu_memory_utilization,
        use_native_execution_backend=use_native_execution_backend,
    )
    assert worker_config.gpu_memory_utilization == gpu_memory_utilization
    assert worker_config.use_native_execution_backend == use_native_execution_backend


@pytest.mark.parametrize(
    "gpu_memory_utilization, use_native_execution_backend",
    [(0.5, False), (0.8, True), (1.0, False)],
)
@pytest.mark.unit
def test_can_deep_copy_worker_config(
    gpu_memory_utilization, use_native_execution_backend
):
    """Tests deep copying valid WorkerConfig objects and accessing their properties."""
    worker_config = WorkerConfig(
        gpu_memory_utilization=gpu_memory_utilization,
        use_native_execution_backend=use_native_execution_backend,
    )
    worker_config_deep_copy = copy.deepcopy(worker_config)
    assert (
        worker_config.gpu_memory_utilization
        == worker_config_deep_copy.gpu_memory_utilization
    )
    assert (
        worker_config.use_native_execution_backend
        == worker_config_deep_copy.use_native_execution_backend
    )


@pytest.mark.parametrize(
    "gpu_memory_utilization, use_native_execution_backend",
    [(0.5, False), (0.8, True), (1.0, False)],
)
@pytest.mark.unit
def test_can_pickle_worker_config(gpu_memory_utilization, use_native_execution_backend):
    """Tests pickling WorkerConfig objects and accessing their properties."""
    worker_config = WorkerConfig(
        gpu_memory_utilization=gpu_memory_utilization,
        use_native_execution_backend=use_native_execution_backend,
    )
    pickled_config = pickle.dumps(worker_config)
    worker_config_from_pickle = pickle.loads(pickled_config)

    assert (
        worker_config.gpu_memory_utilization
        == worker_config_from_pickle.gpu_memory_utilization
    )
    assert (
        worker_config.use_native_execution_backend
        == worker_config_from_pickle.use_native_execution_backend
    )
