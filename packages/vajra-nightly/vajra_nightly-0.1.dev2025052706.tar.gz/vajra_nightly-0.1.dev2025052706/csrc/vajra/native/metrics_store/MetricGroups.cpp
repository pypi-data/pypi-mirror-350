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
#include "native/metrics_store/MetricGroups.h"

#include "commons/Logging.h"
//==============================================================================
namespace vajra {
//==============================================================================
std::vector<MetricType> GetGpuOperationMetricsTypes() {
  return {
      MetricType::MLP_UP_PROJ,
      MetricType::MLP_UP_PROJ_ALL_GATHER,
      MetricType::MLP_ACTIVATION,
      MetricType::MLP_DOWN_PROJ,
      MetricType::MLP_DOWN_PROJ_ALL_REDUCE,
      MetricType::ATTN_PRE_PROJ,
      MetricType::ATTN_PRE_PROJ_ALL_GATHER,
      MetricType::ATTN_POST_PROJ,
      MetricType::ATTN_POST_PROJ_ALL_REDUCE,
      MetricType::ATTN_KV_CACHE_SAVE,
      MetricType::ATTN,
      MetricType::ATTN_ROPE,
      MetricType::ATTN_INPUT_RESHAPE,
      MetricType::ATTN_OUTPUT_RESHAPE,
      MetricType::EMBED_LINEAR,
      MetricType::EMBED_ALL_REDUCE,
      MetricType::LM_HEAD_LINEAR,
      MetricType::LM_HEAD_ALL_GATHER,
      MetricType::INPUT_LAYERNORM,
      MetricType::POST_ATTENTION_LAYERNORM,
      MetricType::NORM,
      MetricType::ADD,
      MetricType::NCCL_SEND,
      MetricType::NCCL_RECV,
      MetricType::MOE_GATING,
      MetricType::MOE_LINEAR,
  };
}
//==============================================================================
std::vector<Metric> GetGpuOperationMetrics(bool requires_label) {
  std::vector<Metric> metrics;
  for (MetricType metric_type : GetGpuOperationMetricsTypes()) {
    metrics.emplace_back(metric_type, UnitType::MS, requires_label,
                         PlotType::CDF,
                         ComparisonGroupType::GPU_OPERATION_RUNTIME,
                         EntityAssociationType::BATCH, LabelType::BATCH);
  }
  return metrics;
}
//==============================================================================
std::vector<MetricType> GetCpuOperationMetricsTypes() {
  return {MetricType::SAMPLER,
          MetricType::PREPARE_INPUTS,
          MetricType::MODEL_EXECUTION,
          MetricType::WORKER_ON_SCHEDULE_HANDLING,
          MetricType::WORKER_ON_STEP_COMPLETE_HANDLING,
          MetricType::ATTN_BEGIN_FORWARD};
}
//==============================================================================
std::vector<Metric> GetCpuOperationMetrics(bool requires_label) {
  std::vector<Metric> metrics;
  for (MetricType metric_type : GetCpuOperationMetricsTypes()) {
    metrics.emplace_back(metric_type, UnitType::SECONDS, requires_label,
                         PlotType::CDF, ComparisonGroupType::BATCH_RUNTIME,
                         EntityAssociationType::BATCH, LabelType::BATCH);
  }

  return metrics;
}
//==============================================================================
std::vector<MetricType> GetSequenceTimeDistributionMetricsTypes() {
  return {MetricType::REQUEST_E2E_TIME,
          MetricType::REQUEST_INTER_ARRIVAL_DELAY,
          MetricType::REQUEST_E2E_TIME_NORMALIZED,
          MetricType::REQUEST_E2E_TIME_PIECEWISE_NORMALIZED,
          MetricType::REQUEST_EXECUTION_TIME,
          MetricType::REQUEST_EXECUTION_TIME_NORMALIZED,
          MetricType::REQUEST_PREEMPTION_TIME,
          MetricType::REQUEST_SCHEDULING_DELAY,
          MetricType::REQUEST_EXECUTION_PLUS_PREEMPTION_TIME,
          MetricType::REQUEST_EXECUTION_PLUS_PREEMPTION_TIME_NORMALIZED,
          MetricType::PREFILL_TIME_E2E,
          MetricType::PREFILL_TIME_E2E_NORMALIZED,
          MetricType::PREFILL_TIME_E2E_PIECEWISE_NORMALIZED,
          MetricType::PREFILL_TIME_EXECUTION_PLUS_PREEMPTION,
          MetricType::PREFILL_TIME_EXECUTION_PLUS_PREEMPTION_NORMALIZED,
          MetricType::DECODE_TIME_EXECUTION_PLUS_PREEMPTION_NORMALIZED};
}
//==============================================================================
std::vector<Metric> GetSequenceTimeDistributionMetrics() {
  std::vector<Metric> metrics;
  for (MetricType metric_type : GetSequenceTimeDistributionMetricsTypes()) {
    metrics.emplace_back(metric_type, UnitType::SECONDS, true, PlotType::CDF,
                         ComparisonGroupType::REQUEST_RUNTIME,
                         EntityAssociationType::REQUEST, LabelType::REQUEST);
  }

  return metrics;
}
//==============================================================================
std::vector<MetricType> GetSequenceHistogramMetricsTypes() {
  return {MetricType::REQUEST_NUM_TOKENS,    MetricType::REQUEST_PREFILL_TOKENS,
          MetricType::REQUEST_DECODE_TOKENS, MetricType::REQUEST_PD_RATIO,
          MetricType::REQUEST_NUM_RESTARTS,  MetricType::REQUEST_NUM_PAUSES,
          MetricType::REQUEST_NUM_IGNORED};
}
//==============================================================================
std::vector<Metric> GetSequenceHistogramMetrics() {
  std::vector<Metric> metrics;
  for (MetricType metric_type : GetSequenceHistogramMetricsTypes()) {
    metrics.emplace_back(metric_type, UnitType::COUNT, true,
                         PlotType::HISTOGRAM, std::nullopt,
                         EntityAssociationType::REQUEST, LabelType::REQUEST);
  }

  return metrics;
}
//==============================================================================
std::vector<MetricType> GetBatchCountDistributionMetricsTypes() {
  return {MetricType::BATCH_NUM_TOKENS, MetricType::BATCH_NUM_PREFILL_TOKENS,
          MetricType::BATCH_NUM_DECODE_TOKENS, MetricType::BATCH_SIZE};
}
//==============================================================================
std::vector<Metric> GetBatchCountDistributionMetrics(bool requires_label) {
  std::vector<Metric> metrics;
  for (MetricType metric_type : GetBatchCountDistributionMetricsTypes()) {
    metrics.emplace_back(metric_type, UnitType::COUNT, requires_label,
                         PlotType::CDF, ComparisonGroupType::BATCH_COMPOSITION,
                         EntityAssociationType::BATCH, LabelType::BATCH);
  }

  return metrics;
}
//==============================================================================
std::vector<MetricType> GetBatchTimeDistributionMetricsTypes() {
  return {MetricType::BATCH_EXECUTION_TIME, MetricType::INTER_BATCH_DELAY};
}
//==============================================================================
std::vector<Metric> GetBatchTimeDistributionMetrics(bool requires_label) {
  std::vector<Metric> metrics;
  for (MetricType metric_type : GetBatchTimeDistributionMetricsTypes()) {
    metrics.emplace_back(metric_type, UnitType::SECONDS, requires_label,
                         PlotType::CDF, ComparisonGroupType::BATCH_RUNTIME,
                         EntityAssociationType::BATCH, LabelType::BATCH);
  }

  return metrics;
}
//==============================================================================
std::vector<MetricType> GetTokenTimeDistributionMetricsTypes() {
  return {MetricType::DECODE_TOKEN_EXECUTION_PLUS_PREEMPTION_TIME};
}
//==============================================================================
std::vector<Metric> GetTokenTimeDistributionMetrics() {
  std::vector<Metric> metrics;
  for (MetricType metric_type : GetTokenTimeDistributionMetricsTypes()) {
    metrics.emplace_back(metric_type, UnitType::SECONDS, false, PlotType::CDF,
                         std::nullopt, std::nullopt, std::nullopt);
  }

  return metrics;
}
//==============================================================================
std::vector<MetricType> GetCompletionTimeSeriesMetricsTypes() {
  return {MetricType::REQUEST_ARRIVED, MetricType::REQUEST_COMPLETED,
          MetricType::PREFILL_COMPLETED, MetricType::DECODE_COMPLETED};
}
//==============================================================================
std::vector<Metric> GetCompletionTimeSeriesMetrics() {
  std::vector<Metric> metrics;
  for (MetricType metric_type : GetCompletionTimeSeriesMetricsTypes()) {
    metrics.emplace_back(metric_type, UnitType::SECONDS, false,
                         PlotType::TIME_SERIES, std::nullopt, std::nullopt,
                         std::nullopt);
  }

  return metrics;
}
//==============================================================================
std::vector<Metric> GetAllMetrics(bool write_metrics,
                                  bool keep_individual_batch_metrics,
                                  bool enable_gpu_op_level_metrics,
                                  bool enable_cpu_op_level_metrics) {
  if (!write_metrics) {
    return {};
  }

  std::vector<Metric> metrics;

  // Operation metrics
  if (enable_gpu_op_level_metrics) {
    auto gpu_op_metrics = GetGpuOperationMetrics(keep_individual_batch_metrics);
    metrics.insert(metrics.end(), gpu_op_metrics.begin(), gpu_op_metrics.end());
  }
  if (enable_cpu_op_level_metrics) {
    auto cpu_op_metrics = GetCpuOperationMetrics(keep_individual_batch_metrics);
    metrics.insert(metrics.end(), cpu_op_metrics.begin(), cpu_op_metrics.end());
  }

  // Sequence metrics
  auto sequence_metrics = GetSequenceTimeDistributionMetrics();
  metrics.insert(metrics.end(), sequence_metrics.begin(),
                 sequence_metrics.end());
  auto sequence_histogram_metrics = GetSequenceHistogramMetrics();
  metrics.insert(metrics.end(), sequence_histogram_metrics.begin(),
                 sequence_histogram_metrics.end());

  // Batch metrics
  auto batch_count_distribution_metrics =
      GetBatchCountDistributionMetrics(keep_individual_batch_metrics);
  metrics.insert(metrics.end(), batch_count_distribution_metrics.begin(),
                 batch_count_distribution_metrics.end());
  auto batch_time_distribution_metrics =
      GetBatchTimeDistributionMetrics(keep_individual_batch_metrics);
  metrics.insert(metrics.end(), batch_time_distribution_metrics.begin(),
                 batch_time_distribution_metrics.end());

  // Token metrics
  auto token_time_distribution_metrics = GetTokenTimeDistributionMetrics();
  metrics.insert(metrics.end(), token_time_distribution_metrics.begin(),
                 token_time_distribution_metrics.end());
  auto completion_time_series_metrics = GetCompletionTimeSeriesMetrics();
  metrics.insert(metrics.end(), completion_time_series_metrics.begin(),
                 completion_time_series_metrics.end());

  return metrics;
}
//==============================================================================
}  // namespace vajra
//==============================================================================
