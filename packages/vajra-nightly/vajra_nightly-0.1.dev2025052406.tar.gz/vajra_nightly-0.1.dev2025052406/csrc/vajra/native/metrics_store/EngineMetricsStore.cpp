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
#include "native/metrics_store/EngineMetricsStore.h"

#include "commons/Logging.h"
#include "commons/Time.h"
#include "native/metrics_store/MetricGroups.h"
//==============================================================================
// Usage: PUT_METRIC(map, metric_type, key, value)
#define PUT_METRIC(datastore_map, metric_type, key, value) \
  datastore_map.at(metric_type)->Put(key, value)

// Macro for putting data with additional condition check
#define PUT_METRIC_IF(datastore_map, metric_type, key, value, condition) \
  if (condition) {                                                       \
    datastore_map.at(metric_type)->Put(key, value);                      \
  }

// Macro for putting data with try-catch handling
#define PUT_METRIC_TRY(datastore_map, metric_type, key, getter_func, \
                       error_msg)                                    \
  try {                                                              \
    datastore_map.at(metric_type)->Put(key, getter_func);            \
  } catch (const std::exception& e) {                                \
    LOG_ERROR(error_msg, e.what());                                  \
  }

//==============================================================================
namespace vajra {
//==============================================================================
EngineMetricsStore::EngineMetricsStore(
    const MetricsConfig& config, const CdfDataStores& cdf_datastores,
    const TimeSeriesDataStores& time_series_datastores,
    const std::shared_ptr<ChromeTracer>& chrome_tracer)
    : BaseMetricsStore(config, cdf_datastores, time_series_datastores,
                       chrome_tracer) {
  // Constructor is minimal as most initialization is handled by
  // BaseMetricsStore
  ASSERT_VALID_POINTER_ARGUMENT(chrome_tracer);
}
//==============================================================================
bool EngineMetricsStore::IsOperationEnabled(MetricType metric_type) {
  if (!IsEnabled()) {
    return false;
  }

  // Check if the metric type is a CPU operation metric
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
void EngineMetricsStore::OnRequestArrival(const std::string& seq_id,
                                          TimeS arrival_time) {
  // Enqueue the task for asynchronous execution
  EnqueueTask([this, seq_id, arrival_time]() {
    OnRequestArrivalImpl(seq_id, arrival_time);
  });
}
//==============================================================================
void EngineMetricsStore::OnRequestEnd(const SequencePtr& seq) {
  RETURN_IF_METRICS_DISABLED();

  ASSERT_VALID_POINTER_ARGUMENT(seq);

  // Capture the sequence by shared pointer to ensure lifetime
  EnqueueTask([this, seq]() { OnRequestEndImpl(seq); });
}
//==============================================================================
void EngineMetricsStore::OnSchedule(const ReplicaId replica_id,
                                    const SchedulerOutputPtr& scheduler_output,
                                    TimeS start_time, TimeS end_time) {
  RETURN_IF_METRICS_DISABLED();

  ASSERT_VALID_POINTER_ARGUMENT(scheduler_output);

  // LOG_INFO("OnSchedule Async call Time passed since end_time: {}",
  //  (time_utils::now_s() - end_time) * 1e6);
  // Capture scheduler_output by shared pointer
  EnqueueTask([this, replica_id, scheduler_output, start_time, end_time]() {
    OnScheduleImpl(replica_id, scheduler_output, start_time, end_time);
  });
}
//==============================================================================
void EngineMetricsStore::OnBatchEnd(const Sequences& seqs,
                                    const SchedulerOutputPtr& scheduler_output,
                                    TimeS batch_start_time,
                                    TimeS batch_end_time) {
  RETURN_IF_METRICS_DISABLED();

  ASSERT_VALID_POINTER_ARGUMENT(scheduler_output);

  // Capture sequences and scheduler_output by shared pointers/copy
  // Note: Capturing 'seqs' by value might be expensive if it's large.
  // If performance is critical, consider capturing shared_ptrs if seqs
  // contains them, or rethink the data structure.
  EnqueueTask([this, seqs, scheduler_output, batch_start_time,
               batch_end_time]() {  // Capture seqs by value (copy)
    OnBatchEndImpl(seqs, scheduler_output, batch_start_time, batch_end_time);
  });
}

//==============================================================================
//                        Private Implementation Methods
//==============================================================================
void EngineMetricsStore::OnRequestArrivalImpl(const std::string& seq_id,
                                              TimeS arrival_time) {
  RETURN_IF_METRICS_DISABLED();

  // Time series metric
  PUT_METRIC(time_series_datastores_, MetricType::REQUEST_ARRIVED, arrival_time,
             1);

  // CDF metric - only put if last request time is available
  PUT_METRIC_IF(cdf_datastores_, MetricType::REQUEST_INTER_ARRIVAL_DELAY,
                seq_id, arrival_time - last_request_arrived_at_.value(),
                last_request_arrived_at_.has_value());

  // Critical section: Update shared state
  // This needs protection if accessed by other threads, but here it's only
  // accessed by the single worker thread.
  last_request_arrived_at_ = arrival_time;
}
//==============================================================================
void EngineMetricsStore::OnRequestEndImpl(const SequencePtr& seq) {
  RETURN_IF_METRICS_DISABLED();

  ASSERT_VALID_POINTER_ARGUMENT(seq);

  // Check that sequence is finished and completed
  ASSERT_VALID_ARGUMENTS(seq->IsFinished(), "Sequence is not finished");

  // Log time series metrics
  PUT_METRIC(time_series_datastores_, MetricType::REQUEST_COMPLETED,
             seq->GetState().GetCompletedAt(), 1);

  // Log CDF metrics for ignored requests
  PUT_METRIC(cdf_datastores_, MetricType::REQUEST_NUM_IGNORED, seq->seq_id,
             seq->GetState().GetIsIgnoreFinished() ? 1 : 0);

  if (seq->GetState().GetIsIgnoreFinished()) {
    // Do not log metrics for ignored requests, they can skew the results
    return;
  }

  // Log CDF histograms
  LogCdfHistogramsOnRequestEnd(seq);

  // Log time distributions
  LogTimeDistributionsOnRequestEnd(seq);
}
//==============================================================================
void EngineMetricsStore::OnScheduleImpl(
    const ReplicaId replica_id, const SchedulerOutputPtr& scheduler_output,
    double start_time, double end_time) {
  RETURN_IF_METRICS_DISABLED();

  // Critical section: Update shared state
  scheduler_output_id_ = scheduler_output->id;

  if (!config_.enable_chrome_trace) {
    return;
  }

  // Use the dedicated method for logging scheduler events
  chrome_tracer_->PutSchedulerEvent(
      replica_id, scheduler_output->id,
      scheduler_output->seq_schedule_metadata_list, start_time, end_time);
}
//==============================================================================
void EngineMetricsStore::OnBatchEndImpl(
    const Sequences& seqs, const SchedulerOutputPtr& scheduler_output,
    TimeS batch_start_time, TimeS batch_end_time) {
  RETURN_IF_METRICS_DISABLED();

  TimeS execution_time = batch_end_time - batch_start_time;

  // Process each sequence
  for (const auto& seq : seqs) {
    ASSERT_VALID_POINTER_ARGUMENT(seq);

    UpdatePerTokenExecutionTimes(batch_end_time, seq);
    // Call the Impl version if OnRequestEnd is also async
    if (seq->IsFinished()) {
      OnRequestEndImpl(seq);
    }
  }

  // Record inter-batch delay - only if we have a previous batch end time
  PUT_METRIC_IF(cdf_datastores_, MetricType::INTER_BATCH_DELAY,
                std::to_string(scheduler_output->id),
                batch_start_time - last_batch_end_time_.value(),
                last_batch_end_time_.has_value());

  // Critical section: Update shared state
  last_batch_end_time_ = batch_end_time;

  // Calculate token counts
  int num_tokens = 0;
  int num_prompt_tokens = 0;

  for (const auto& metadata : scheduler_output->seq_schedule_metadata_list) {
    num_tokens += metadata->num_q_tokens;
    if (metadata->num_q_tokens > 1) {
      num_prompt_tokens += metadata->num_q_tokens;
    }
  }
  int num_output_tokens = num_tokens - num_prompt_tokens;

  // Record batch metrics
  PUT_METRIC(cdf_datastores_, MetricType::BATCH_NUM_TOKENS,
             std::to_string(scheduler_output->id), num_tokens);

  PUT_METRIC(cdf_datastores_, MetricType::BATCH_NUM_PREFILL_TOKENS,
             std::to_string(scheduler_output->id), num_prompt_tokens);

  PUT_METRIC(cdf_datastores_, MetricType::BATCH_NUM_DECODE_TOKENS,
             std::to_string(scheduler_output->id), num_output_tokens);

  PUT_METRIC(cdf_datastores_, MetricType::BATCH_SIZE,
             std::to_string(scheduler_output->id), seqs.size());

  PUT_METRIC(cdf_datastores_, MetricType::BATCH_EXECUTION_TIME,
             std::to_string(scheduler_output->id), execution_time);
}
//==============================================================================
void EngineMetricsStore::LogCdfHistogramsOnRequestEnd(const SequencePtr& seq) {
  RETURN_IF_METRICS_DISABLED();

  ASSERT_VALID_POINTER_ARGUMENT(seq);

  // Token counts
  PUT_METRIC(cdf_datastores_, MetricType::REQUEST_NUM_TOKENS, seq->seq_id,
             seq->GetState().GetNumTotalTokens());
  PUT_METRIC(cdf_datastores_, MetricType::REQUEST_PREFILL_TOKENS, seq->seq_id,
             seq->GetState().GetNumPromptTokens());
  PUT_METRIC(cdf_datastores_, MetricType::REQUEST_DECODE_TOKENS, seq->seq_id,
             seq->GetState().GetNumOutputTokens());

  // Only compute ratio if output tokens > 0 to avoid division by zero
  PUT_METRIC_IF(cdf_datastores_, MetricType::REQUEST_PD_RATIO, seq->seq_id,
                static_cast<float>(seq->GetState().GetNumPromptTokens()) /
                    seq->GetState().GetNumOutputTokens(),
                seq->GetState().GetNumOutputTokens() > 0);

  PUT_METRIC(cdf_datastores_, MetricType::REQUEST_NUM_RESTARTS, seq->seq_id,
             seq->GetState().GetNumRestarts());
  PUT_METRIC(cdf_datastores_, MetricType::REQUEST_NUM_PAUSES, seq->seq_id,
             seq->GetState().GetNumPauses());
}
//==============================================================================
void EngineMetricsStore::LogTimeDistributionsOnRequestEnd(
    const SequencePtr& seq) {
  RETURN_IF_METRICS_DISABLED();

  ASSERT_VALID_POINTER_ARGUMENT(seq);

  const auto& state = seq->GetState();

  // E2E times
  PUT_METRIC(cdf_datastores_, MetricType::REQUEST_E2E_TIME, seq->seq_id,
             state.GetE2ETime());
  PUT_METRIC(cdf_datastores_, MetricType::REQUEST_E2E_TIME_NORMALIZED,
             seq->seq_id, state.GetE2ETimeNormalized());
  PUT_METRIC(cdf_datastores_, MetricType::REQUEST_E2E_TIME_PIECEWISE_NORMALIZED,
             seq->seq_id, state.GetE2ETimePiecewiseNormalized());

  // Execution and preemption times
  PUT_METRIC(cdf_datastores_,
             MetricType::REQUEST_EXECUTION_PLUS_PREEMPTION_TIME, seq->seq_id,
             state.GetExecutionPlusPreemptionTime());
  PUT_METRIC(cdf_datastores_,
             MetricType::REQUEST_EXECUTION_PLUS_PREEMPTION_TIME_NORMALIZED,
             seq->seq_id, state.GetExecutionPlusPreemptionTimeNormalized());

  auto delay = state.GetSchedulingDelay();
  PUT_METRIC_IF(cdf_datastores_, MetricType::REQUEST_SCHEDULING_DELAY,
                seq->seq_id, delay, delay >= 0);

  PUT_METRIC(cdf_datastores_, MetricType::REQUEST_EXECUTION_TIME, seq->seq_id,
             state.GetExecutionTime());
  PUT_METRIC(cdf_datastores_, MetricType::REQUEST_EXECUTION_TIME_NORMALIZED,
             seq->seq_id, state.GetExecutionTimeNormalized());
  PUT_METRIC(cdf_datastores_, MetricType::REQUEST_PREEMPTION_TIME, seq->seq_id,
             state.GetPreemptedTime());

  // Prefill times
  PUT_METRIC_TRY(cdf_datastores_, MetricType::PREFILL_TIME_E2E, seq->seq_id,
                 state.GetE2EPrefillTime(),
                 "Failed to get E2E prefill time: {}");

  PUT_METRIC_TRY(cdf_datastores_, MetricType::PREFILL_TIME_E2E_NORMALIZED,
                 seq->seq_id, state.GetE2EPrefillTimeNormalized(),
                 "Failed to get E2E prefill time normalized: {}");

  PUT_METRIC_TRY(cdf_datastores_,
                 MetricType::PREFILL_TIME_E2E_PIECEWISE_NORMALIZED, seq->seq_id,
                 state.GetE2EPrefillTimePiecewiseNormalized(),
                 "Failed to get E2E prefill time piecewise normalized: {}");

  // Execution plus preemption times
  PUT_METRIC(cdf_datastores_,
             MetricType::PREFILL_TIME_EXECUTION_PLUS_PREEMPTION, seq->seq_id,
             state.GetPrefillExecutionPlusPreemptionTime());

  PUT_METRIC_TRY(
      cdf_datastores_,
      MetricType::PREFILL_TIME_EXECUTION_PLUS_PREEMPTION_NORMALIZED,
      seq->seq_id, state.GetPrefillExecutionPlusPreemptionTimeNormalized(),
      "Failed to get prefill execution plus preemption time normalized: {}");

  PUT_METRIC_TRY(
      cdf_datastores_,
      MetricType::DECODE_TIME_EXECUTION_PLUS_PREEMPTION_NORMALIZED, seq->seq_id,
      state.GetDecodeExecutionPlusPreemptionTimeNormalized(),
      "Failed to get decode execution plus preemption time normalized: {}");
}
//==============================================================================
void EngineMetricsStore::UpdatePerTokenExecutionTimes(TimeS batch_end_time,
                                                      const SequencePtr& seq) {
  RETURN_IF_METRICS_DISABLED();

  ASSERT_VALID_POINTER_ARGUMENT(seq);

  // Determine if this was prefill or decode token
  if (!seq->GetPromptProcessingFinished()) {
    return;
  }

  // Critical section: Update shared state
  num_decoded_tokens_++;

  // If prefill has just finished in this iteration, update the prefill
  // completion timeseries
  if (seq->GetOutputLength() == 1) {
    PUT_METRIC(time_series_datastores_, MetricType::PREFILL_COMPLETED,
               batch_end_time, seq->GetState().GetNumPromptTokens());
  }

  PUT_METRIC(cdf_datastores_,
             MetricType::DECODE_TOKEN_EXECUTION_PLUS_PREEMPTION_TIME,
             std::to_string(num_decoded_tokens_),
             seq->GetState().GetLastTokenGenerationTime());

  // Only log individual batch metrics if configured
  PUT_METRIC_IF(time_series_datastores_, MetricType::DECODE_COMPLETED,
                batch_end_time, 1, config_.keep_individual_batch_metrics);
}
//==============================================================================
}  // namespace vajra
//==============================================================================
