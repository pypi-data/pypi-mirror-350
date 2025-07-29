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
#include "commons/Logging.h"
#include "commons/StdCommon.h"
//==============================================================================
namespace vajra {
//==============================================================================
struct SequenceMetadata final {
  SequenceMetadata(std::size_t schedule_id_param /*[in]*/,
                   const std::string seq_id_param /*[in]*/,
                   std::size_t num_q_tokens_param /*[in]*/,
                   std::size_t num_kv_tokens_param /*[in]*/,
                   const std::vector<int> block_table_param /*[in]*/,
                   const std::vector<std::size_t> kvp_group_ids_param /*[in]*/,
                   bool save_kv_cache_param /*[in]*/)
      : schedule_id(schedule_id_param),
        seq_id(seq_id_param),
        num_q_tokens(num_q_tokens_param),
        num_kv_tokens(num_kv_tokens_param),
        block_table(block_table_param),
        kvp_group_ids(kvp_group_ids_param),
        save_kv_cache(save_kv_cache_param),
        is_kvp_request(kvp_group_ids_param.size() > 1) {}

  std::string ToString() const {
    return std::format(
        "SequenceMetadata("
        "ScheduleId: {}, "
        "SeqId: {}, "
        "NumQTokens: {}, "
        "NumKvTokens: {}, "
        "KvpGroupIds: [{}], "
        "SaveKvCache: {}, "
        "IsKvpRequest: {})",
        schedule_id, seq_id, num_q_tokens, num_kv_tokens,
        JoinStrings(kvp_group_ids, ", "), save_kv_cache, is_kvp_request);
  }

  const std::size_t schedule_id;
  const std::string seq_id;
  const std::size_t num_q_tokens;
  const std::size_t num_kv_tokens;
  const std::vector<int> block_table;
  const std::vector<std::size_t> kvp_group_ids;
  const bool save_kv_cache;
  const bool is_kvp_request;
};

using SequenceMetadataPtr = std::shared_ptr<const SequenceMetadata>;
using SequenceMetadataVector = std::vector<SequenceMetadataPtr>;
//==============================================================================
}  // namespace vajra
//==============================================================================
