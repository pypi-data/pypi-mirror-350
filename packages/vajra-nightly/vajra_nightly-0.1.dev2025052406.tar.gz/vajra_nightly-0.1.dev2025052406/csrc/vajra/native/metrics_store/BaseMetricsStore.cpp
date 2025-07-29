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
#include "native/metrics_store/BaseMetricsStore.h"

#include "commons/Logging.h"
#include "native/metrics_store/MetricGroups.h"
//==============================================================================
namespace vajra {
//==============================================================================
BaseMetricsStore::BaseMetricsStore(
    const MetricsConfig& config, const CdfDataStores& cdf_datastores,
    const TimeSeriesDataStores& time_series_datastores,
    const std::shared_ptr<ChromeTracer>& chrome_tracer)
    : disabled_(false),
      config_(config),
      plots_dir_(config.output_dir + "/plots/"),
      num_decoded_tokens_(0) {
  ASSERT_VALID_POINTER_ARGUMENT(chrome_tracer);

  // Initialize datastores
  cdf_datastores_ = cdf_datastores;
  time_series_datastores_ = time_series_datastores;

  // Initialize chrome tracer
  chrome_tracer_ = chrome_tracer;

  // Get all metrics
  if (!config_.write_metrics) {
    LOG_INFO("Metrics are disabled");
    disabled_ = true;
    return;
  }
  // Get metric types
  gpu_op_metrics_types_ = GetGpuOperationMetricsTypes();
  cpu_op_metrics_types_ = GetCpuOperationMetricsTypes();

  // Timing variables
  last_request_arrived_at_ = std::nullopt;
  last_batch_end_time_ = std::nullopt;
  num_decoded_tokens_ = 0;
  scheduler_output_id_.clear();

  // Start the worker thread
  worker_thread_ = std::thread(&BaseMetricsStore::WorkerLoop, this);
}
//==============================================================================
BaseMetricsStore::~BaseMetricsStore() {
  if (worker_thread_.joinable()) {
    // Signal the worker thread to stop
    stop_worker_.store(true);
    // Enqueue an empty task to wake up the worker thread if it's waiting
    task_queue_.push({});
    // Wait for the worker thread to finish
    worker_thread_.join();
  }
}
//==============================================================================
bool BaseMetricsStore::ShouldWriteMetrics() const {
  return config_.write_metrics;
}
//==============================================================================
bool BaseMetricsStore::IsEnabled() const { return !disabled_; }
//==============================================================================
void BaseMetricsStore::Reset() {
  RETURN_IF_METRICS_DISABLED();
  // Reset timing variables
  last_request_arrived_at_ = std::nullopt;
  last_batch_end_time_ = std::nullopt;
  num_decoded_tokens_ = 0;
  scheduler_output_id_.clear();
}
//==============================================================================
void BaseMetricsStore::PushCpuOperationMetric(MetricType metric_type,
                                              TimeS time) {
  RETURN_IF_METRICS_DISABLED();

  // Put the metric into the appropriate datastore
  cdf_datastores_.at(metric_type)->Put(scheduler_output_id_, time);
}
//==============================================================================
//                   Protected and Private Methods
//==============================================================================
void BaseMetricsStore::WorkerLoop() {
  LOG_INFO("Metrics worker thread started.");
  while (!stop_worker_.load()) {
    Task task;
    // Wait for a task to become available
    task_queue_.wait_pull(task);

    // Check for stop signal after potentially being woken up by an empty task
    if (stop_worker_.load()) {
      break;
    }

    // Execute the task
    if (task) {
      try {
        task();
      } catch (const std::exception& e) {
        throw std::runtime_error(
            std::format("Exception in metrics worker thread: {}", e.what()));
      } catch (...) {
        throw std::runtime_error("Unknown exception in metrics worker thread.");
      }
    }
  }
  LOG_INFO("Metrics worker thread stopped.");
}
//==============================================================================
}  // namespace vajra
//==============================================================================
