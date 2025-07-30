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
#include "native/core/scheduler/replica_schedulers/BaseReplicaScheduler.h"
//==============================================================================
namespace vajra {
//==============================================================================
// Make sure we have the SequenceScheduleMetadataPtr type
using SequenceScheduleMetadataPtr =
    std::shared_ptr<const SequenceScheduleMetadata>;
//==============================================================================
BaseReplicaScheduler::BaseReplicaScheduler(
    const ModelConfig& model_config,
    const std::shared_ptr<const BaseReplicaSchedulerConfig>& scheduler_config,
    const CacheConfig& cache_config, const ParallelConfig& parallel_config,
    std::size_t num_gpu_blocks, SequencePriorityQueuePtr waiting_queue,
    std::shared_ptr<BaseRequestPrioritizer> request_prioritizer)
    : model_config_(model_config),
      scheduler_config_(scheduler_config),
      cache_config_(cache_config),
      parallel_config_(parallel_config),
      request_prioritizer_(request_prioritizer),
      kvp_state_tracker_(std::make_shared<KvpStateTracker>(
          model_config, cache_config, parallel_config, num_gpu_blocks)),
      iteration_id_(0),
      prompt_limit_(model_config.max_model_len),
      num_running_batches_(0),
      num_running_stages_(0),
      waiting_(waiting_queue),
      running_(),           // Initialize as empty vector
      partial_prefills_(),  // Initialize as empty multiset
      last_batch_execution_time_(0.0f) {
  ASSERT_VALID_POINTER_ARGUMENT(scheduler_config);
  ASSERT_VALID_POINTER_ARGUMENT(waiting_queue);
  ASSERT_VALID_POINTER_ARGUMENT(request_prioritizer);
}
//==============================================================================
void BaseReplicaScheduler::ResetState() {
  std::lock_guard<std::mutex> lock(mutex_);
  iteration_id_ = 0;
  last_batch_execution_time_ = 0.0f;
}
//==============================================================================
void BaseReplicaScheduler::AddPartialPrefill(const MutableSequencePtr& seq) {
  ASSERT_VALID_POINTER_ARGUMENT(seq);

  partial_prefills_.insert(request_prioritizer_->GetSeqWithPriority(seq));
}
//==============================================================================
void BaseReplicaScheduler::OnStageCompleted(const MutableSequences& seqs) {
  std::lock_guard<std::mutex> lock(mutex_);
  num_running_stages_--;

  for (const auto& seq : seqs) {
    ASSERT_VALID_RUNTIME(
        !seq->IsFinished(),
        "Sequence {} should not be in finished state during OnStageCompleted",
        seq->seq_id);

    if (!seq->IsPaused()) {
      continue;
    }

    ASSERT_VALID_RUNTIME(
        !seq->GetPromptStageProcessingFinished(),
        "Sequence {} should not have GetPromptStageProcessingFinished() set "
        "during OnStageCompleted",
        seq->seq_id);
    AddPartialPrefill(seq);
  }
}
//==============================================================================
void BaseReplicaScheduler::OnStepCompleted(const MutableSequences& seqs,
                                           float execution_time) {
  std::lock_guard<std::mutex> lock(mutex_);
  num_running_batches_--;
  if (!(parallel_config_.pipeline_parallel_size > 1)) {
    num_running_stages_--;
  }

  last_batch_execution_time_ = execution_time;

  for (const auto& seq : seqs) {
    if (seq->IsFinished()) {
      FreeSeq(seq);
      continue;
    }

    if (!seq->IsPaused()) {
      continue;
    }

    if (seq->GetPromptProcessingFinished()) {
      running_.push_back(seq);
    } else if (!parallel_config_.enable_sequence_pipeline_parallel) {
      AddPartialPrefill(seq);
    }
  }
}
//==============================================================================
bool BaseReplicaScheduler::IsSeqAllocated(const std::string& seq_id) const {
  std::lock_guard<std::mutex> lock(mutex_);
  return seq_block_counter_.find(seq_id) != seq_block_counter_.end();
}
//==============================================================================
void BaseReplicaScheduler::Preempt(const MutableSequencePtr& seq) {
  ASSERT_VALID_POINTER_ARGUMENT(seq);

  ASSERT_VALID_RUNTIME(seq->IsExecuting(),
                       "Sequence {} must be in executing state for preemption",
                       seq->seq_id);
  FreeSeq(seq);
  waiting_->push(request_prioritizer_->GetSeqWithPriority(seq));
}
//==============================================================================
bool BaseReplicaScheduler::Allocate(const MutableSequencePtr& seq) {
  // We use a naive approach to allocate memory where we allocate all the memory
  // required by the seq in one go. This is because we expect the compute
  // requirement to far exceed the memory requirement. In KVP, incremental
  // memory allocation can lead to deadlocks -- where multiple long seqs are
  // waiting for memory to be available on a new kvp group, but none of them can
  // proceed because the memory is not available.
  // TODO(amey): This is a naive approach and can be improved in the future.
  // Especially, offloading memory allocation to CPU can be a good solution,
  // especially for longer seqs. While allocating memory, we must choose the kvp
  // groups such that we have minimal compute contention. While also ensuring
  // that we don't create memory hotspots. The allocate method offloads this
  // responsibility to _get_allocation_order method.

  // If sequence is already allocated, return true
  if (seq_block_counter_.find(seq->seq_id) != seq_block_counter_.end()) {
    return true;
  }

  // Delegate allocation to the KVP manager
  bool status;
  int num_blocks;
  std::tie(status, num_blocks) = kvp_state_tracker_->Allocate(seq);
  if (status) {
    seq_block_counter_[seq->seq_id] = num_blocks;
  }
  return status;
}
//==============================================================================
void BaseReplicaScheduler::FreeSeq(const MutableSequencePtr& seq) {
  ASSERT_VALID_POINTER_ARGUMENT(seq);

  kvp_state_tracker_->FreeSeq(seq);
  seq_block_counter_.erase(seq->seq_id);
}
//==============================================================================
bool BaseReplicaScheduler::AppendSlot(const MutableSequencePtr& seq) {
  ASSERT_VALID_POINTER_ARGUMENT(seq);

  int num_total_blocks = seq_block_counter_[seq->seq_id];
  bool has_appended = kvp_state_tracker_->AppendSlot(seq, num_total_blocks);
  if (has_appended) {
    seq_block_counter_[seq->seq_id] += 1;
  }
  return has_appended;
}
//==============================================================================
bool BaseReplicaScheduler::EnsureCanAppendSlot(
    const MutableSequencePtr& input_seq,
    BatchFormationTracker& batch_formation_tracker) {
  ASSERT_VALID_POINTER_ARGUMENT(input_seq);

  if (kvp_state_tracker_->CanAppendSlot(input_seq)) {
    return true;
  }

  // Get the sequence with the lowest actual priority (highest numerical
  // priority value) Since partial_prefills_ is a multiset ordered by priority,
  // the last element has the highest value
  MutableBaseSequenceWithPriorityPtr lowest_priority_seq = nullptr;
  if (!partial_prefills_.empty()) {
    lowest_priority_seq = *partial_prefills_.rbegin();
  }

  // If we find a sequence that can be preempted, preempt it
  if (lowest_priority_seq) {
    // Remove the sequence from the multiset
    partial_prefills_.erase(partial_prefills_.find(lowest_priority_seq));

    // Ensure we're not preempting the input sequence
    ASSERT_VALID_RUNTIME(
        input_seq->seq_id != lowest_priority_seq->GetSequence()->seq_id,
        "Cannot preempt the input sequence {}", input_seq->seq_id);

    Preempt(lowest_priority_seq->GetSequence());
    batch_formation_tracker.AddPreemptedSequence(
        lowest_priority_seq->GetSequence());
    return true;
  }

  // If we haven't found space yet, check running list in reverse
  // Note: We need to process from the end to match Python's behavior
  for (auto it = running_.rbegin(); it != running_.rend(); ++it) {
    auto seq = *it;
    std::size_t last_kv_group_id = kvp_state_tracker_->GetLastKvGroupId(seq);

    auto kvp_groups =
        kvp_state_tracker_->GetKvpGroupBlockCounter(input_seq->seq_id);
    ASSERT_VALID_RUNTIME(
        kvp_groups.find(last_kv_group_id) != kvp_groups.end(),
        "Running sequence {} is not allocated on the last kv group",
        seq->seq_id);

    // Preempt the sequence
    Preempt(seq);
    batch_formation_tracker.AddPreemptedSequence(seq);

    // Don't add back other sequences to running - they've been preempted
    // Remove this sequence from the running list
    auto non_reversed_it =
        std::next(running_.begin(), std::distance(running_.rbegin(), it + 1));
    running_.erase(non_reversed_it);

    // If the preempted sequence is not the input sequence, return true
    return seq->seq_id != input_seq->seq_id;
  }

  THROW_RUNTIME_ERROR("Unreachable condition reached");
}
//==============================================================================
bool BaseReplicaScheduler::CheckSeqPromptLength(const MutableSequencePtr& seq) {
  ASSERT_VALID_POINTER_ARGUMENT(seq);

  return seq->GetPromptLength() <= kvp_state_tracker_->GetMaxSeqLen();
}
//==============================================================================
std::shared_ptr<BatchFormationTracker>
BaseReplicaScheduler::GetBatchFormationTracker() {
  return std::make_shared<BatchFormationTracker>(
      iteration_id_, scheduler_config_->GetMaxBatchSize(), kvp_state_tracker_);
}
//==============================================================================
std::pair<SchedulerOutputPtr, MutableSequences>
BaseReplicaScheduler::ScheduleInternal() {
  auto batch_formation_tracker = GetBatchFormationTracker();
  std::size_t num_skipped_seqs = 0;
  MutableSequences new_seqs;

  // First we handle the running sequences
  // Since we're directly manipulating the running_ vector, no need to copy it

  while (!running_.empty() && num_skipped_seqs < running_.size()) {
    auto seq = running_[num_skipped_seqs];  // Start with the skipped sequences

    ASSERT_VALID_RUNTIME(
        !seq->IsFinished(),
        "Sequence {} should not be in finished state during scheduling",
        seq->seq_id);
    ASSERT_VALID_RUNTIME(
        seq->GetPromptStageProcessingFinished(),
        "Sequence {} should have GetPromptStageProcessingFinished() set during "
        "scheduling",
        seq->seq_id);
    ASSERT_VALID_RUNTIME(
        seq->IsPaused(),
        "Sequence {} should be in paused state during scheduling", seq->seq_id);

    if (!batch_formation_tracker->CanAddSequences()) {
      break;
    }

    if (!EnsureCanAppendSlot(seq, *batch_formation_tracker)) {
      continue;
    }

    AppendSlot(seq);
    if (!batch_formation_tracker->CanAddSequences()) {
      num_skipped_seqs++;
      continue;
    }

    // Remove the sequence from the running list at the current position
    running_.erase(running_.begin() + num_skipped_seqs);
    batch_formation_tracker->AddSequence(seq, 1);
  }

  // Then handle waiting and partial prefill queues
  while (num_skipped_seqs < MAX_NUM_SKIPPED_SEQS) {
    // Try to peek at both queues
    MutableBaseSequenceWithPriorityPtr waiting_seq = nullptr;
    MutableBaseSequenceWithPriorityPtr partial_prefill_seq = nullptr;

    if (!waiting_->empty()) {
      waiting_seq = waiting_->pull();
    }

    // Get highest actual priority sequence (lowest numerical priority value)
    // from partial_prefills_
    if (!partial_prefills_.empty()) {
      partial_prefill_seq =
          *partial_prefills_
               .begin();  // First element has lowest numerical priority value
      partial_prefills_.erase(partial_prefills_.begin());
    }

    // If both queues are empty, break
    if (!waiting_seq && !partial_prefill_seq) {
      break;
    }

    float waiting_seq_priority = waiting_seq
                                     ? waiting_seq->GetPriority()
                                     : std::numeric_limits<float>::infinity();
    float partial_prefill_seq_priority =
        partial_prefill_seq ? partial_prefill_seq->GetPriority()
                            : std::numeric_limits<float>::infinity();

    MutableBaseSequenceWithPriorityPtr seq_with_priority = nullptr;
    bool is_from_waiting = false;

    // Lower numerical priority value means higher actual priority
    if (waiting_seq_priority < partial_prefill_seq_priority) {
      ASSERT_VALID_RUNTIME(waiting_seq != nullptr,
                           "Waiting sequence should not be null when its "
                           "priority is less than partial prefill");
      seq_with_priority = waiting_seq;
      is_from_waiting = true;
      if (partial_prefill_seq) {
        partial_prefills_.insert(partial_prefill_seq);
      }
    } else {
      ASSERT_VALID_RUNTIME(partial_prefill_seq != nullptr,
                           "Partial prefill sequence should not be null when "
                           "its priority is less than or equal to waiting");
      seq_with_priority = partial_prefill_seq;
      is_from_waiting = false;
      if (waiting_seq) {
        waiting_->push(waiting_seq);
      }
    }

    ASSERT_VALID_RUNTIME(
        seq_with_priority != nullptr,
        "Sequence with priority should not be null at this point");
    auto seq = seq_with_priority->GetSequence();

    if (!CheckSeqPromptLength(seq)) {
      batch_formation_tracker->AddIgnoredSequence(seq);
      seq->SetStatus(SequenceStatus::FinishedIgnored);
      LOG_WARNING("Ignoring seq_id: {} due to max seq length limit.",
                  seq->seq_id);
      continue;
    }

    if (!batch_formation_tracker->CanAddSequences()) {
      // Put the sequence back in its original queue
      if (is_from_waiting) {
        waiting_->push(waiting_seq);
      } else {
        partial_prefills_.insert(partial_prefill_seq);
      }
      break;
    }

    ASSERT_VALID_RUNTIME(
        !seq->GetPromptStageProcessingFinished(),
        "Sequence {} should not have GetPromptStageProcessingFinished() set "
        "during scheduling from queues",
        seq->seq_id);
    ASSERT_VALID_RUNTIME(!seq->IsFinished(),
                         "Sequence {} should not be in finished state during "
                         "scheduling from queues",
                         seq->seq_id);
    ASSERT_VALID_RUNTIME(
        seq->IsPaused() || seq->IsWaitingPreempted() || seq->IsWaiting(),
        "Sequence {} should be in paused, waiting_preempted, or waiting state "
        "during scheduling from queues, but is in state {}",
        seq->seq_id, static_cast<int>(seq->GetStatus()));

    if (!Allocate(seq)) {
      num_skipped_seqs++;
      // Put back in original queue
      if (is_from_waiting) {
        waiting_->push(waiting_seq);
      } else {
        partial_prefills_.insert(partial_prefill_seq);
      }
      continue;
    }

    int num_q_tokens = GetSeqNextNumQTokens(seq, *batch_formation_tracker);

    if (num_q_tokens == 0) {
      num_skipped_seqs++;
      // Put back in original queue
      if (is_from_waiting) {
        waiting_->push(waiting_seq);
      } else {
        partial_prefills_.insert(partial_prefill_seq);
      }
      continue;
    }

    if (seq->IsWaiting()) {
      new_seqs.push_back(seq);
    }

    batch_formation_tracker->AddSequence(seq, num_q_tokens);
  }

  auto batch = batch_formation_tracker->GetBatch();
  return std::make_pair(batch, std::move(new_seqs));
}
//==============================================================================
std::pair<SchedulerOutputPtr, MutableSequences>
BaseReplicaScheduler::Schedule() {
  std::lock_guard<std::mutex> lock(mutex_);
  iteration_id_++;

  if (num_running_batches_ >= parallel_config_.pipeline_parallel_size ||
      num_running_stages_ != 0) {
    return std::make_pair(std::make_shared<SchedulerOutput>(
                              iteration_id_, std::vector<std::string>{},
                              std::vector<std::string>{},
                              std::vector<SequenceScheduleMetadataPtr>{}),
                          MutableSequences{});
  }

  auto [scheduler_output, sequences] = ScheduleInternal();

  if (!scheduler_output->is_empty) {
    num_running_batches_++;
    num_running_stages_++;
  }

  return std::make_pair(scheduler_output, sequences);
}
//==============================================================================
void BaseReplicaScheduler::FreeFinishedSeqs() {
  std::lock_guard<std::mutex> lock(mutex_);

  // Create a new vector to hold non-finished sequences
  MutableSequences remaining_seqs;

  for (const auto& seq : running_) {
    if (seq->IsFinished()) {
      FreeSeq(seq);
    } else {
      remaining_seqs.push_back(seq);
    }
  }

  // Replace running_ with the filtered vector
  running_ = std::move(remaining_seqs);
}
//==============================================================================
}  // namespace vajra
//==============================================================================
