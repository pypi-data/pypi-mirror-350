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
#include "commons/BoostCommon.h"
#include "commons/ClassTraits.h"
#include "commons/Logging.h"
#include "commons/StdCommon.h"
#include "native/configs/CacheConfig.h"
#include "native/configs/ModelConfig.h"
#include "native/configs/ParallelConfig.h"
#include "native/configs/ReplicaSchedulerConfig.h"
#include "native/core/scheduler/replica_schedulers/trackers/BatchFormationTracker.h"
#include "native/core/scheduler/replica_schedulers/trackers/KvpStateTracker.h"
#include "native/core/scheduler/request_prioritizers/BaseRequestPrioritizer.h"
#include "native/data_structures/Queues.h"
#include "native/datatypes/BaseSequenceWithPriority.h"
#include "native/datatypes/SchedulerOutput.h"
#include "native/datatypes/Sequence.h"
#include "native/datatypes/SequenceScheduleMetadata.h"
//==============================================================================
namespace vajra {
//==============================================================================
constexpr std::size_t MAX_NUM_SKIPPED_SEQS = 10;
//==============================================================================

class BaseReplicaScheduler : public NonCopyableNonMovable {
 public:
  // Queues to manage sequences

  BaseReplicaScheduler(
      const ModelConfig& model_config,
      const std::shared_ptr<const BaseReplicaSchedulerConfig>& scheduler_config,
      const CacheConfig& cache_config, const ParallelConfig& parallel_config,
      std::size_t num_gpu_blocks, SequencePriorityQueuePtr waiting_queue,
      std::shared_ptr<BaseRequestPrioritizer> request_prioritizer);

  virtual ~BaseReplicaScheduler() = default;

  // Reset the internal state
  void ResetState();

  // Add sequence to the partial prefill queue
  void AddPartialPrefill(const MutableSequencePtr& seq);

  // Called when a stage is completed
  void OnStageCompleted(const MutableSequences& seqs);

  // Called when a step is completed
  void OnStepCompleted(const MutableSequences& seqs, float execution_time);

  // Schedule the next batch
  [[nodiscard]] std::pair<SchedulerOutputPtr, MutableSequences> Schedule();

  // Free finished sequences
  void FreeFinishedSeqs();

  // Check if sequence is allocated
  bool IsSeqAllocated(const std::string& seq_id) const;

 protected:
  // Preempt a sequence
  void Preempt(const MutableSequencePtr& seq);

  // Allocate memory for a sequence
  bool Allocate(const MutableSequencePtr& seq);

  // Free memory allocated for a sequence
  void FreeSeq(const MutableSequencePtr& seq);

  // Append a slot to a sequence
  bool AppendSlot(const MutableSequencePtr& seq);

  // Ensure that a slot can be appended to a sequence
  bool EnsureCanAppendSlot(const MutableSequencePtr& input_seq,
                           BatchFormationTracker& batch_formation_tracker);

  // Check if sequence prompt length is within limits
  bool CheckSeqPromptLength(const MutableSequencePtr& seq);

  // Get batch formation tracker
  virtual std::shared_ptr<BatchFormationTracker> GetBatchFormationTracker();

  // Schedule the next batch (internal implementation)
  std::pair<SchedulerOutputPtr, MutableSequences> ScheduleInternal();

  // Method to be implemented by subclasses or provided by base
  virtual std::size_t GetSeqNextNumQTokens(
      const MutableSequencePtr& seq,
      [[maybe_unused]] const BatchFormationTracker& batch_formation_tracker)
      const {
    return std::min(seq->GetPromptLength(), prompt_limit_);
  }

  // Configuration objects
  ModelConfig model_config_;
  std::shared_ptr<const BaseReplicaSchedulerConfig> scheduler_config_;
  CacheConfig cache_config_;
  ParallelConfig parallel_config_;
  std::shared_ptr<BaseRequestPrioritizer> request_prioritizer_;

  // KVP state tracker
  std::shared_ptr<KvpStateTracker> kvp_state_tracker_;

  // Counter for schedule iterations
  int iteration_id_;

  // Maximum sequence length
  std::size_t prompt_limit_;

  // Number of running batches and stages
  std::size_t num_running_batches_;
  std::size_t num_running_stages_;

  // Map to track allocated blocks per sequence
  std::unordered_map<std::string, int> seq_block_counter_;

  SequencePriorityQueuePtr waiting_;
  MutableSequences running_;  // Using a simple vector for running sequences

  std::multiset<MutableBaseSequenceWithPriorityPtr,
                BaseSequenceWithPriorityComparator>
      partial_prefills_;  // Using multiset for arbitrary element removal

  // Time tracking
  float last_batch_execution_time_;

  // Mutex for thread safety
  mutable std::mutex mutex_;
};
//==============================================================================
}  // namespace vajra
//==============================================================================
