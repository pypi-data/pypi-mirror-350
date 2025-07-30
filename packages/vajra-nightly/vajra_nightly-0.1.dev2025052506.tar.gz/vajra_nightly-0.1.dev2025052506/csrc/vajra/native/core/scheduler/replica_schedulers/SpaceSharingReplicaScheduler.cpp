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
#include "native/core/scheduler/replica_schedulers/SpaceSharingReplicaScheduler.h"
//==============================================================================
#include "native/configs/ReplicaSchedulerConfig.h"
//==============================================================================
namespace vajra {
//==============================================================================
SpaceSharingReplicaScheduler::SpaceSharingReplicaScheduler(
    const ModelConfig& model_config,
    const std::shared_ptr<const SpaceSharingReplicaSchedulerConfig>&
        scheduler_config,
    const CacheConfig& cache_config, const ParallelConfig& parallel_config,
    std::size_t num_gpu_blocks, SequencePriorityQueuePtr waiting_queue,
    std::shared_ptr<BaseRequestPrioritizer> request_prioritizer,
    std::shared_ptr<vidur::execution_time_predictor::ExecutionTimePredictor>
        execution_time_predictor)
    : DynamicChunkReplicaScheduler(model_config, scheduler_config, cache_config,
                                   parallel_config, num_gpu_blocks,
                                   waiting_queue, request_prioritizer,
                                   execution_time_predictor) {
  ASSERT_VALID_POINTER_ARGUMENT(scheduler_config);
  ASSERT_VALID_POINTER_ARGUMENT(waiting_queue);
  ASSERT_VALID_POINTER_ARGUMENT(request_prioritizer);
  ASSERT_VALID_POINTER_ARGUMENT(execution_time_predictor);

  // Verify that the request prioritizer is of the required type
  auto lrs_prioritizer =
      std::dynamic_pointer_cast<LrsRequestPrioritizer>(request_prioritizer);
  ASSERT_VALID_RUNTIME(lrs_prioritizer != nullptr,
                       "SpaceSharingReplicaScheduler can only be used with "
                       "LrsRequestPrioritizer");
}
//==============================================================================

std::size_t SpaceSharingReplicaScheduler::GetSeqNextNumQTokens(
    const MutableSequencePtr& seq,
    const BatchFormationTracker& batch_formation_tracker) const {
  ASSERT_VALID_POINTER_ARGUMENT(seq);

  // Ensure we have the right config type
  const auto* config = GetSchedulerConfig().get();

  // Ensure sequence is in the right state
  ASSERT_VALID_RUNTIME(!seq->IsFinished(),
                       "Sequence {} should not be in finished state",
                       seq->seq_id);
  ASSERT_VALID_RUNTIME(
      !seq->GetPromptStageProcessingFinished(),
      "Sequence {} should not have GetPromptStageProcessingFinished() set",
      seq->seq_id);

  // Get the active KVP group IDs for this sequence
  std::vector<std::size_t> active_kvp_group_ids =
      kvp_state_tracker_->GetActiveKvpGroupIds(seq);

  // Get the number of tokens already processed for this sequence
  std::size_t num_processed_tokens = seq->GetNumTokensStageProcessed();

  // Determine target batch time based on sequence length
  double target_time;

  // Cast the batch formation tracker to the runtime prediction type
  ASSERT_VALID_RUNTIME(typeid(batch_formation_tracker) ==
                           typeid(BatchFormationTrackerWithRuntimePrediction),
                       "batch_formation_tracker must be a "
                       "BatchFormationTrackerWithRuntimePrediction");
  const auto* runtime_tracker =
      static_cast<const BatchFormationTrackerWithRuntimePrediction*>(
          &batch_formation_tracker);

  if (num_processed_tokens < config->GetLongSeqKvCacheLenThreshold()) {
    // For short sequences, use the standard target batch time
    target_time = config->GetTargetBatchTime();
  } else {
    // For long sequences, check if there's another long sequence in the same
    // KVP groups
    bool has_long_seq_in_group = false;

    // Check each KVP group for long sequences
    for (std::size_t kvp_group_id : active_kvp_group_ids) {
      // Check if any sequence in this group is a long sequence
      for (std::size_t processed_tokens :
           kvp_state_tracker_->GetPerGroupNumProcessedTokens(kvp_group_id)) {
        if (processed_tokens > config->GetLongSeqKvCacheLenThreshold()) {
          has_long_seq_in_group = true;
          break;
        }
      }

      if (has_long_seq_in_group) {
        break;
      }
    }

    // Avoid space sharing with another long sequence
    if (has_long_seq_in_group) {
      return 0;
    }

    // Get the sequence with priority from the prioritizer
    auto lrs_prioritizer =
        std::dynamic_pointer_cast<LrsRequestPrioritizer>(request_prioritizer_);
    ASSERT_VALID_RUNTIME(lrs_prioritizer != nullptr,
                         "SpaceSharingReplicaScheduler can only be used with "
                         "LrsRequestPrioritizer");

    // Get the priority (which is the slack fraction in LrsRequestPrioritizer)
    auto seq_with_priority = lrs_prioritizer->GetSeqWithPriority(seq);
    float slack_fraction = seq_with_priority->GetPriority();

    // Apply bounds to the slack fraction
    slack_fraction = std::max(0.0f, slack_fraction);
    slack_fraction = std::min(MAX_SPACE_SHARE_FRAC, slack_fraction);

    // TODO(Amey): We should identify a better way to compute the slack

    // Calculate the adjusted target time with slack
    target_time = config->GetTargetBatchTime() * (1.0 - slack_fraction);
  }

  // Get the maximum chunk size for this sequence based on target batch time
  std::size_t next_num_tokens = runtime_tracker->GetMaxChunkSizeForSeq(
      seq, active_kvp_group_ids, target_time);

  // Adjust for KV parallelism if needed
  if (parallel_config_.kv_parallel_size > 1) {
    std::size_t max_num_tokens_per_kvp_group =
        kvp_state_tracker_->GetMaxNumTokensPerKvpGroup();

    std::size_t last_group_tokens =
        num_processed_tokens % max_num_tokens_per_kvp_group;

    next_num_tokens = std::min(
        next_num_tokens, max_num_tokens_per_kvp_group - last_group_tokens);
  }

  return next_num_tokens;
}
//==============================================================================
}  // namespace vajra
//==============================================================================
