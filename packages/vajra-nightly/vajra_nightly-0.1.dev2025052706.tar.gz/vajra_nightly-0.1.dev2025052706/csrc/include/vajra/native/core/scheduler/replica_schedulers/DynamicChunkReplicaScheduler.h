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
#include "native/core/scheduler/replica_schedulers/BaseReplicaScheduler.h"
#include "native/core/scheduler/replica_schedulers/trackers/BatchFormationTrackerWithRuntimePrediction.h"
#include "vidur/execution_time_predictor/execution_time_predictor.h"
//==============================================================================
namespace vajra {
//==============================================================================
/**
 * @brief Dynamic Chunk Replica Scheduler that adjusts chunk size based on
 * runtime predictions
 *
 * This scheduler extends the BaseReplicaScheduler with the ability to
 * dynamically adjust chunk sizes based on runtime predictions to meet target
 * batch times.
 */
class DynamicChunkReplicaScheduler : public BaseReplicaScheduler {
 public:
  /**
   * @brief Constructs a new Dynamic Chunk Replica Scheduler
   *
   * @param model_config The model configuration
   * @param scheduler_config The scheduler configuration (must be
   * DynamicChunkReplicaSchedulerConfig)
   * @param cache_config The cache configuration
   * @param parallel_config The parallel configuration
   * @param num_gpu_blocks The number of GPU blocks available
   * @param waiting_queue The queue of waiting sequences
   * @param request_prioritizer The request prioritizer
   * @param execution_time_predictor_capsule Capsule containing the Vidur
   * execution time predictor
   */
  DynamicChunkReplicaScheduler(
      const ModelConfig& model_config,
      const std::shared_ptr<const DynamicChunkReplicaSchedulerConfig>&
          scheduler_config,
      const CacheConfig& cache_config, const ParallelConfig& parallel_config,
      std::size_t num_gpu_blocks, SequencePriorityQueuePtr waiting_queue,
      std::shared_ptr<BaseRequestPrioritizer> request_prioritizer,
      std::shared_ptr<vidur::execution_time_predictor::ExecutionTimePredictor>
          execution_time_predictor);

  /**
   * @brief Destructor
   */
  ~DynamicChunkReplicaScheduler() override = default;

 protected:
  /**
   * @brief Get the batch formation tracker for this scheduler
   *
   * @return std::shared_ptr<BatchFormationTrackerWithRuntimePrediction> The
   * batch formation tracker
   */
  std::shared_ptr<BatchFormationTracker> GetBatchFormationTracker() override;

  /**
   * @brief Get the number of tokens to process next for a sequence
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
   * @return std::shared_ptr<const DynamicChunkReplicaSchedulerConfig> The
   * scheduler config
   */
  std::shared_ptr<const DynamicChunkReplicaSchedulerConfig> GetSchedulerConfig()
      const {
    return std::static_pointer_cast<const DynamicChunkReplicaSchedulerConfig>(
        scheduler_config_);
  }

  // Execution time predictor for runtime prediction
  std::shared_ptr<vidur::execution_time_predictor::ExecutionTimePredictor>
      execution_time_predictor_;
};
//==============================================================================
}  // namespace vajra
//==============================================================================
