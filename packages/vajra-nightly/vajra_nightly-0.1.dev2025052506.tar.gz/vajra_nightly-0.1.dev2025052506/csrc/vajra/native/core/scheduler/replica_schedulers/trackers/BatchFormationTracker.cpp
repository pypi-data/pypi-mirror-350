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
#include "native/core/scheduler/replica_schedulers/trackers/BatchFormationTracker.h"

using vajra::BatchFormationTracker;

BatchFormationTracker::BatchFormationTracker(
    const std::size_t schedule_id, const std::size_t max_micro_batch_size,
    std::shared_ptr<KvpStateTracker> kvp_state_tracker)
    : schedule_id_(schedule_id),
      max_micro_batch_size_(max_micro_batch_size),
      kvp_state_tracker_(kvp_state_tracker),
      num_sequences_(0) {
  ASSERT_VALID_POINTER_ARGUMENT(kvp_state_tracker);

  // Start a new batch formation cycle in the KVP manager
  kvp_state_tracker_->StartBatchFormation();
}

void BatchFormationTracker::AddSequence(const MutableSequencePtr seq,
                                        const std::size_t num_q_tokens) {
  ASSERT_VALID_POINTER_ARGUMENT(seq);

  num_sequences_++;
  std::vector<std::size_t> active_kvp_group_ids =
      kvp_state_tracker_->GetActiveKvpGroupIds(seq);

  sequences_.push_back(seq);
  batch_num_q_tokens_.push_back(num_q_tokens);
  batch_group_mapping_.push_back(
      kvp_state_tracker_->GetKvpGroupBlockCounter(seq->seq_id));
  batch_active_group_ids_.push_back(active_kvp_group_ids);

  std::size_t num_processed_tokens = seq->GetNumTokensStageProcessed();

  // Update prefill work tracking in the KVP manager
  kvp_state_tracker_->UpdatePrefillWork(seq, num_processed_tokens,
                                        num_q_tokens);

  // Add sequence to the KVP manager's batch tracker
  kvp_state_tracker_->AddSequenceToBatch(seq, num_q_tokens,
                                         active_kvp_group_ids);
}

void BatchFormationTracker::AddIgnoredSequence(const MutableSequencePtr seq) {
  ASSERT_VALID_POINTER_ARGUMENT(seq);

  ignored_sequence_ids_.push_back(seq->seq_id);
}

void BatchFormationTracker::AddPreemptedSequence(const MutableSequencePtr seq) {
  ASSERT_VALID_POINTER_ARGUMENT(seq);

  preempted_sequence_ids_.push_back(seq->seq_id);
}

bool BatchFormationTracker::CanAddSequences() const {
  return num_sequences_ < max_micro_batch_size_;
}

std::shared_ptr<vajra::SchedulerOutput> BatchFormationTracker::GetBatch()
    const {
  // Ensure all relevant vectors have the same size.
  ASSERT_VALID_RUNTIME(sequences_.size() == batch_group_mapping_.size(),
                       "BatchFormationTracker: sequences_.size() != "
                       "batch_group_mapping_.size()");
  ASSERT_VALID_RUNTIME(sequences_.size() == batch_active_group_ids_.size(),
                       "BatchFormationTracker: sequences_.size() != "
                       "batch_active_group_ids_.size()");
  ASSERT_VALID_RUNTIME(sequences_.size() == batch_num_q_tokens_.size(),
                       "BatchFormationTracker: sequences_.size() != "
                       "batch_num_q_tokens_.size()");

  std::vector<SequenceScheduleMetadataPtr> seq_schedule_metadata_list;

  for (std::size_t i = 0; i < sequences_.size(); ++i) {
    std::unordered_map<std::size_t, std::size_t> kvp_group_block_counter;
    for (const auto& [group_id, block_count] : batch_group_mapping_.at(i)) {
      kvp_group_block_counter[group_id] = block_count;
    }

    const std::vector<std::size_t>& kvp_group_ids =
        batch_active_group_ids_.at(i);

    seq_schedule_metadata_list.push_back(
        std::make_shared<SequenceScheduleMetadata>(
            schedule_id_, sequences_.at(i)->seq_id, batch_num_q_tokens_.at(i),
            kvp_group_block_counter, kvp_group_ids));
  }

  return std::make_shared<SchedulerOutput>(schedule_id_, ignored_sequence_ids_,
                                           preempted_sequence_ids_,
                                           seq_schedule_metadata_list);
}
