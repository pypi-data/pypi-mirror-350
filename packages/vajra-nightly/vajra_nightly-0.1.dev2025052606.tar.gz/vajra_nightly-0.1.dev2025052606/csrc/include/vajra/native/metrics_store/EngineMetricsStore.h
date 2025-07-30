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
#include "native/datatypes/SchedulerOutput.h"
#include "native/datatypes/Sequence.h"
#include "native/metrics_store/BaseMetricsStore.h"
//==============================================================================
namespace vajra {
//==============================================================================
class EngineMetricsStore : public BaseMetricsStore {
 public:
  // Constructor
  explicit EngineMetricsStore(
      const MetricsConfig& config, const CdfDataStores& cdf_datastores,
      const TimeSeriesDataStores& time_series_datastores,
      const std::shared_ptr<ChromeTracer>& chrome_tracer);

  // Virtual destructor
  ~EngineMetricsStore() override = default;

  // Override IsOperationEnabled
  bool IsOperationEnabled(MetricType metric_type) override;

  // Metrics recording methods
  void OnRequestArrival(const std::string& seq_id, TimeS arrival_time);
  void OnRequestEnd(const SequencePtr& seq);
  void OnSchedule(const ReplicaId replica_id,
                  const SchedulerOutputPtr& scheduler_output, TimeS start_time,
                  TimeS end_time);
  void OnBatchEnd(const Sequences& seqs,
                  const SchedulerOutputPtr& scheduler_output,
                  TimeS batch_start_time, TimeS batch_end_time);

 private:
  // Helper methods
  void LogCdfHistogramsOnRequestEnd(const SequencePtr& seq);
  void LogTimeDistributionsOnRequestEnd(const SequencePtr& seq);
  void UpdatePerTokenExecutionTimes(TimeS batch_end_time,
                                    const SequencePtr& seq);

  // Private Implementation Methods for async execution
  void OnRequestArrivalImpl(const std::string& seq_id, TimeS arrival_time);
  void OnRequestEndImpl(const SequencePtr& seq);
  void OnScheduleImpl(const ReplicaId replica_id,
                      const SchedulerOutputPtr& scheduler_output,
                      TimeS start_time, TimeS end_time);
  void OnBatchEndImpl(const Sequences& seqs,
                      const SchedulerOutputPtr& scheduler_output,
                      TimeS batch_start_time, TimeS batch_end_time);
};

using EngineMetricsStorePtr = std::shared_ptr<EngineMetricsStore>;
//==============================================================================
}  // namespace vajra
//==============================================================================
