#!/bin/bash
set -xe

_script_dir=$(dirname "$0")
# root dir is 2 levels up
ROOT_DIR=$(dirname $(dirname $_script_dir))

MODEL_NAME=gradientai/Llama-3-8B-Instruct-Gradient-1048k
TP_DEGREE=1
PP_DEGREE=1
KVP_DEGREE=1
USE_PIPE_SEQ_PARALLEL=false
CHUNK_SIZE=4096
PREFILL_LENGTH=$((128 * 1024))
DECODE_LENGTH=128
OVERRIDE_NUM_LAYERS=""
USE_NATIVE_BACKEND=false
SCHEDULER="FCFS_FIXED_CHUNK"
WANDB_PROJECT=""
WANDB_GROUP=""
WANDB_RUN=""


while [[ $# -gt 0 ]]
do
key="$1"
case $key in
    --model_name)
    MODEL_NAME="$2"
    shift
    shift
    ;;
    --tensor_parallel_degree)
    TP_DEGREE="$2"
    shift
    shift
    ;;
    --kv_parallel_degree)
    KVP_DEGREE="$2"
    shift
    shift
    ;;
    --pipe_parallel_degree)
    PP_DEGREE="$2"
    shift
    shift
    ;;
    --use_pipe_seq_parallel)
    USE_PIPE_SEQ_PARALLEL=true
    shift
    ;;
    --prefill_length)
    PREFILL_LENGTH="$2"
    shift
    shift
    ;;
    --decode_length)
    DECODE_LENGTH="$2"
    shift
    shift
    ;;
    --chunk_size)
    CHUNK_SIZE="$2"
    shift
    shift
    ;;
    --override_num_layers)
    OVERRIDE_NUM_LAYERS="$2"
    shift
    shift
    ;;
    --wandb_project)
    WANDB_PROJECT="$2"
    shift
    shift
    ;;
    --wandb_group)
    WANDB_GROUP="$2"
    shift
    shift
    ;;
    --wandb_run)
    WANDB_RUN="$2"
    shift
    shift
    ;;
    --use_native_backend)
    USE_NATIVE_BACKEND=true
    shift
    ;;
    *)
    echo "Unknown option $1"
    exit 1
    ;;
esac
done

_PREFILL_LENGTH=$((PREFILL_LENGTH))
TOTAL_LENGTH=$((_PREFILL_LENGTH + DECODE_LENGTH))
_MAX_CACHE_OCCUPANCY=$((PREFILL_LENGTH / KVP_DEGREE + CHUNK_SIZE))

cd $ROOT_DIR

if [ ! -z "$WANDB_RUN" ]; then
    WANDB_RUN="$WANDB_RUN-"
fi

RUN_NAME=${WANDB_RUN}p_${PREFILL_LENGTH}-d_${DECODE_LENGTH}-tp_${TP_DEGREE}-kvp_${KVP_DEGREE}-pp_${PP_DEGREE}-spp_${USE_PIPE_SEQ_PARALLEL}-cs_${CHUNK_SIZE}

OUTPUT_DIR=$ROOT_DIR/benchmark_output/single_request_benchmark/$RUN_NAME

WANDB_PROJECT_ARG=""
if [ ! -z "$WANDB_PROJECT" ]; then
    WANDB_PROJECT_ARG="--metrics_config_wandb_project $WANDB_PROJECT"
fi

if [ ! -z "$GROUP_NAME" ]; then
    GROUP_NAME=${WANDB_GROUP}-${MODEL_NAME}
    WANDB_GROUP_ARG="--metrics_config_wandb_group $GROUP_NAME"
fi

if [ ! -z "$WANDB_RUN" ]; then
    WANDB_RUN_ARG="--metrics_config_wandb_run_name $WANDB_RUN"
fi

OVERRIDE_NUM_LAYERS_ARG=""
if [ ! -z "$OVERRIDE_NUM_LAYERS" ]; then
    OVERRIDE_NUM_LAYERS_ARG="--model_config_override_num_layers $OVERRIDE_NUM_LAYERS"
fi

mkdir -p $OUTPUT_DIR

python -m vajra.benchmark.main \
--output_dir $OUTPUT_DIR \
--model_config_model $MODEL_NAME \
--model_config_max_model_len $TOTAL_LENGTH \
--parallel_config_tensor_parallel_size $TP_DEGREE \
--parallel_config_pipeline_parallel_size $PP_DEGREE \
--parallel_config_kv_parallel_size $KVP_DEGREE \
--parallel_config_max_num_tokens_per_kvp_group $_MAX_CACHE_OCCUPANCY \
--parallel_config_enable_sequence_pipeline_parallel $USE_PIPE_SEQ_PARALLEL \
--request_generator_config_type SYNTHETIC \
--interval_generator_config_type STATIC \
--synthetic_request_generator_config_num_requests 1 \
--length_generator_config_type FIXED \
--fixed_request_length_generator_config_prefill_tokens $_PREFILL_LENGTH \
--fixed_request_length_generator_config_decode_tokens $DECODE_LENGTH \
--scheduler_config_type $SCHEDULER \
--fcfs_fixed_chunk_scheduler_config_max_batch_size 1 \
--fcfs_fixed_chunk_scheduler_config_chunk_size $CHUNK_SIZE \
--metrics_config_enable_cpu_op_level_metrics false \
--metrics_config_enable_chrome_trace false \
--worker_config_use_native_execution_backend $USE_NATIVE_BACKEND \
$OVERRIDE_NUM_LAYERS_ARG \
$WANDB_PROJECT_ARG \
$WANDB_GROUP_ARG \
$WANDB_RUN_ARG |& tee $OUTPUT_DIR/output.log
