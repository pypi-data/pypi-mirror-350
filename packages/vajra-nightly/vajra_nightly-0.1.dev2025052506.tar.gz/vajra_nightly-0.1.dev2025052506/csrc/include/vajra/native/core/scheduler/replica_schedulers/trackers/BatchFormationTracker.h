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
#include "commons/ClassTraits.h"
#include "commons/StdCommon.h"
#include "native/core/scheduler/replica_schedulers/trackers/KvpStateTracker.h"
#include "native/datatypes/SchedulerOutput.h"
#include "native/datatypes/Sequence.h"
#include "native/datatypes/SequenceScheduleMetadata.h"
//==============================================================================
namespace vajra {
//==============================================================================
/**
 * @brief Batch formation tracker for the current scheduling cycle
 *
 * This class tracks the sequences being formed into a batch during
 * the current scheduling cycle. It interacts with the KvpStateTracker
 * to manage KVP resources.
 */
class BatchFormationTracker : public NonCopyableNonMovable {
 public:
  /**
   * @brief Constructs a BatchFormationTracker
   *
   * @param schedule_id The ID of the current scheduling cycle
   * @param max_micro_batch_size The maximum number of sequences in a microbatch
   * @param kvp_state_tracker The KVP state tracker to use
   */
  BatchFormationTracker(const std::size_t schedule_id,
                        const std::size_t max_micro_batch_size,
                        std::shared_ptr<KvpStateTracker> kvp_state_tracker);

  /**
   * @brief Virtual destructor
   */
  virtual ~BatchFormationTracker() = default;

  /**
   * @brief Adds a sequence to the batch
   *
   * @param seq The sequence to add
   * @param num_q_tokens Number of query tokens for the sequence
   */
  void AddSequence(const MutableSequencePtr seq,
                   const std::size_t num_q_tokens);

  /**
   * @brief Adds a sequence to the ignored list
   *
   * @param seq The sequence to ignore
   */
  void AddIgnoredSequence(const MutableSequencePtr seq);

  /**
   * @brief Adds a sequence to the preempted list
   *
   * @param seq The sequence to preempt
   */
  void AddPreemptedSequence(const MutableSequencePtr seq);

  /**
   * @brief Checks if more sequences can be added to the batch
   *
   * @return True if more sequences can be added
   */
  [[nodiscard]] bool CanAddSequences() const;

  /**
   * @brief Gets the formed batch as a SchedulerOutput
   *
   * @return The scheduler output containing the batch
   */
  [[nodiscard]] std::shared_ptr<SchedulerOutput> GetBatch() const;

 private:
  // Schedule information
  const std::size_t schedule_id_;
  const std::size_t max_micro_batch_size_;

 protected:
  // KVP state tracker
  std::shared_ptr<KvpStateTracker> kvp_state_tracker_;

  // Basic batch formation tracking
  std::size_t num_sequences_;
  std::vector<MutableSequencePtr> sequences_;
  std::vector<std::string> ignored_sequence_ids_;
  std::vector<std::string> preempted_sequence_ids_;

  // Metadata for building the scheduler output
  std::vector<std::size_t>
      batch_num_q_tokens_;  // Stores the number of query tokens for each
                            // sequence in the batch
  std::vector<std::map<std::size_t, std::size_t>>
      batch_group_mapping_;  // Maps KVP group IDs to block counts for each
                             // sequence
  std::vector<std::vector<std::size_t>>
      batch_active_group_ids_;  // Stores the active KVP group IDs for each
                                // sequence
};
//==============================================================================
}  // namespace vajra
//==============================================================================
