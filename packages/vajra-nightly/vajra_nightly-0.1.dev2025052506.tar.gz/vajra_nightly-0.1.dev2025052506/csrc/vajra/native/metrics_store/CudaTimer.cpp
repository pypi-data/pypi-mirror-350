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
#include "native/metrics_store/CudaTimer.h"
//==============================================================================
namespace vajra {
//==============================================================================
CudaTimer::CudaTimer(std::optional<MetricType> metric_type,
                     std::shared_ptr<WorkerMetricsStore> metrics_store,
                     std::optional<int> layer_id)
    : metric_type_(metric_type),
      metrics_store_(metrics_store),
      layer_id_(layer_id),
      disabled_(false) {
  // Check if metrics are disabled
  if (!metric_type_.has_value() || !metrics_store_) {
    disabled_ = true;
    return;
  }

  // Check if this operation is enabled in the metrics store
  disabled_ =
      !metrics_store_->IsOperationEnabled(metric_type_.value(), layer_id_);
}
//==============================================================================
void CudaTimer::Start() {
  if (disabled_) {
    return;
  }

  // Create and record start event
  start_event_ = std::make_shared<at::cuda::CUDAEvent>(true /*enable_timing*/);
  start_event_->record(at::cuda::getCurrentCUDAStream());
}

//==============================================================================
void CudaTimer::Stop() {
  if (disabled_) {
    return;
  }

  // Create and record end event
  end_event_ = std::make_shared<at::cuda::CUDAEvent>(true /*enable_timing*/);
  end_event_->record(at::cuda::getCurrentCUDAStream());

  // Push events to metrics store
  if (metric_type_.has_value() && start_event_ && end_event_) {
    metrics_store_->PushGpuOperationMetricCudaEvents(metric_type_.value(),
                                                     start_event_, end_event_);
  }
}
//==============================================================================
}  // namespace vajra
//==============================================================================
