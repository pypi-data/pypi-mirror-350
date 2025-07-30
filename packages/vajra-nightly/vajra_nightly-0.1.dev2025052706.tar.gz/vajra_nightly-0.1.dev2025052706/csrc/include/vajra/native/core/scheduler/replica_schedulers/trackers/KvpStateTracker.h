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
#include "commons/Logging.h"
#include "commons/StdCommon.h"
#include "native/configs/CacheConfig.h"
#include "native/configs/ModelConfig.h"
#include "native/configs/ParallelConfig.h"
#include "native/core/block_space_manager/BlockSpaceManager.h"
#include "native/core/scheduler/replica_schedulers/trackers/KvpBatchTracker.h"
#include "native/datatypes/Sequence.h"
//==============================================================================
namespace vajra {
//==============================================================================
// Data structure representing all info needed for a particular KVP group.
struct BatchTrackerGroupInfo {
  std::vector<MutableSequencePtr> sequences;
  std::vector<std::size_t> q_tokens;
  std::vector<std::size_t> kv_tokens;
  std::vector<std::size_t> active_group_ids;
  std::vector<std::size_t> last_group_ids;
};
//==============================================================================
/**
 * @brief Tracks KVP state information for sequence allocation and scheduling.
 *
 * This class manages the allocation and tracking of sequence blocks across KVP
 * groups. It handles the state of KVP groups, sequence allocations, and batch
 * formation.
 */
class KvpStateTracker : public NonCopyableNonMovable {
 public:
  /**
   * @brief Constructs a KvpStateTracker
   *
   * @param model_config The model configuration
   * @param cache_config The cache configuration
   * @param parallel_config The parallel configuration
   */
  KvpStateTracker(const ModelConfig& model_config,
                  const CacheConfig& cache_config,
                  const ParallelConfig& parallel_config,
                  const std::size_t num_gpu_blocks);

  /**
   * @brief Starts a new batch formation cycle
   */
  void StartBatchFormation();

  /**
   * @brief Gets Q tokens for the given sequence from the current batch tracker
   *
   * @param seq The sequence to get Q tokens for
   * @return List of Q token counts
   */
  [[nodiscard]] std::vector<std::size_t> GetBatchTrackerQTokens(
      const MutableSequencePtr seq) const;

  /**
   * @brief Gets the maximum number of tokens per KVP group
   *
   * @return Maximum number of tokens per KVP group
   */
  [[nodiscard]] std::size_t GetMaxNumTokensPerKvpGroup() const;

  /**
   * @brief Gets KVP groups that are not busy from the current batch tracker
   *
   * @return List of free KVP group IDs
   */
  [[nodiscard]] std::vector<std::size_t> GetBatchTrackerFreeGroups() const;

  /**
   * @brief Adds a sequence to the current batch tracker
   *
   * @param seq The sequence to add
   * @param num_q_tokens Number of Q tokens
   * @param active_kvp_group_ids List of active KVP group IDs
   */
  void AddSequenceToBatch(const MutableSequencePtr seq,
                          std::size_t num_q_tokens,
                          const std::vector<std::size_t>& active_kvp_group_ids);

  /**
   * @brief Gets all information for a specific KVP group from the current batch
   * tracker
   *
   * @param kvp_group_id The KVP group ID
   * @return BatchTrackerGroupInfo containing sequences, q_tokens, kv_tokens,
   * active_kvp_groups, and last_kvp_group_ids
   */
  [[nodiscard]] BatchTrackerGroupInfo GetBatchTrackerPerGroupInfo(
      std::size_t kvp_group_id) const;

  /**
   * @brief Gets the maximum sequence length
   *
   * @return Maximum sequence length
   */
  [[nodiscard]] std::size_t GetMaxSeqLen() const;

  /**
   * @brief Gets the allocation order for KVP groups
   *
   * @param kvp_group_ids List of KVP group IDs
   * @return Sorted list of KVP group IDs by pending work
   */
  [[nodiscard]] std::vector<std::size_t> GetAllocationOrder(
      const std::vector<std::size_t>& kvp_group_ids) const;

  /**
   * @brief Allocates memory for a sequence across KVP groups
   *
   * @param seq The sequence to allocate memory for
   * @return Pair of (success, num_blocks)
   */
  [[nodiscard]] std::pair<bool, std::size_t> Allocate(
      const MutableSequencePtr seq);

  /**
   * @brief Frees all memory allocated for a sequence
   *
   * @param seq The sequence to free
   */
  void FreeSeq(const MutableSequencePtr seq);

  /**
   * @brief Gets the last KVP group ID for a sequence
   *
   * @param seq The sequence
   * @return Last KVP group ID
   */
  [[nodiscard]] std::size_t GetLastKvGroupId(
      const MutableSequencePtr seq) const;

  /**
   * @brief Checks if a slot can be appended to the sequence
   *
   * @param seq The sequence
   * @return True if a slot can be appended
   */
  [[nodiscard]] bool CanAppendSlot(const MutableSequencePtr seq) const;

  /**
   * @brief Appends a slot to the sequence
   *
   * @param seq The sequence
   * @param num_total_blocks Total number of blocks
   * @return True if the slot was appended
   */
  bool AppendSlot(const MutableSequencePtr seq, std::size_t num_total_blocks);

  /**
   * @brief Gets the active KVP group IDs for a sequence
   *
   * @param seq The sequence
   * @return List of active KVP group IDs
   */
  [[nodiscard]] std::vector<std::size_t> GetActiveKvpGroupIds(
      const MutableSequencePtr seq) const;

  /**
   * @brief Updates the prefill work for a KVP group
   *
   * @param seq The sequence
   * @param current_tokens Current number of tokens
   * @param new_tokens New number of tokens
   */
  void UpdatePrefillWork(const MutableSequencePtr seq,
                         std::size_t current_tokens, std::size_t new_tokens);

  /**
   * @brief Gets the KVP group block counter for a sequence
   *
   * @param seq_id The sequence ID
   * @return Ordered map of KVP group IDs to block counts
   */
  [[nodiscard]] std::map<std::size_t, std::size_t> GetKvpGroupBlockCounter(
      const std::string& seq_id) const;

  /**
   * @brief Gets KV token info for a sequence
   *
   * @param seq The sequence
   * @param active_kvp_group_ids List of active KVP group IDs
   * @return Pair of (num_processed_tokens, kv_token_info)
   */
  [[nodiscard]] std::pair<std::size_t, std::vector<KvTokenInfo>>
  GetSequenceKvTokenInfo(
      const MutableSequencePtr seq,
      const std::vector<std::size_t>& active_kvp_group_ids) const;

  /**
   * @brief Gets the number of KVP groups
   *
   * @return The number of KVP groups (KV parallel size)
   */
  [[nodiscard]] std::size_t GetKvpSize() const { return kvp_size_; }

  /**
   * @brief Gets the batch tracker per group info for a KVP group
   *
   * @param kvp_group_id The KVP group ID
   * @return The batch tracker group info for the specified group
   */
  [[nodiscard]] std::vector<std::size_t> GetPerGroupNumProcessedTokens(
      std::size_t kvp_group_id) const;

 private:
  /**
   * @brief Ensures that a batch tracker exists
   */
  void EnsureBatchTracker();

  // Configuration
  ModelConfig model_config_;
  CacheConfig cache_config_;
  ParallelConfig parallel_config_;
  std::size_t num_gpu_blocks_;

  // KVP parameters
  std::size_t kvp_size_;
  std::size_t max_num_tokens_per_kvp_group_;
  std::size_t max_num_blocks_per_kvp_group_;
  std::size_t max_seq_len_;

  // Block managers
  std::unordered_map<std::size_t, std::unique_ptr<BlockSpaceManager>>
      block_managers_map_;

  // Sequence tracking
  using OrderedIntMap = std::map<std::size_t, std::size_t>;
  std::unordered_map<std::string, OrderedIntMap> seq_kvp_group_block_counter_;
  std::vector<std::size_t> kvp_group_pending_prefill_work_;

  // Current batch tracker
  std::unique_ptr<KvpBatchTracker> current_batch_tracker_;
};
//==============================================================================
}  // namespace vajra
//==============================================================================
