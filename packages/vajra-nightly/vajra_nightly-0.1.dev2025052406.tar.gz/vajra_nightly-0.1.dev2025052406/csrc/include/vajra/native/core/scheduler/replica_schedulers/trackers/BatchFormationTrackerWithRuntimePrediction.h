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
// clang-format off
// Include vidur headers
#include "vidur/entities/batch.h"
#include "vidur/execution_time_predictor/execution_time_predictor.h"
// clang-format on
//==============================================================================
#include "commons/StdCommon.h"
#include "native/core/scheduler/replica_schedulers/trackers/BatchFormationTracker.h"
#include "native/core/scheduler/replica_schedulers/trackers/KvpStateTracker.h"
#include "native/datatypes/SchedulerOutput.h"
#include "native/datatypes/Sequence.h"
#include "native/datatypes/SequenceScheduleMetadata.h"
#include "native/utils/NumericalUtils.h"
//==============================================================================
namespace vajra {
//==============================================================================
// Constants
constexpr double EXECUTION_TIME_PREDICTION_SLACK = 0.1;
constexpr std::size_t EXECUTION_TIME_PREDICTION_START_CHUNK_SIZE = 512;
constexpr std::size_t EXECUTION_TIME_PREDICTION_CHUNK_SIZE_GRANULARITY = 32;
//==============================================================================
/**
 * @brief Batch formation tracker with runtime prediction functionality
 *
 * This class extends the basic BatchFormationTracker with additional
 * capabilities to predict execution times and optimize chunk sizes
 * based on those predictions.
 */
class BatchFormationTrackerWithRuntimePrediction
    : public BatchFormationTracker {
 public:
  /**
   * @brief Constructs a BatchFormationTrackerWithRuntimePrediction
   *
   * @param schedule_id The ID of the current scheduling cycle
   * @param max_micro_batch_size The maximum number of sequences in a microbatch
   * @param pipeline_parallel_size The size of the pipeline parallel dimension
   * @param kvp_state_tracker The KVP state tracker to use
   * @param max_chunk_size The maximum chunk size allowed
   * @param min_chunk_size The minimum chunk size allowed
   * @param execution_time_predictor The execution time predictor to use
   */
  BatchFormationTrackerWithRuntimePrediction(
      const std::size_t schedule_id, const std::size_t max_micro_batch_size,
      const std::size_t pipeline_parallel_size,
      const std::shared_ptr<KvpStateTracker> kvp_state_tracker,
      const std::size_t max_chunk_size, const std::size_t min_chunk_size,
      const std::shared_ptr<
          vidur::execution_time_predictor::ExecutionTimePredictor>
          execution_time_predictor);

  /**
   * @brief Adds a sequence to the batch with additional runtime prediction
   *
   * @param seq The sequence to add
   * @param num_q_tokens Number of query tokens for the sequence
   * @param active_kvp_group_ids The active KVP group IDs for this sequence
   * @param kvp_group_block_counter The KVP group block counter map
   */
  void AddSequence(const MutableSequencePtr seq,
                   const std::size_t num_q_tokens);

  /**
   * @brief Gets the predicted execution time for a KVP group
   *
   * @param kvp_group_id The KVP group ID
   * @return The predicted execution time
   */
  [[nodiscard]] double GetBatchExecutionTime(std::size_t kvp_group_id) const;

  /**
   * @brief Gets the predicted execution times for multiple KVP groups
   *
   * @param kvp_group_ids The KVP group IDs
   * @return A vector of predicted execution times
   */
  [[nodiscard]] std::vector<double> GetBatchExecutionTimeForKvpGroups(
      const std::vector<std::size_t>& kvp_group_ids) const;

  /**
   * @brief Gets the maximum chunk size for a sequence based on target batch
   * time
   *
   * @param seq The sequence
   * @param active_kvp_group_ids The active KVP group IDs for this sequence
   * @param target_batch_time The target batch execution time
   * @return The maximum chunk size for the sequence
   */
  [[nodiscard]] std::size_t GetMaxChunkSizeForSeq(
      const MutableSequencePtr seq,
      const std::vector<std::size_t>& active_kvp_group_ids,
      double target_batch_time) const;

 private:
  // Configuration
  const std::size_t pipeline_parallel_size_;
  const std::shared_ptr<vidur::execution_time_predictor::ExecutionTimePredictor>
      execution_time_predictor_;
  const std::size_t max_chunk_size_;
  const std::size_t min_chunk_size_;

  // Runtime prediction tracking
  // Stores the predicted execution time for each KVP group in the current
  // batch. The index corresponds to the KVP group ID and the value is the
  // predicted execution time in nanoseconds.
  std::vector<std::size_t> batch_execution_time_predictions_;

  /**
   * @brief Computes the batch execution time for a KVP group
   *
   * @param kvp_group_id The KVP group ID
   * @param extra_seqs Optional extra sequences to consider
   * @param extra_num_q_tokens Optional extra query token counts
   * @param extra_num_kv_tokens Optional extra KV token counts
   * @param extra_num_active_kvp_groups Optional extra active KVP groups counts
   * @param extra_last_kvp_group_ids Optional extra last KVP group IDs
   * @return The computed batch execution time
   */
  double ComputeBatchExecutionTime(
      std::size_t kvp_group_id,
      const std::vector<MutableSequencePtr>& extra_seqs = {},
      const std::vector<std::size_t>& extra_num_q_tokens = {},
      const std::vector<std::size_t>& extra_num_kv_tokens = {},
      const std::vector<std::size_t>& extra_num_active_kvp_groups = {},
      const std::vector<std::size_t>& extra_last_kvp_group_ids = {}) const;

  /**
   * @brief Gets the number of KV tokens for a sequence
   *
   * @param num_processed_tokens The number of tokens already processed
   * @param active_kvp_group_ids The active KVP group IDs
   * @param is_last_group Whether this is the last KVP group
   * @return The number of KV tokens
   */
  [[nodiscard]] std::size_t GetNumKvTokens(
      std::size_t num_processed_tokens,
      const std::vector<std::size_t>& active_kvp_group_ids,
      bool is_last_group) const;
};
//==============================================================================
}  // namespace vajra
//==============================================================================
