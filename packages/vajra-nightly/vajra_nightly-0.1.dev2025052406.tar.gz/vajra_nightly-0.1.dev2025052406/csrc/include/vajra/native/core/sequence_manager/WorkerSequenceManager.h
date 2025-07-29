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
#include "native/core/block_space_manager/BlockSpaceManager.h"
#include "native/core/sequence_manager/BaseSequenceManager.h"
#include "native/datatypes/SequenceMetadata.h"
//==============================================================================
namespace vajra {
//==============================================================================
// TODO(1ntEgr8): replace this with LLMReplicaConfig when it becomes stable
struct WorkerSequenceManagerParams {
  const bool enable_sequence_pipeline_parallel;

  // Cache config params
  const std::size_t block_size;
  const std::size_t num_gpu_blocks;

  // Model config params
  const std::size_t max_model_len;

  // Parallel config params
  const std::size_t max_num_tokens_per_kvp_group;

  // torch.distributed params
  const std::size_t rank;
  const std::size_t kvp_group_id;
  const std::size_t kvp_parallel_world_size;
};
//==============================================================================
class WorkerSequenceManager : public BaseSequenceManager {
 public:
  explicit WorkerSequenceManager(WorkerSequenceManagerParams params);

  void OnStageCompleted(SchedulerOutputPtr scheduler_output) override;

  void OnStepCompleted(const std::vector<SequenceScheduleMetadataPtr>&
                           seq_schedule_metadata_list,
                       const ValidSamplerOutputs& sampler_outputs) override;

  std::pair<MutableSequences, MutableSequences> OnSchedule(
      SchedulerOutputPtr scheduler_output) override;

  std::tuple<Sequences, Sequences, SequenceMetadataVector> OnScheduleWorker(
      const SchedulerOutputPtr scheduler_output);

 protected:
  void FreeSeq(const std::string& seq_id) override;

  void PreemptSeq(const std::string& seq_id) override;

  void OnSeqScheduled(SequenceScheduleMetadataPtr seq_sched_metadata) override;

  std::vector<int> GetBlockTable(SequencePtr seq) const override;

  void OnAppendToken(MutableSequencePtr seq,
                     std::size_t num_new_tokens) override;

 private:
  std::pair<std::size_t, bool> ComputeKVCacheInfo(
      SequencePtr seq, const std::vector<std::size_t> kvp_group_ids);

  std::size_t rank_;
  std::size_t kvp_group_id_;
  std::size_t max_num_tokens_per_kvp_group_;
  BlockSpaceManager block_manager_;
};
//==============================================================================
using WorkerSequenceManagerPtr = std::shared_ptr<WorkerSequenceManager>;
//==============================================================================
}  // namespace vajra
//==============================================================================
