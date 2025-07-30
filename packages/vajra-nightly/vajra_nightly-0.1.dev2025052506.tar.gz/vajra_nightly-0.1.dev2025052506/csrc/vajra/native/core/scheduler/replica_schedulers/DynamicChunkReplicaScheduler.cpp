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
#include "native/core/scheduler/replica_schedulers/DynamicChunkReplicaScheduler.h"
//==============================================================================
#include "native/configs/ReplicaSchedulerConfig.h"
//==============================================================================
namespace vajra {
//==============================================================================
DynamicChunkReplicaScheduler::DynamicChunkReplicaScheduler(
    const ModelConfig& model_config,
    const std::shared_ptr<const DynamicChunkReplicaSchedulerConfig>&
        scheduler_config,
    const CacheConfig& cache_config, const ParallelConfig& parallel_config,
    std::size_t num_gpu_blocks, SequencePriorityQueuePtr waiting_queue,
    std::shared_ptr<BaseRequestPrioritizer> request_prioritizer,
    std::shared_ptr<vidur::execution_time_predictor::ExecutionTimePredictor>
        execution_time_predictor)
    : BaseReplicaScheduler(model_config, scheduler_config, cache_config,
                           parallel_config, num_gpu_blocks, waiting_queue,
                           request_prioritizer),
      execution_time_predictor_(execution_time_predictor) {
  ASSERT_VALID_POINTER_ARGUMENT(execution_time_predictor);
  ASSERT_VALID_POINTER_ARGUMENT(scheduler_config);
  ASSERT_VALID_POINTER_ARGUMENT(waiting_queue);
  ASSERT_VALID_POINTER_ARGUMENT(request_prioritizer);
}
//==============================================================================

std::shared_ptr<BatchFormationTracker>
DynamicChunkReplicaScheduler::GetBatchFormationTracker() {
  // Get the config with proper type
  const auto* config = GetSchedulerConfig().get();

  // Create and return the BatchFormationTrackerWithRuntimePrediction
  return std::make_shared<BatchFormationTrackerWithRuntimePrediction>(
      iteration_id_, config->GetMaxBatchSize(),
      parallel_config_.pipeline_parallel_size, kvp_state_tracker_,
      config->GetMaxChunkSize(), config->GetMinChunkSize(),
      execution_time_predictor_);
}
//==============================================================================

std::size_t DynamicChunkReplicaScheduler::GetSeqNextNumQTokens(
    const MutableSequencePtr& seq,
    const BatchFormationTracker& batch_formation_tracker) const {
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

  // Cast the batch formation tracker to the runtime prediction type
  ASSERT_VALID_RUNTIME(typeid(batch_formation_tracker) ==
                           typeid(BatchFormationTrackerWithRuntimePrediction),
                       "batch_formation_tracker must be a "
                       "BatchFormationTrackerWithRuntimePrediction");
  const auto* runtime_tracker =
      static_cast<const BatchFormationTrackerWithRuntimePrediction*>(
          &batch_formation_tracker);

  // Get the active KVP group IDs for this sequence
  std::vector<std::size_t> active_kvp_group_ids =
      kvp_state_tracker_->GetActiveKvpGroupIds(seq);

  // Get the maximum chunk size for this sequence based on target batch time
  std::size_t next_num_tokens = runtime_tracker->GetMaxChunkSizeForSeq(
      seq, active_kvp_group_ids, config->GetTargetBatchTime());

  // Adjust for KV parallelism if needed
  std::size_t num_processed_tokens = seq->GetNumTokensStageProcessed();
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
