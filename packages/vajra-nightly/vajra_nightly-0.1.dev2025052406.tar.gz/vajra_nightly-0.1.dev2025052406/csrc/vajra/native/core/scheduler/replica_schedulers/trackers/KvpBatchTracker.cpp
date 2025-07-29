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
#include "native/core/scheduler/replica_schedulers/trackers/KvpBatchTracker.h"

using vajra::KvpBatchTracker;

namespace vajra {
// Constant for invalid KVP group ID
constexpr std::size_t INVALID_KVP_GROUP_ID =
    std::numeric_limits<std::size_t>::max();
//==============================================================================

KvpBatchTracker::KvpBatchTracker(std::size_t kvp_size /*[in]*/)
    : kvp_size_(kvp_size) {
  // Initialize the per KVP group trackers
  per_kvp_group_sequences_.resize(kvp_size);
  per_kvp_group_num_q_tokens_.resize(kvp_size);
  per_kvp_group_num_kv_tokens_.resize(kvp_size);
  per_kvp_group_num_active_kvp_groups_.resize(kvp_size);
  per_kvp_group_last_kvp_group_ids_.resize(kvp_size);
  per_kvp_group_seq_num_processed_tokens_.resize(kvp_size);
  per_kvp_group_total_num_q_tokens_.resize(kvp_size, 0);
}
//==============================================================================

void KvpBatchTracker::AddSequence(
    const MutableSequencePtr seq /*[in]*/, std::size_t num_q_tokens /*[in]*/,
    const std::vector<std::size_t>& active_kvp_group_ids /*[in]*/,
    const std::vector<KvTokenInfo>& kv_token_info /*[in]*/,
    std::size_t num_processed_tokens /*[in]*/) {
  ASSERT_VALID_POINTER_ARGUMENT(seq);

  // Add the sequence to each active KVP group
  for (std::size_t group_id : active_kvp_group_ids) {
    ASSERT_VALID_ARGUMENTS(group_id < kvp_size_, "Invalid KVP group ID: {}",
                           group_id);

    per_kvp_group_sequences_[group_id].push_back(seq);
    per_kvp_group_num_q_tokens_[group_id].push_back(num_q_tokens);
    per_kvp_group_num_active_kvp_groups_[group_id].push_back(
        active_kvp_group_ids.size());
    per_kvp_group_seq_num_processed_tokens_[group_id].push_back(
        num_processed_tokens);

    // Update the total number of Q tokens for this group
    per_kvp_group_total_num_q_tokens_[group_id] += num_q_tokens;

    if (!active_kvp_group_ids.empty()) {
      std::size_t last_kvp_group_id = active_kvp_group_ids.back();
      per_kvp_group_last_kvp_group_ids_[group_id].push_back(last_kvp_group_id);
    } else {
      per_kvp_group_last_kvp_group_ids_[group_id].push_back(
          INVALID_KVP_GROUP_ID);
    }
  }
  //==============================================================================

  // Process the KV token info
  for (const auto& token_info : kv_token_info) {
    ASSERT_VALID_ARGUMENTS(token_info.group_id < kvp_size_,
                           "Invalid KVP group ID in token info: {}",
                           token_info.group_id);

    per_kvp_group_num_kv_tokens_[token_info.group_id].push_back(
        token_info.num_tokens);
  }
}
//==============================================================================
std::vector<std::size_t> KvpBatchTracker::GetQTokensForKvpGroups(
    const std::vector<std::size_t>& active_kvp_group_ids /*[in]*/) const {
  std::vector<std::size_t> q_tokens;
  for (std::size_t group_id : active_kvp_group_ids) {
    ASSERT_VALID_ARGUMENTS(group_id < kvp_size_, "Invalid KVP group ID: {}",
                           group_id);

    q_tokens.push_back(per_kvp_group_total_num_q_tokens_[group_id]);
  }
  return q_tokens;
}
//==============================================================================

std::vector<std::size_t> KvpBatchTracker::GetFreeKvpGroups(
    std::size_t token_threshold /*[in]*/) const {
  std::vector<std::size_t> free_groups;
  for (std::size_t group_id = 0; group_id < kvp_size_; ++group_id) {
    if (per_kvp_group_total_num_q_tokens_[group_id] <= token_threshold) {
      free_groups.push_back(group_id);
    }
  }
  return free_groups;
}
//==============================================================================

std::vector<MutableSequencePtr> KvpBatchTracker::GetPerGroupSequences(
    std::size_t kvp_group_id /*[in]*/) const {
  ASSERT_VALID_ARGUMENTS(kvp_group_id < kvp_size_, "Invalid KVP group ID: {}",
                         kvp_group_id);

  return per_kvp_group_sequences_[kvp_group_id];
}
//==============================================================================

std::vector<std::size_t> KvpBatchTracker::GetPerGroupQTokens(
    std::size_t kvp_group_id /*[in]*/) const {
  ASSERT_VALID_ARGUMENTS(kvp_group_id < kvp_size_, "Invalid KVP group ID: {}",
                         kvp_group_id);

  return per_kvp_group_num_q_tokens_[kvp_group_id];
}
//==============================================================================

std::vector<std::size_t> KvpBatchTracker::GetPerGroupKvTokens(
    std::size_t kvp_group_id /*[in]*/) const {
  ASSERT_VALID_ARGUMENTS(kvp_group_id < kvp_size_, "Invalid KVP group ID: {}",
                         kvp_group_id);

  return per_kvp_group_num_kv_tokens_[kvp_group_id];
}
//==============================================================================

std::vector<std::size_t> KvpBatchTracker::GetPerGroupActiveKvpGroups(
    std::size_t kvp_group_id /*[in]*/) const {
  ASSERT_VALID_ARGUMENTS(kvp_group_id < kvp_size_, "Invalid KVP group ID: {}",
                         kvp_group_id);

  return per_kvp_group_num_active_kvp_groups_[kvp_group_id];
}
//==============================================================================

std::vector<std::size_t> KvpBatchTracker::GetPerGroupLastKvpGroupIds(
    std::size_t kvp_group_id /*[in]*/) const {
  ASSERT_VALID_ARGUMENTS(kvp_group_id < kvp_size_, "Invalid KVP group ID: {}",
                         kvp_group_id);

  return per_kvp_group_last_kvp_group_ids_[kvp_group_id];
}
//==============================================================================

std::vector<std::size_t> KvpBatchTracker::GetPerGroupNumProcessedTokens(
    std::size_t kvp_group_id /*[in]*/) const {
  return per_kvp_group_seq_num_processed_tokens_[kvp_group_id];
}
}  // namespace vajra
