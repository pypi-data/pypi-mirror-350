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
#include "commons/TorchCommon.h"
#include "native/datatypes/SchedulerOutput.h"
#include "native/datatypes/SequenceMetadata.h"
#include "native/metrics_store/BaseMetricsStore.h"
//==============================================================================
namespace vajra {
//==============================================================================
// Constant for layer to profile
constexpr int PROFILE_LAYER_ID = 1;
//==============================================================================
using CudaEventPtr = std::shared_ptr<at::cuda::CUDAEvent>;
//==============================================================================
struct CudaEventPair final {
  CudaEventPtr start;
  CudaEventPtr end;

  CudaEventPair(CudaEventPtr s, CudaEventPtr e)
      : start(std::move(s)), end(std::move(e)) {
    ASSERT_VALID_POINTER_ARGUMENT(s);
    ASSERT_VALID_POINTER_ARGUMENT(e);
  }
};

class WorkerMetricsStore : public BaseMetricsStore {
 public:
  // Constructor
  explicit WorkerMetricsStore(
      const MetricsConfig& config, const CdfDataStores& cdf_datastores,
      const TimeSeriesDataStores& time_series_datastores,
      const std::shared_ptr<ChromeTracer>& chrome_tracer,
      const std::size_t rank);

  // Virtual destructor
  ~WorkerMetricsStore() override = default;

  void Reset();

  // Override IsOperationEnabled
  bool IsOperationEnabled(MetricType metric_type) override;

  // Extended version with additional parameters
  bool IsOperationEnabled(MetricType metric_type, std::optional<int> layer_id);

  // Metrics recording methods
  void OnBatchStageStart(const SchedulerOutputPtr& scheduler_output);

  void OnBatchStageEnd(const ReplicaId replica_id,
                       const SequenceMetadataVector& seq_metadata_list,
                       int tensor_parallel_rank, int pipeline_parallel_rank,
                       int kv_parallel_rank, double start_time,
                       double end_time);

  // CUDA event methods
  void PushGpuOperationMetricCudaEvents(MetricType metric_type,
                                        CudaEventPtr start_event,
                                        CudaEventPtr end_event);

  void PushGpuOperationMetric(MetricType metric_type, float time);

 private:
  // Process pending CUDA events
  void ProcessPendingOperationMetricCudaEvents();

  // Private Implementation Methods for async execution
  void OnBatchStageStartImpl(const SchedulerOutputPtr& scheduler_output);
  void OnBatchStageEndImpl(const ReplicaId replica_id,
                           const SequenceMetadataVector& seq_metadata_list,
                           int tensor_parallel_rank, int pipeline_parallel_rank,
                           int kv_parallel_rank, double start_time,
                           double end_time);

  // Pending CUDA events with pre-computed elapsed times
  std::unordered_map<MetricType, std::vector<CudaEventPair>>
      gpu_ops_metrics_pending_events_;
};
//==============================================================================
using WorkerMetricsStorePtr = std::shared_ptr<WorkerMetricsStore>;
//==============================================================================
}  // namespace vajra
//==============================================================================
