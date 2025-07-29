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
#include "native/core/scheduler/replica_schedulers/trackers/BatchFormationTrackerWithRuntimePrediction.h"

using vajra::BatchFormationTrackerWithRuntimePrediction;

BatchFormationTrackerWithRuntimePrediction::
    BatchFormationTrackerWithRuntimePrediction(
        const std::size_t schedule_id, const std::size_t max_micro_batch_size,
        const std::size_t pipeline_parallel_size,
        const std::shared_ptr<KvpStateTracker> kvp_state_tracker,
        const std::size_t max_chunk_size, const std::size_t min_chunk_size,
        const std::shared_ptr<
            vidur::execution_time_predictor::ExecutionTimePredictor>
            execution_time_predictor)
    : BatchFormationTracker(schedule_id, max_micro_batch_size,
                            kvp_state_tracker),
      pipeline_parallel_size_(pipeline_parallel_size),
      execution_time_predictor_(execution_time_predictor),
      max_chunk_size_(max_chunk_size),
      min_chunk_size_(min_chunk_size) {
  ASSERT_VALID_POINTER_ARGUMENT(execution_time_predictor);
  ASSERT_VALID_POINTER_ARGUMENT(kvp_state_tracker);

  // Initialize batch_execution_time_predictions with zeros for each KVP group
  batch_execution_time_predictions_.resize(kvp_state_tracker->GetKvpSize(), 0);
}

void BatchFormationTrackerWithRuntimePrediction::AddSequence(
    const MutableSequencePtr seq, const std::size_t num_q_tokens) {
  ASSERT_VALID_POINTER_ARGUMENT(seq);

  // Call the parent class method
  BatchFormationTracker::AddSequence(seq, num_q_tokens);

  // Skip execution time prediction updates for decode sequences (num_q_tokens
  // == 1)
  if (num_q_tokens == 1) {
    return;
  }

  // Update execution time predictions for all KVP groups
  for (std::size_t kvp_group_id = 0;
       kvp_group_id < kvp_state_tracker_->GetKvpSize(); ++kvp_group_id) {
    batch_execution_time_predictions_[kvp_group_id] =
        ComputeBatchExecutionTime(kvp_group_id);
  }
}

double BatchFormationTrackerWithRuntimePrediction::ComputeBatchExecutionTime(
    std::size_t kvp_group_id, const std::vector<MutableSequencePtr>& extra_seqs,
    const std::vector<std::size_t>& extra_num_q_tokens,
    const std::vector<std::size_t>& extra_num_kv_tokens,
    const std::vector<std::size_t>& extra_num_active_kvp_groups,
    const std::vector<std::size_t>& extra_last_kvp_group_ids) const {
  // Get batch information for the specified KVP group
  auto batch_info =
      kvp_state_tracker_->GetBatchTrackerPerGroupInfo(kvp_group_id);

  // If no sequences and no extra sequences, return 0
  if (batch_info.sequences.empty() && extra_seqs.empty()) {
    return 0;
  }

  // Total number of sequences
  std::size_t num_seqs = batch_info.sequences.size() + extra_seqs.size();

  // Combine existing batch info with extra info
  std::vector<std::size_t> combined_q_tokens = batch_info.q_tokens;
  std::vector<std::size_t> combined_kv_tokens = batch_info.kv_tokens;
  std::vector<std::size_t> combined_active_groups = batch_info.active_group_ids;
  std::vector<std::size_t> combined_last_group_ids = batch_info.last_group_ids;

  // Add the extra info
  combined_q_tokens.insert(combined_q_tokens.end(), extra_num_q_tokens.begin(),
                           extra_num_q_tokens.end());
  combined_kv_tokens.insert(combined_kv_tokens.end(),
                            extra_num_kv_tokens.begin(),
                            extra_num_kv_tokens.end());
  combined_active_groups.insert(combined_active_groups.end(),
                                extra_num_active_kvp_groups.begin(),
                                extra_num_active_kvp_groups.end());
  combined_last_group_ids.insert(combined_last_group_ids.end(),
                                 extra_last_kvp_group_ids.begin(),
                                 extra_last_kvp_group_ids.end());

  // Use Vidur's ExecutionTimePredictor to get execution time
  auto execution_time = execution_time_predictor_->GetExecutionTimeBatch(
      vidur::entities::Batch(0,  // replica_id
                             num_seqs, combined_q_tokens, combined_kv_tokens,
                             combined_active_groups, kvp_group_id),
      0  // pipeline_stage
  );

  // Scale by pipeline_parallel_size
  return execution_time.GetTotalTime() * pipeline_parallel_size_;
}

double BatchFormationTrackerWithRuntimePrediction::GetBatchExecutionTime(
    std::size_t kvp_group_id) const {
  return batch_execution_time_predictions_[kvp_group_id];
}

std::vector<double>
BatchFormationTrackerWithRuntimePrediction::GetBatchExecutionTimeForKvpGroups(
    const std::vector<std::size_t>& kvp_group_ids) const {
  std::vector<double> result;
  result.reserve(kvp_group_ids.size());

  for (std::size_t kvp_group_id : kvp_group_ids) {
    result.push_back(batch_execution_time_predictions_[kvp_group_id]);
  }

  return result;
}

std::size_t BatchFormationTrackerWithRuntimePrediction::GetMaxChunkSizeForSeq(
    const MutableSequencePtr seq,
    const std::vector<std::size_t>& active_kvp_group_ids,
    double target_batch_time) const {
  ASSERT_VALID_POINTER_ARGUMENT(seq);

  // Find the KVP group with the maximum execution time
  std::size_t max_execution_time_group_id = active_kvp_group_ids[0];
  std::size_t max_execution_time = 0;

  for (std::size_t kvp_group_id : active_kvp_group_ids) {
    std::size_t execution_time = GetBatchExecutionTime(kvp_group_id);
    if (execution_time > max_execution_time) {
      max_execution_time = execution_time;
      max_execution_time_group_id = kvp_group_id;
    }
  }

  // Check if current max execution time is already close to target
  if (max_execution_time >
      target_batch_time * (1.0 - EXECUTION_TIME_PREDICTION_SLACK)) {
    return 0;
  }

  // Determine if this is the last group
  bool is_last_group =
      max_execution_time_group_id == active_kvp_group_ids.back();

  // Get the number of processed tokens
  std::size_t num_processed_tokens = seq->GetNumTokensStageProcessed();

  // Get the number of KV tokens
  std::size_t num_kv_tokens =
      GetNumKvTokens(num_processed_tokens, active_kvp_group_ids, is_last_group);
  std::size_t num_kvp_groups = active_kvp_group_ids.size();
  std::size_t last_kvp_group_id = active_kvp_group_ids.back();
  std::size_t remaining_tokens = 0;

  // Use the GetPromptLength() method to get the prompt length
  if (seq->GetPromptLength() > num_processed_tokens) {
    remaining_tokens = seq->GetPromptLength() - num_processed_tokens;
  }

  // Set initial bounds for binary search
  std::size_t high = EXECUTION_TIME_PREDICTION_START_CHUNK_SIZE;

  // Cap high by remaining tokens and round to multiple
  high = RoundDownToNearestMultiple(
      2 * high, EXECUTION_TIME_PREDICTION_CHUNK_SIZE_GRANULARITY);
  high = std::min(remaining_tokens, high);
  std::size_t low = 0;

  // Binary search variables
  std::size_t closest_match = 0;
  double closest_time = 0;
  bool closest_time_set = false;

  // Keep track of chunk sizes we've already tried
  std::unordered_set<std::size_t> seen_chunk_sizes;

  // Binary search with granularity steps
  while (low <= high) {
    std::size_t mid = (low + high) / 2;

    // Apply bounds
    mid = std::min(max_chunk_size_, mid);

    if (mid < remaining_tokens) {
      mid = RoundDownToNearestMultiple(
          mid, EXECUTION_TIME_PREDICTION_CHUNK_SIZE_GRANULARITY);
      if (mid == 0) {
        mid = std::min(min_chunk_size_, remaining_tokens);
      }
    } else {
      mid = remaining_tokens;
    }

    // Check if we've already tried this chunk size
    if (seen_chunk_sizes.find(mid) != seen_chunk_sizes.end()) {
      break;
    }

    seen_chunk_sizes.insert(mid);

    // If mid becomes 0, break
    if (mid == 0) {
      break;
    }

    // Compute execution time with this chunk size
    std::vector<MutableSequencePtr> extra_seqs = {seq};
    std::vector<std::size_t> extra_num_q_tokens = {mid};
    std::vector<std::size_t> extra_num_kv_tokens = {num_kv_tokens};
    std::vector<std::size_t> extra_num_active_kvp_groups = {num_kvp_groups};
    std::vector<std::size_t> extra_last_kvp_group_ids = {last_kvp_group_id};

    std::size_t execution_time = ComputeBatchExecutionTime(
        max_execution_time_group_id, extra_seqs, extra_num_q_tokens,
        extra_num_kv_tokens, extra_num_active_kvp_groups,
        extra_last_kvp_group_ids);

    // Check if execution time is within acceptable range
    if (execution_time >=
            target_batch_time * (1.0 - EXECUTION_TIME_PREDICTION_SLACK) &&
        execution_time <=
            target_batch_time * (1.0 + EXECUTION_TIME_PREDICTION_SLACK)) {
      // Found a good match
      closest_match = mid;
      closest_time = execution_time;
      closest_time_set = true;
      break;
    } else if (execution_time <
               target_batch_time * (1.0 - EXECUTION_TIME_PREDICTION_SLACK)) {
      // Need to increase chunk size
      low = mid + 1;
    } else {
      // Need to decrease chunk size
      high = mid - 1;
    }

    // Update closest match if this is closer to the target
    double current_diff =
        std::abs(static_cast<double>(execution_time) - target_batch_time);
    double best_diff = std::abs(closest_time - target_batch_time);

    if (!closest_time_set || current_diff < best_diff) {
      closest_match = mid;
      closest_time = execution_time;
      closest_time_set = true;
    }
  }

  // TODO(amey): Store the best chunk size in sequence metadata when the feature
  // is available

  return closest_match;
}

[[nodiscard]] std::size_t
BatchFormationTrackerWithRuntimePrediction::GetNumKvTokens(
    std::size_t num_processed_tokens,
    [[maybe_unused]] const std::vector<std::size_t>& active_kvp_group_ids,
    [[maybe_unused]] bool is_last_group) const {
  // TODO(amey): Implement the actual logic for getting the number of KV tokens
  // For now, return a simple implementation matching the Python placeholder
  return num_processed_tokens;
}
