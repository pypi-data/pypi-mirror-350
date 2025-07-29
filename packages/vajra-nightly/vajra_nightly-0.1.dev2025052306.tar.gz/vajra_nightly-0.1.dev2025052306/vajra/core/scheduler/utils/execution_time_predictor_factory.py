from typing import Dict

from vidur.config import RandomForrestExecutionTimePredictorConfig
from vidur.config import ReplicaConfig as VidurReplicaConfig
from vidur.execution_time_predictor import (
    BaseExecutionTimePredictor,
    ExecutionTimePredictorRegistry,
)

from vajra.config import CacheConfig, ModelConfig, ParallelConfig

# TODO(Amey): wire these up to be picked dynamically
PREDICTION_MAX_CHUNK_SIZE = 4 * 1024
MAX_TOKENS_PER_SEQ = 2 * 1024 * 1024
PREDICTION_MAX_BATCH_SIZE = 128
PREDICTION_DEVICE = "h100"
PREDICTION_NETWORK_DEVICE = "h100_dgx"
KV_CACHE_PREDICTION_GRANULARITY = 512
MODEL_NAME_MAPPING = {
    "meta-llama/Meta-Llama-3-8B": "meta-llama/Llama-3-8B",
    "meta-llama/Meta-Llama-3-8B-Instruct": "meta-llama/Llama-3-8B",
    "gradientai/Llama-3-8B-Instruct-Gradient-1048k": "meta-llama/Llama-3-8B",
    "gradientai/Llama-3-70B-Instruct-Gradient-1048k": "meta-llama/Llama-2-70b-hf",
}


class ExecutionTimePredictorFactory:
    _execution_time_predictors: Dict[int, BaseExecutionTimePredictor] = {}

    @classmethod
    def get_config_hash(
        cls,
        model_config: ModelConfig,
        parallel_config: ParallelConfig,
        cache_config: CacheConfig,
    ) -> int:
        return hash(
            (
                model_config.model,
                parallel_config.pipeline_parallel_size,
                cache_config.block_size,
            )
        )

    @classmethod
    def get_execution_time_predictor(
        cls,
        model_config: ModelConfig,
        parallel_config: ParallelConfig,
        cache_config: CacheConfig,
    ) -> BaseExecutionTimePredictor:
        config_hash = cls.get_config_hash(model_config, parallel_config, cache_config)

        if config_hash in cls._execution_time_predictors:
            return cls._execution_time_predictors[config_hash]

        execution_time_predictor_config = RandomForrestExecutionTimePredictorConfig(
            prediction_max_prefill_chunk_size=PREDICTION_MAX_CHUNK_SIZE,
            prediction_max_tokens_per_request=MAX_TOKENS_PER_SEQ,
            prediction_max_batch_size=PREDICTION_MAX_BATCH_SIZE,
            kv_cache_prediction_granularity=KV_CACHE_PREDICTION_GRANULARITY,
            use_native_execution_time_predictor=True,
        )
        vidur_replica_config = VidurReplicaConfig(
            model_name=MODEL_NAME_MAPPING[model_config.model],
            num_pipeline_stages=parallel_config.pipeline_parallel_size,
            tensor_parallel_size=parallel_config.tensor_parallel_size,
            kv_parallel_size=parallel_config.kv_parallel_size,
            max_num_tokens_per_kvp_group=parallel_config.max_num_tokens_per_kvp_group,
            enable_sequence_pipeline_parallel=parallel_config.enable_sequence_pipeline_parallel,
            device=PREDICTION_DEVICE,
            network_device=PREDICTION_NETWORK_DEVICE,
            block_size=cache_config.block_size,
        )
        execution_time_predictor = ExecutionTimePredictorRegistry.get(
            execution_time_predictor_config.get_type(),
            predictor_config=execution_time_predictor_config,
            replica_config=vidur_replica_config,
        )

        # Make sure the native_execution_time_predictor is initialized
        if not execution_time_predictor._native_execution_time_predictor:
            raise ValueError(
                "execution_time_predictor does not have _native_execution_time_predictor attribute"
            )

        cls._execution_time_predictors[config_hash] = execution_time_predictor

        return execution_time_predictor
