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
#include "native/core/scheduler/replica_schedulers/FixedChunkReplicaScheduler.h"
//==============================================================================
#include "native/configs/ReplicaSchedulerConfig.h"
//==============================================================================
namespace vajra {
//==============================================================================
FixedChunkReplicaScheduler::FixedChunkReplicaScheduler(
    const ModelConfig& model_config,
    const std::shared_ptr<const FixedChunkReplicaSchedulerConfig>&
        scheduler_config,
    const CacheConfig& cache_config, const ParallelConfig& parallel_config,
    std::size_t num_gpu_blocks, SequencePriorityQueuePtr waiting_queue,
    std::shared_ptr<BaseRequestPrioritizer> request_prioritizer)
    : BaseReplicaScheduler(model_config, scheduler_config, cache_config,
                           parallel_config, num_gpu_blocks, waiting_queue,
                           request_prioritizer) {
  ASSERT_VALID_POINTER_ARGUMENT(scheduler_config);
  ASSERT_VALID_POINTER_ARGUMENT(waiting_queue);
  ASSERT_VALID_POINTER_ARGUMENT(request_prioritizer);
}

std::size_t FixedChunkReplicaScheduler::GetSeqNextNumQTokens(
    const MutableSequencePtr& seq,
    [[maybe_unused]] const BatchFormationTracker& batch_formation_tracker)
    const {
  ASSERT_VALID_POINTER_ARGUMENT(seq);

  // Ensure sequence is in the right state
  ASSERT_VALID_RUNTIME(!seq->IsFinished(),
                       "Sequence {} should not be in finished state",
                       seq->seq_id);
  ASSERT_VALID_RUNTIME(
      !seq->GetPromptStageProcessingFinished(),
      "Sequence {} should not have GetPromptStageProcessingFinished() set",
      seq->seq_id);

  // Get the config with proper type
  const auto* config = GetSchedulerConfig().get();

  // Get batch tracker query tokens across groups for the sequence
  std::vector<std::size_t> batched_num_q_tokens_across_groups =
      kvp_state_tracker_->GetBatchTrackerQTokens(seq);

  // Find the maximum number of query tokens across groups
  std::size_t max_num_q_tokens_across_groups = 0;
  if (!batched_num_q_tokens_across_groups.empty()) {
    max_num_q_tokens_across_groups =
        *std::max_element(batched_num_q_tokens_across_groups.begin(),
                          batched_num_q_tokens_across_groups.end());
  }

  // Get the number of tokens already processed for this sequence
  std::size_t num_processed_tokens = seq->GetNumTokensStageProcessed();

  // Calculate the next number of tokens based on the fixed chunk size and
  // already processed tokens
  std::size_t next_num_tokens =
      std::min(seq->GetPromptLength() - num_processed_tokens,
               config->GetMaxChunkSize() - max_num_q_tokens_across_groups);

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
