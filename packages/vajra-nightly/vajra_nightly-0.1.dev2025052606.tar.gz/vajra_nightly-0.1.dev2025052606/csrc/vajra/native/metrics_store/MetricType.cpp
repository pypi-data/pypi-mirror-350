//==============================================================================
// Copyright 2025 Vajra Team; Georgia Institute of Technology
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.
//==============================================================================
#include "native/metrics_store/MetricType.h"

#include "commons/Logging.h"
//==============================================================================
namespace vajra {
//==============================================================================
std::string MetricTypeToString(MetricType type) {
  switch (type) {
    // GPU Operations
    case MetricType::MLP_UP_PROJ:
      return "mlp_up_proj";
    case MetricType::MLP_UP_PROJ_ALL_GATHER:
      return "mlp_up_proj_all_gather";
    case MetricType::MLP_ACTIVATION:
      return "mlp_activation";
    case MetricType::MLP_DOWN_PROJ:
      return "mlp_down_proj";
    case MetricType::MLP_DOWN_PROJ_ALL_REDUCE:
      return "mlp_down_proj_all_reduce";
    case MetricType::ATTN_PRE_PROJ:
      return "attn_pre_proj";
    case MetricType::ATTN_PRE_PROJ_ALL_GATHER:
      return "attn_pre_proj_all_gather";
    case MetricType::ATTN_POST_PROJ:
      return "attn_post_proj";
    case MetricType::ATTN_POST_PROJ_ALL_REDUCE:
      return "attn_post_proj_all_reduce";
    case MetricType::ATTN_KV_CACHE_SAVE:
      return "attn_kv_cache_save";
    case MetricType::ATTN:
      return "attn";
    case MetricType::ATTN_ROPE:
      return "attn_rope";
    case MetricType::ATTN_INPUT_RESHAPE:
      return "attn_input_reshape";
    case MetricType::ATTN_OUTPUT_RESHAPE:
      return "attn_output_reshape";
    case MetricType::EMBED_LINEAR:
      return "embed_linear";
    case MetricType::EMBED_ALL_REDUCE:
      return "embed_all_reduce";
    case MetricType::LM_HEAD_LINEAR:
      return "lm_head_linear";
    case MetricType::LM_HEAD_ALL_GATHER:
      return "lm_head_all_gather";
    case MetricType::INPUT_LAYERNORM:
      return "input_layernorm";
    case MetricType::POST_ATTENTION_LAYERNORM:
      return "post_attention_layernorm";
    case MetricType::NORM:
      return "norm";
    case MetricType::ADD:
      return "add";
    case MetricType::NCCL_SEND:
      return "nccl_send";
    case MetricType::NCCL_RECV:
      return "nccl_recv";
    case MetricType::MOE_GATING:
      return "moe_gating";
    case MetricType::MOE_LINEAR:
      return "moe_linear";
    // CPU Operations
    case MetricType::SAMPLER:
      return "sample";
    case MetricType::PREPARE_INPUTS:
      return "prepare_inputs";
    case MetricType::MODEL_EXECUTION:
      return "model_execution";
    case MetricType::WORKER_ON_SCHEDULE_HANDLING:
      return "worker_on_schedule_handling";
    case MetricType::WORKER_ON_STEP_COMPLETE_HANDLING:
      return "worker_on_step_complete_handling";
    case MetricType::ATTN_BEGIN_FORWARD:
      return "attn_begin_forward";
    // Sequence Metrics Time Distributions
    case MetricType::REQUEST_E2E_TIME:
      return "request_e2e_time";
    case MetricType::REQUEST_INTER_ARRIVAL_DELAY:
      return "request_inter_arrival_delay";
    case MetricType::REQUEST_E2E_TIME_NORMALIZED:
      return "request_e2e_time_normalized";
    case MetricType::REQUEST_E2E_TIME_PIECEWISE_NORMALIZED:
      return "request_e2e_time_piecewise_normalized";
    case MetricType::REQUEST_EXECUTION_TIME:
      return "request_execution_time";
    case MetricType::REQUEST_EXECUTION_TIME_NORMALIZED:
      return "request_execution_time_normalized";
    case MetricType::REQUEST_PREEMPTION_TIME:
      return "request_preemption_time";
    case MetricType::REQUEST_SCHEDULING_DELAY:
      return "request_scheduling_delay";
    case MetricType::REQUEST_EXECUTION_PLUS_PREEMPTION_TIME:
      return "request_execution_plus_preemption_time";
    case MetricType::REQUEST_EXECUTION_PLUS_PREEMPTION_TIME_NORMALIZED:
      return "request_execution_plus_preemption_time_normalized";
    case MetricType::PREFILL_TIME_E2E:
      return "prefill_e2e_time";
    case MetricType::PREFILL_TIME_E2E_NORMALIZED:
      return "prefill_e2e_time_normalized";
    case MetricType::PREFILL_TIME_E2E_PIECEWISE_NORMALIZED:
      return "prefill_e2e_time_piecewise_normalized";
    case MetricType::PREFILL_TIME_EXECUTION_PLUS_PREEMPTION:
      return "prefill_time_execution_plus_preemption";
    case MetricType::PREFILL_TIME_EXECUTION_PLUS_PREEMPTION_NORMALIZED:
      return "prefill_time_execution_plus_preemption_normalized";
    case MetricType::DECODE_TIME_EXECUTION_PLUS_PREEMPTION_NORMALIZED:
      return "decode_time_execution_plus_preemption_normalized";
    // Sequence Metrics Histograms
    case MetricType::REQUEST_NUM_TOKENS:
      return "request_num_tokens";
    case MetricType::REQUEST_PREFILL_TOKENS:
      return "request_num_prefill_tokens";
    case MetricType::REQUEST_DECODE_TOKENS:
      return "request_num_decode_tokens";
    case MetricType::REQUEST_PD_RATIO:
      return "request_pd_ratio";
    case MetricType::REQUEST_NUM_RESTARTS:
      return "request_num_restarts";
    case MetricType::REQUEST_NUM_PAUSES:
      return "request_num_pauses";
    case MetricType::REQUEST_NUM_IGNORED:
      return "request_num_ignored";
    // Batch Metrics Count Distributions
    case MetricType::BATCH_NUM_TOKENS:
      return "batch_num_tokens";
    case MetricType::BATCH_NUM_PREFILL_TOKENS:
      return "batch_num_prefill_tokens";
    case MetricType::BATCH_NUM_DECODE_TOKENS:
      return "batch_num_decode_tokens";
    case MetricType::BATCH_SIZE:
      return "batch_size";
    // Batch Metrics Time Distributions
    case MetricType::BATCH_EXECUTION_TIME:
      return "batch_execution_time";
    case MetricType::INTER_BATCH_DELAY:
      return "inter_batch_delay";
    // Token Metrics Time Distributions
    case MetricType::DECODE_TOKEN_EXECUTION_PLUS_PREEMPTION_TIME:
      return "decode_token_execution_plus_preemption_time";
    // Completion Metrics Time Series
    case MetricType::REQUEST_ARRIVED:
      return "request_arrived";
    case MetricType::REQUEST_COMPLETED:
      return "request_completed";
    case MetricType::PREFILL_COMPLETED:
      return "prefill_completed";
    case MetricType::DECODE_COMPLETED:
      return "decode_completed";
    default:
      RAISE_INVALID_ARGUMENTS_ERROR("Unknown MetricType");
  }
}
//==============================================================================
MetricType StringToMetricType(const std::string& str) {
  // GPU Operations
  if (str == "mlp_up_proj") return MetricType::MLP_UP_PROJ;
  if (str == "mlp_up_proj_all_gather")
    return MetricType::MLP_UP_PROJ_ALL_GATHER;
  if (str == "mlp_activation") return MetricType::MLP_ACTIVATION;
  if (str == "mlp_down_proj") return MetricType::MLP_DOWN_PROJ;
  if (str == "mlp_down_proj_all_reduce")
    return MetricType::MLP_DOWN_PROJ_ALL_REDUCE;
  if (str == "attn_pre_proj") return MetricType::ATTN_PRE_PROJ;
  if (str == "attn_pre_proj_all_gather")
    return MetricType::ATTN_PRE_PROJ_ALL_GATHER;
  if (str == "attn_post_proj") return MetricType::ATTN_POST_PROJ;
  if (str == "attn_post_proj_all_reduce")
    return MetricType::ATTN_POST_PROJ_ALL_REDUCE;
  if (str == "attn_kv_cache_save") return MetricType::ATTN_KV_CACHE_SAVE;
  if (str == "attn") return MetricType::ATTN;
  if (str == "attn_rope") return MetricType::ATTN_ROPE;
  if (str == "attn_input_reshape") return MetricType::ATTN_INPUT_RESHAPE;
  if (str == "attn_output_reshape") return MetricType::ATTN_OUTPUT_RESHAPE;
  if (str == "embed_linear") return MetricType::EMBED_LINEAR;
  if (str == "embed_all_reduce") return MetricType::EMBED_ALL_REDUCE;
  if (str == "lm_head_linear") return MetricType::LM_HEAD_LINEAR;
  if (str == "lm_head_all_gather") return MetricType::LM_HEAD_ALL_GATHER;
  if (str == "input_layernorm") return MetricType::INPUT_LAYERNORM;
  if (str == "post_attention_layernorm")
    return MetricType::POST_ATTENTION_LAYERNORM;
  if (str == "norm") return MetricType::NORM;
  if (str == "add") return MetricType::ADD;
  if (str == "nccl_send") return MetricType::NCCL_SEND;
  if (str == "nccl_recv") return MetricType::NCCL_RECV;
  if (str == "moe_gating") return MetricType::MOE_GATING;
  if (str == "moe_linear") return MetricType::MOE_LINEAR;
  // CPU Operations
  if (str == "sample") return MetricType::SAMPLER;
  if (str == "prepare_inputs") return MetricType::PREPARE_INPUTS;
  if (str == "model_execution") return MetricType::MODEL_EXECUTION;
  if (str == "worker_on_schedule_handling")
    return MetricType::WORKER_ON_SCHEDULE_HANDLING;
  if (str == "worker_on_step_complete_handling")
    return MetricType::WORKER_ON_STEP_COMPLETE_HANDLING;
  if (str == "attn_begin_forward") return MetricType::ATTN_BEGIN_FORWARD;
  // Sequence Metrics Time Distributions
  if (str == "request_e2e_time") return MetricType::REQUEST_E2E_TIME;
  if (str == "request_inter_arrival_delay")
    return MetricType::REQUEST_INTER_ARRIVAL_DELAY;
  if (str == "request_e2e_time_normalized")
    return MetricType::REQUEST_E2E_TIME_NORMALIZED;
  if (str == "request_e2e_time_piecewise_normalized")
    return MetricType::REQUEST_E2E_TIME_PIECEWISE_NORMALIZED;
  if (str == "request_execution_time")
    return MetricType::REQUEST_EXECUTION_TIME;
  if (str == "request_execution_time_normalized")
    return MetricType::REQUEST_EXECUTION_TIME_NORMALIZED;
  if (str == "request_preemption_time")
    return MetricType::REQUEST_PREEMPTION_TIME;
  if (str == "request_scheduling_delay")
    return MetricType::REQUEST_SCHEDULING_DELAY;
  if (str == "request_execution_plus_preemption_time")
    return MetricType::REQUEST_EXECUTION_PLUS_PREEMPTION_TIME;
  if (str == "request_execution_plus_preemption_time_normalized")
    return MetricType::REQUEST_EXECUTION_PLUS_PREEMPTION_TIME_NORMALIZED;
  if (str == "prefill_e2e_time") return MetricType::PREFILL_TIME_E2E;
  if (str == "prefill_e2e_time_normalized")
    return MetricType::PREFILL_TIME_E2E_NORMALIZED;
  if (str == "prefill_e2e_time_piecewise_normalized")
    return MetricType::PREFILL_TIME_E2E_PIECEWISE_NORMALIZED;
  if (str == "prefill_time_execution_plus_preemption")
    return MetricType::PREFILL_TIME_EXECUTION_PLUS_PREEMPTION;
  if (str == "prefill_time_execution_plus_preemption_normalized")
    return MetricType::PREFILL_TIME_EXECUTION_PLUS_PREEMPTION_NORMALIZED;
  if (str == "decode_time_execution_plus_preemption_normalized")
    return MetricType::DECODE_TIME_EXECUTION_PLUS_PREEMPTION_NORMALIZED;
  // Sequence Metrics Histograms
  if (str == "request_num_tokens") return MetricType::REQUEST_NUM_TOKENS;
  if (str == "request_num_prefill_tokens")
    return MetricType::REQUEST_PREFILL_TOKENS;
  if (str == "request_num_decode_tokens")
    return MetricType::REQUEST_DECODE_TOKENS;
  if (str == "request_pd_ratio") return MetricType::REQUEST_PD_RATIO;
  if (str == "request_num_restarts") return MetricType::REQUEST_NUM_RESTARTS;
  if (str == "request_num_pauses") return MetricType::REQUEST_NUM_PAUSES;
  if (str == "request_num_ignored") return MetricType::REQUEST_NUM_IGNORED;
  // Batch Metrics Count Distributions
  if (str == "batch_num_tokens") return MetricType::BATCH_NUM_TOKENS;
  if (str == "batch_num_prefill_tokens")
    return MetricType::BATCH_NUM_PREFILL_TOKENS;
  if (str == "batch_num_decode_tokens")
    return MetricType::BATCH_NUM_DECODE_TOKENS;
  if (str == "batch_size") return MetricType::BATCH_SIZE;
  // Batch Metrics Time Distributions
  if (str == "batch_execution_time") return MetricType::BATCH_EXECUTION_TIME;
  if (str == "inter_batch_delay") return MetricType::INTER_BATCH_DELAY;
  // Token Metrics Time Distributions
  if (str == "decode_token_execution_plus_preemption_time")
    return MetricType::DECODE_TOKEN_EXECUTION_PLUS_PREEMPTION_TIME;
  // Completion Metrics Time Series
  if (str == "request_arrived") return MetricType::REQUEST_ARRIVED;
  if (str == "request_completed") return MetricType::REQUEST_COMPLETED;
  if (str == "prefill_completed") return MetricType::PREFILL_COMPLETED;
  if (str == "decode_completed") return MetricType::DECODE_COMPLETED;

  RAISE_INVALID_ARGUMENTS_ERROR("Unknown MetricType string: {}", str);
}
//==============================================================================
}  // namespace vajra
//==============================================================================
