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
#include "native/metrics_store/WorkerMetricsStore.h"

#include <ATen/cuda/CUDAEvent.h>

#include "commons/Constants.h"
#include "commons/Logging.h"
#include "native/datatypes/SchedulerOutput.h"
#include "native/metrics_store/MetricGroups.h"
//==============================================================================
// Macro for safely putting data into a metrics datastore
// Usage: PUT_METRIC(map, metric_type, key, value)
#define PUT_METRIC(datastore_map, metric_type, key, value) \
  do {                                                     \
    datastore_map.at(metric_type)->Put(key, value);        \
  } while (0)

//==============================================================================
namespace vajra {
//==============================================================================
WorkerMetricsStore::WorkerMetricsStore(
    const MetricsConfig& config, const CdfDataStores& cdf_datastores,
    const TimeSeriesDataStores& time_series_datastores,
    const std::shared_ptr<ChromeTracer>& chrome_tracer, const std::size_t rank)
    : BaseMetricsStore(config, cdf_datastores, time_series_datastores,
                       chrome_tracer) {
  ASSERT_VALID_POINTER_ARGUMENT(chrome_tracer);

  // Constructor initialization is minimal as most is handled by
  // BaseMetricsStore
  if (rank != ROOT_RANK) {
    disabled_ = true;
    // If disabled, don't initialize pending events or start worker
    return;
  }
  gpu_ops_metrics_pending_events_.clear();
  for (const auto& metric_type : gpu_op_metrics_types_) {
    gpu_ops_metrics_pending_events_[metric_type] = std::vector<CudaEventPair>();
  }
}
//==============================================================================
void WorkerMetricsStore::Reset() {
  RETURN_IF_METRICS_DISABLED();

  // Call the base class Reset first
  BaseMetricsStore::Reset();

  // Initialize pending events storage
  gpu_ops_metrics_pending_events_.clear();
  for (const auto& metric_type : gpu_op_metrics_types_) {
    gpu_ops_metrics_pending_events_[metric_type] = std::vector<CudaEventPair>();
  }
}
//==============================================================================
bool WorkerMetricsStore::IsOperationEnabled(MetricType metric_type) {
  // Call the extended version with default parameters
  return IsOperationEnabled(metric_type, std::nullopt);
}
//==============================================================================
bool WorkerMetricsStore::IsOperationEnabled(MetricType metric_type,
                                            std::optional<int> layer_id) {
  if (!IsEnabled() || !ShouldWriteMetrics()) {
    return false;
  }

  // Check for GPU operation metrics
  for (const auto& gpu_metric_type : gpu_op_metrics_types_) {
    if (metric_type == gpu_metric_type) {
      return config_.enable_gpu_op_level_metrics &&
             (layer_id.value_or(-1) == PROFILE_LAYER_ID ||
              !layer_id.has_value());
    }
  }

  // Check for CPU operation metrics
  for (const auto& cpu_metric_type : cpu_op_metrics_types_) {
    if (metric_type == cpu_metric_type) {
      return config_.enable_cpu_op_level_metrics;
    }
  }

  // If we get here, the metric type is unknown
  LOG_ERROR("Unknown metric type: {}", MetricTypeToString(metric_type));
  return false;
}
//==============================================================================
void WorkerMetricsStore::OnBatchStageStart(
    const SchedulerOutputPtr& scheduler_output) {
  RETURN_IF_METRICS_DISABLED();

  ASSERT_VALID_POINTER_ARGUMENT(scheduler_output);
  EnqueueTask(
      [this, scheduler_output]() { OnBatchStageStartImpl(scheduler_output); });
}
//==============================================================================
void WorkerMetricsStore::OnBatchStageEnd(
    const ReplicaId replica_id, const SequenceMetadataVector& seq_metadata_list,
    int tensor_parallel_rank, int pipeline_parallel_rank, int kv_parallel_rank,
    double start_time, double end_time) {
  EnqueueTask([this, replica_id, seq_metadata_list, tensor_parallel_rank,
               pipeline_parallel_rank, kv_parallel_rank, start_time,
               end_time]() {
    OnBatchStageEndImpl(replica_id, seq_metadata_list, tensor_parallel_rank,
                        pipeline_parallel_rank, kv_parallel_rank, start_time,
                        end_time);
  });
}
//==============================================================================
void WorkerMetricsStore::PushGpuOperationMetricCudaEvents(
    MetricType metric_type, CudaEventPtr start_event, CudaEventPtr end_event) {
  RETURN_IF_METRICS_DISABLED();

  ASSERT_VALID_POINTER_ARGUMENT(start_event);
  ASSERT_VALID_POINTER_ARGUMENT(end_event);

  auto it = gpu_ops_metrics_pending_events_.find(metric_type);
  if (it != gpu_ops_metrics_pending_events_.end()) {
    it->second.push_back(
        CudaEventPair{std::move(start_event), std::move(end_event)});
  }
}
//==============================================================================
void WorkerMetricsStore::PushGpuOperationMetric(MetricType metric_type,
                                                float time) {
  RETURN_IF_METRICS_DISABLED();

  PUT_METRIC(cdf_datastores_, metric_type, scheduler_output_id_, time);
}
//==============================================================================
void WorkerMetricsStore::ProcessPendingOperationMetricCudaEvents() {
  RETURN_IF_METRICS_DISABLED();

  for (auto& [metric_type, events] : gpu_ops_metrics_pending_events_) {
    for (auto& pair : events) {
      pair.start->synchronize();
      pair.end->synchronize();

      // Measure the time
      float elapsed_time_ms = pair.start->elapsed_time(*pair.end);
      PushGpuOperationMetric(metric_type, elapsed_time_ms);
    }
    events.clear();
  }
}
//==============================================================================
//                        Private Implementation Methods
//==============================================================================
void WorkerMetricsStore::OnBatchStageStartImpl(
    const SchedulerOutputPtr& scheduler_output) {
  RETURN_IF_METRICS_DISABLED();

  ASSERT_VALID_POINTER_ARGUMENT(scheduler_output);

  scheduler_output_id_ = std::to_string(scheduler_output->id);
}
//==============================================================================
void WorkerMetricsStore::OnBatchStageEndImpl(
    const ReplicaId replica_id, const SequenceMetadataVector& seq_metadata_list,
    int tensor_parallel_rank, int pipeline_parallel_rank, int kv_parallel_rank,
    double start_time, double end_time) {
  RETURN_IF_METRICS_DISABLED();

  ProcessPendingOperationMetricCudaEvents();

  if (!config_.enable_chrome_trace) {
    return;
  }

  // Use the chrome tracer to record the event
  chrome_tracer_->Put(seq_metadata_list, replica_id, tensor_parallel_rank,
                      pipeline_parallel_rank, kv_parallel_rank, start_time,
                      end_time);
}
//==============================================================================
}  // namespace vajra
//==============================================================================
