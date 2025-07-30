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
#include "commons/StdCommon.h"
#include "native/configs/ReplicaSchedulerConfig.h"
#include "native/core/scheduler/replica_schedulers/DynamicChunkReplicaScheduler.h"
#include "native/core/scheduler/replica_schedulers/trackers/BatchFormationTrackerWithRuntimePrediction.h"
#include "native/core/scheduler/request_prioritizers/LrsRequestPrioritizer.h"
//==============================================================================
namespace vajra {
//==============================================================================
/**
 * @brief Space Sharing Replica Scheduler for managing sequences with
 * long-running requests
 *
 * This scheduler extends the DynamicChunkReplicaScheduler with space sharing
 * capabilities to optimize execution for long-running sequences. It
 * intelligently adjusts target batch times based on sequence length and
 * available slack in the system.
 */
class SpaceSharingReplicaScheduler : public DynamicChunkReplicaScheduler {
 public:
  /**
   * @brief Constructs a new Space Sharing Replica Scheduler
   *
   * @param model_config The model configuration
   * @param scheduler_config The scheduler configuration (must be
   * SpaceSharingReplicaSchedulerConfig)
   * @param cache_config The cache configuration
   * @param parallel_config The parallel configuration
   * @param num_gpu_blocks The number of GPU blocks available
   * @param waiting_queue The queue of waiting sequences
   * @param request_prioritizer The request prioritizer (must be
   * LrsRequestPrioritizer)
   * @param execution_time_predictor The execution time predictor
   */
  SpaceSharingReplicaScheduler(
      const ModelConfig& model_config,
      const std::shared_ptr<const SpaceSharingReplicaSchedulerConfig>&
          scheduler_config,
      const CacheConfig& cache_config, const ParallelConfig& parallel_config,
      std::size_t num_gpu_blocks, SequencePriorityQueuePtr waiting_queue,
      std::shared_ptr<BaseRequestPrioritizer> request_prioritizer,
      std::shared_ptr<vidur::execution_time_predictor::ExecutionTimePredictor>
          execution_time_predictor);

  /**
   * @brief Destructor
   */
  ~SpaceSharingReplicaScheduler() override = default;

 protected:
  /**
   * @brief Get the number of tokens to process next for a sequence with space
   * sharing logic
   *
   * @param seq The sequence to process
   * @param batch_formation_tracker The batch formation tracker
   * @return std::size_t The number of tokens to process
   */
  std::size_t GetSeqNextNumQTokens(
      const MutableSequencePtr& seq,
      const BatchFormationTracker& batch_formation_tracker) const override;

 private:
  /**
   * @brief Get the scheduler config with proper type
   *
   * @return std::shared_ptr<const SpaceSharingReplicaSchedulerConfig> The
   * scheduler config
   */
  std::shared_ptr<const SpaceSharingReplicaSchedulerConfig> GetSchedulerConfig()
      const {
    return std::static_pointer_cast<const SpaceSharingReplicaSchedulerConfig>(
        scheduler_config_);
  }
  // Maximum fraction for space sharing
  static constexpr float MAX_SPACE_SHARE_FRAC = 0.5f;
};
//==============================================================================
}  // namespace vajra
//==============================================================================
