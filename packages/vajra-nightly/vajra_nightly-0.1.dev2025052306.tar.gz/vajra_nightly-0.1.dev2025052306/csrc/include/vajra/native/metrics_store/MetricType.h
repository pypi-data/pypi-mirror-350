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
#pragma once
//==============================================================================
#include "commons/StdCommon.h"
//==============================================================================
namespace vajra {
//==============================================================================
// Enum for metric types
enum class MetricType {
  // GPU Operations
  MLP_UP_PROJ,
  MLP_UP_PROJ_ALL_GATHER,
  MLP_ACTIVATION,
  MLP_DOWN_PROJ,
  MLP_DOWN_PROJ_ALL_REDUCE,
  ATTN_PRE_PROJ,
  ATTN_PRE_PROJ_ALL_GATHER,
  ATTN_POST_PROJ,
  ATTN_POST_PROJ_ALL_REDUCE,
  ATTN_KV_CACHE_SAVE,
  ATTN,
  ATTN_ROPE,
  ATTN_INPUT_RESHAPE,
  ATTN_OUTPUT_RESHAPE,
  EMBED_LINEAR,
  EMBED_ALL_REDUCE,
  LM_HEAD_LINEAR,
  LM_HEAD_ALL_GATHER,
  INPUT_LAYERNORM,
  POST_ATTENTION_LAYERNORM,
  NORM,
  ADD,
  NCCL_SEND,
  NCCL_RECV,
  MOE_GATING,
  MOE_LINEAR,
  // CPU Operations
  SAMPLER,
  PREPARE_INPUTS,
  MODEL_EXECUTION,
  WORKER_ON_SCHEDULE_HANDLING,
  WORKER_ON_STEP_COMPLETE_HANDLING,
  ATTN_BEGIN_FORWARD,
  // Sequence Metrics Time Distributions
  REQUEST_E2E_TIME,
  REQUEST_INTER_ARRIVAL_DELAY,
  REQUEST_E2E_TIME_NORMALIZED,
  REQUEST_E2E_TIME_PIECEWISE_NORMALIZED,
  REQUEST_EXECUTION_TIME,
  REQUEST_EXECUTION_TIME_NORMALIZED,
  REQUEST_PREEMPTION_TIME,
  REQUEST_SCHEDULING_DELAY,
  REQUEST_EXECUTION_PLUS_PREEMPTION_TIME,
  REQUEST_EXECUTION_PLUS_PREEMPTION_TIME_NORMALIZED,
  PREFILL_TIME_E2E,
  PREFILL_TIME_E2E_NORMALIZED,
  PREFILL_TIME_E2E_PIECEWISE_NORMALIZED,
  PREFILL_TIME_EXECUTION_PLUS_PREEMPTION,
  PREFILL_TIME_EXECUTION_PLUS_PREEMPTION_NORMALIZED,
  DECODE_TIME_EXECUTION_PLUS_PREEMPTION_NORMALIZED,
  // Sequence Metrics Histograms
  REQUEST_NUM_TOKENS,
  REQUEST_PREFILL_TOKENS,
  REQUEST_DECODE_TOKENS,
  REQUEST_PD_RATIO,
  REQUEST_NUM_RESTARTS,
  REQUEST_NUM_PAUSES,
  REQUEST_NUM_IGNORED,
  // Batch Metrics Count Distributions
  BATCH_NUM_TOKENS,
  BATCH_NUM_PREFILL_TOKENS,
  BATCH_NUM_DECODE_TOKENS,
  BATCH_SIZE,
  // Batch Metrics Time Distributions
  BATCH_EXECUTION_TIME,
  INTER_BATCH_DELAY,
  // Token Metrics Time Distributions
  DECODE_TOKEN_EXECUTION_PLUS_PREEMPTION_TIME,
  // Completion Metrics Time Series
  REQUEST_ARRIVED,
  REQUEST_COMPLETED,
  PREFILL_COMPLETED,
  DECODE_COMPLETED
};

// Convert MetricType to string
std::string MetricTypeToString(MetricType type);

// Convert string to MetricType
MetricType StringToMetricType(const std::string& str);
}  // namespace vajra
//==============================================================================
