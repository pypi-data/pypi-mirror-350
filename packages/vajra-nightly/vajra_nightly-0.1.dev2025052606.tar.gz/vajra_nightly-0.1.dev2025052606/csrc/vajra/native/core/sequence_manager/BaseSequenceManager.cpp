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
#include "native/core/sequence_manager/BaseSequenceManager.h"
//==============================================================================
namespace vajra {
//==============================================================================
std::pair<MutableSequences, MutableSequences> BaseSequenceManager::OnSchedule(
    const SchedulerOutputPtr scheduler_output) {
  ASSERT_VALID_POINTER_ARGUMENT(scheduler_output);

  std::lock_guard<std::recursive_mutex> lk(mutex_);

  MutableSequences ignored_seqs;
  for (auto seq_id : scheduler_output->ignored_seq_ids) {
    ASSERT_VALID_RUNTIME(seq_map_.find(seq_id) != seq_map_.end(),
                         "sequence {} not found", seq_id);
    auto seq = seq_map_[seq_id];
    ignored_seqs.emplace_back(seq);
    FreeSeq(seq_id);
  }

  for (auto seq_id : scheduler_output->preempted_seq_ids) {
    PreemptSeq(seq_id);
  }

  MutableSequences seqs;

  for (auto seq_sched_metadata : scheduler_output->seq_schedule_metadata_list) {
    OnSeqScheduled(seq_sched_metadata);
    auto seq = seq_map_[seq_sched_metadata->seq_id];
    seqs.push_back(seq);
  }

  return std::make_pair(ignored_seqs, seqs);
}
//==============================================================================
void BaseSequenceManager::OnStepCompleted(
    const std::vector<SequenceScheduleMetadataPtr>& seq_schedule_metadata_list,
    const ValidSamplerOutputs& sampler_outputs) {
  std::lock_guard<std::recursive_mutex> lk(mutex_);

  for (std::size_t i = 0; i < seq_schedule_metadata_list.size(); i++) {
    auto& seq_schedule_metadata = seq_schedule_metadata_list[i];
    ASSERT_VALID_POINTER_ARGUMENT(seq_schedule_metadata);

    auto sampler_output = sampler_outputs[i];

    ASSERT_VALID_RUNTIME(
        seq_schedule_metadata->seq_id == sampler_output->GetSeqId(),
        "Sequence ids do not match. {}, {}", seq_schedule_metadata->seq_id,
        sampler_output->GetSeqId());
    auto seq = seq_map_[seq_schedule_metadata->seq_id];

    if (seq->IsWaitingPreempted()) {
      // seq is preempted
      // this can happen with pipeline parallel -- if the system
      // runs out of memory, it will preempt the last arrived request
      // this request might still be executing when the next stage scheduling
      // triggers the preemption
      continue;
    }

    if (seq->GetPromptProcessingFinished()) {
      seq->UpdateTokensProcessed(seq_schedule_metadata->num_q_tokens);
    } else {
      if (!enable_sequence_pipeline_parallel_) {
        // In case of sequence pipeline parallel, the stage token cursor is
        // already updated in the on_stage_completed method
        seq->UpdatePromptTokensStageProcessed(
            seq_schedule_metadata->num_q_tokens);
      }
      seq->UpdatePromptTokensProcessed(seq_schedule_metadata->num_q_tokens);
    }

    if (enable_sequence_pipeline_parallel_) {
      if (!seq->GetPromptStageProcessingFinished()) {
        // for prompts that are running in sequence parallel manner
        // they would get unpaused at the end of the stage
        //
        // DO NOTHING
      } else if (seq->GetPromptStageProcessingFinished() &&
                 !seq->GetPromptProcessingFinished()) {
        // this is the transition phase where the first stage has finished
        // processing the prompt but there are intermediate micro-batches which
        // are remaining before the prompt processing actually completes
        //
        // DO NOTHING
      } else if (seq->GetPromptProcessingFinished()) {
        PauseSeq(seq_schedule_metadata->seq_id);
      }
    } else {
      PauseSeq(seq_schedule_metadata->seq_id);
    }

    ProcessSeqOutput(seq, sampler_output);
  }
}
//==============================================================================
void BaseSequenceManager::OnStageCompleted(
    const SchedulerOutputPtr scheduler_output) {
  ASSERT_VALID_POINTER_ARGUMENT(scheduler_output);

  std::lock_guard<std::recursive_mutex> lk(mutex_);

  if (!enable_sequence_pipeline_parallel_) return;

  for (auto seq_schedule_metadata :
       scheduler_output->seq_schedule_metadata_list) {
    auto seq = seq_map_[seq_schedule_metadata->seq_id];
    ASSERT_VALID_RUNTIME(!seq->IsFinished(), "sequence {} is finished!",
                         seq->seq_id);

    // seq is preempted
    // this can happen with pipeline parallel -- if the system
    // runs out of memory, it will preempt the last arrived request
    // this request might still be executing when the next stage scheduling
    // triggers the preemption
    if (seq->IsWaitingPreempted()) continue;

    if (seq->GetPromptStageProcessingFinished()) continue;

    seq->UpdatePromptTokensStageProcessed(seq_schedule_metadata->num_q_tokens);
    if (!seq->GetPromptStageProcessingFinished()) {
      PauseSeq(seq_schedule_metadata->seq_id);
    }
  }
}
//==============================================================================
std::vector<RequestOutputPtr> BaseSequenceManager::GenerateRequestOutputs(
    const Sequences& ignored_seqs, const Sequences& seqs) {
  std::vector<RequestOutputPtr> results;
  results.reserve(ignored_seqs.size() + seqs.size());
  for (auto seq : ignored_seqs) {
    results.push_back(std::make_shared<RequestOutput>(seq));
  }
  for (auto seq : seqs) {
    results.push_back(std::make_shared<RequestOutput>(seq));
  }
  return results;
}
//==============================================================================
void BaseSequenceManager::PreemptSeq(const std::string& seq_id) {
  ASSERT_VALID_RUNTIME(seq_map_.find(seq_id) != seq_map_.end(),
                       "sequence {} not found", seq_id);
  auto seq = seq_map_[seq_id];
  ASSERT_VALID_RUNTIME(seq->IsExecuting(),
                       "sequence {} is not executing. Status: {}", seq_id,
                       seq->GetStatus());
  seq->Reset();
}
//==============================================================================
void BaseSequenceManager::PauseSeq(const std::string& seq_id) {
  ASSERT_VALID_RUNTIME(seq_map_.find(seq_id) != seq_map_.end(),
                       "sequence {} not found", seq_id);
  auto seq = seq_map_[seq_id];
  ASSERT_VALID_RUNTIME(seq->IsRunning(),
                       "sequence {} is not running. Status: {}", seq_id,
                       seq->GetStatus());
  seq->SetStatus(SequenceStatus::Paused);
}
//==============================================================================
void BaseSequenceManager::ResumeSeq(const std::string& seq_id) {
  ASSERT_VALID_RUNTIME(seq_map_.find(seq_id) != seq_map_.end(),
                       "sequence {} not found", seq_id);
  auto seq = seq_map_[seq_id];
  ASSERT_VALID_RUNTIME(
      seq->IsWaiting() || seq->IsPaused() || seq->IsWaitingPreempted(),
      "sequence {} is not waiting, paused, or waiting preempted. Status: {}",
      seq_id, seq->GetStatus());
  seq->SetStatus(SequenceStatus::Running);
}
//==============================================================================
void BaseSequenceManager::ProcessSeqOutput(MutableSequencePtr seq,
                                           const SamplerOutputPtr sample) {
  ASSERT_VALID_POINTER_ARGUMENT(seq);
  ASSERT_VALID_RUNTIME(!seq->IsFinished(), "sequence {} is finished",
                       seq->seq_id);

  if (!seq->GetPromptProcessingFinished()) return;

  auto output_tokens = sample->GetOutputTokens();
  for (auto output_token : output_tokens) {
    seq->AppendTokenId(output_token);
  }

  std::size_t num_new_tokens = output_tokens.size();

  OnAppendToken(seq, num_new_tokens);

  seq->CheckStop(num_new_tokens);
  if (seq->IsFinished()) {
    FreeSeq(seq->seq_id);
  }
}
//==============================================================================
}  // namespace vajra
//==============================================================================
