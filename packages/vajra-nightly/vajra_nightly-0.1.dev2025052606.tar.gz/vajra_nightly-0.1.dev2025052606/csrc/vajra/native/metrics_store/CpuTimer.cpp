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
#include "native/metrics_store/CpuTimer.h"
//==============================================================================
namespace vajra {
//==============================================================================
CpuTimer::CpuTimer(std::optional<MetricType> metric_type,
                   std::shared_ptr<BaseMetricsStore> metrics_store)
    : metric_type_(metric_type),
      metrics_store_(metrics_store),
      disabled_(false) {
  ASSERT_VALID_POINTER_ARGUMENT(metrics_store);

  // Check if metrics are disabled

  if (!metric_type_.has_value()) {
    disabled_ = true;
    return;
  }

  // Check if this operation is enabled in the metrics store
  disabled_ = !metrics_store_->IsOperationEnabled(metric_type_.value());
}
//==============================================================================
void CpuTimer::Start() {
  if (disabled_) {
    return;
  }

  start_time_ = time_utils::now_s();
}

//==============================================================================
void CpuTimer::Stop() {
  if (disabled_) {
    return;
  }

  // Create and record end event
  end_time_ = time_utils::now_s();

  // Push events to metrics store
  if (metric_type_.has_value()) {
    metrics_store_->PushCpuOperationMetric(metric_type_.value(),
                                           end_time_ - start_time_);
  }
}
//==============================================================================
}  // namespace vajra
//==============================================================================
