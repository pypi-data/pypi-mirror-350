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
#include "native/datatypes/Sequence.h"
//==============================================================================
namespace vajra {
//==============================================================================
// Constant for allocation token threshold
constexpr std::size_t ALLOCATION_MAX_TOKEN_THRESHOLD = 500;
//==============================================================================
/**
 * @brief Structure to hold KV token information
 *
 * This structure encapsulates information about token allocation for KVP
 * groups.
 */
struct KvTokenInfo {
  std::size_t group_id;    // KVP group ID
  std::size_t num_tokens;  // Number of tokens
  bool is_prefill;         // Whether this is a prefill operation
};
//==============================================================================
/**
 * @brief Tracks KVP-specific batch information for a scheduling cycle.
 *
 * This class tracks batching information for KVP groups, managing sequences,
 * tokens counts, and allocation tracking for KVP-based scheduling.
 */
class KvpBatchTracker : public NonCopyableNonMovable {
 public:
  /**
   * @brief Constructs a KvpBatchTracker
   *
   * @param kvp_size Number of KVP groups to track
   */
  explicit KvpBatchTracker(std::size_t kvp_size /*[in]*/);

  /**
   * @brief Adds a sequence to be tracked
   *
   * @param seq The sequence to add
   * @param num_q_tokens Number of Q tokens
   * @param active_kvp_group_ids List of active KVP group IDs
   * @param kv_token_info List of KV token info
   * @param num_processed_tokens Number of tokens already processed
   */
  void AddSequence(
      const MutableSequencePtr seq /*[in]*/, std::size_t num_q_tokens /*[in]*/,
      const std::vector<std::size_t>& active_kvp_group_ids /*[in]*/,
      const std::vector<KvTokenInfo>& kv_token_info /*[in]*/,
      std::size_t num_processed_tokens /*[in]*/);

  /**
   * @brief Gets Q tokens for the given KVP groups
   *
   * @param active_kvp_group_ids List of active KVP group IDs
   * @return List of Q token counts for each active KVP group
   */
  [[nodiscard]] std::vector<std::size_t> GetQTokensForKvpGroups(
      const std::vector<std::size_t>& active_kvp_group_ids /*[in]*/) const;

  /**
   * @brief Gets KVP groups that are not busy
   *
   * @param token_threshold Token threshold for considering a group as free
   * @return List of free KVP group IDs
   */
  [[nodiscard]] std::vector<std::size_t> GetFreeKvpGroups(
      std::size_t token_threshold =
          ALLOCATION_MAX_TOKEN_THRESHOLD /*[in]*/) const;

  /**
   * @brief Gets sequences belonging to a specific KVP group
   *
   * @param kvp_group_id The KVP group ID
   * @return List of sequences in the group
   */
  [[nodiscard]] std::vector<MutableSequencePtr> GetPerGroupSequences(
      std::size_t kvp_group_id /*[in]*/) const;

  /**
   * @brief Gets Q token counts for a specific KVP group
   *
   * @param kvp_group_id The KVP group ID
   * @return List of Q token counts for the sequences in the group
   */
  [[nodiscard]] std::vector<std::size_t> GetPerGroupQTokens(
      std::size_t kvp_group_id /*[in]*/) const;

  /**
   * @brief Gets KV token counts for a specific KVP group
   *
   * @param kvp_group_id The KVP group ID
   * @return List of KV token counts for the sequences in the group
   */
  [[nodiscard]] std::vector<std::size_t> GetPerGroupKvTokens(
      std::size_t kvp_group_id /*[in]*/) const;

  /**
   * @brief Gets active KVP groups for each sequence in a specific KVP group
   *
   * @param kvp_group_id The KVP group ID
   * @return List of active KVP group counts for the sequences in the group
   */
  [[nodiscard]] std::vector<std::size_t> GetPerGroupActiveKvpGroups(
      std::size_t kvp_group_id /*[in]*/) const;

  /**
   * @brief Gets the last KVP group IDs for the sequences in a specific KVP
   * group
   *
   * @param kvp_group_id The KVP group ID
   * @return List of last KVP group IDs for the sequences in the group
   */
  [[nodiscard]] std::vector<std::size_t> GetPerGroupLastKvpGroupIds(
      std::size_t kvp_group_id /*[in]*/) const;

  /**
   * @brief Gets the number of processed tokens for sequences in a specific KVP
   * group
   *
   * @param kvp_group_id The KVP group ID
   * @return List of processed token counts for the sequences in the group
   */
  [[nodiscard]] std::vector<std::size_t> GetPerGroupNumProcessedTokens(
      std::size_t kvp_group_id /*[in]*/) const;

 private:
  // Number of KVP groups
  std::size_t kvp_size_;

  // Per KVP group tracking
  std::vector<std::vector<MutableSequencePtr>> per_kvp_group_sequences_;
  std::vector<std::vector<std::size_t>> per_kvp_group_num_q_tokens_;
  std::vector<std::vector<std::size_t>> per_kvp_group_num_kv_tokens_;
  std::vector<std::vector<std::size_t>> per_kvp_group_num_active_kvp_groups_;
  std::vector<std::vector<std::size_t>> per_kvp_group_last_kvp_group_ids_;
  std::vector<std::vector<std::size_t>> per_kvp_group_seq_num_processed_tokens_;
  std::vector<std::size_t> per_kvp_group_total_num_q_tokens_;
};
//==============================================================================
}  // namespace vajra
//==============================================================================
