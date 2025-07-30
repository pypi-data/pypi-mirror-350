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
#include "commons/StringUtils.h"
//==============================================================================
namespace vajra {
//==============================================================================
struct SequenceScheduleMetadata final {
  SequenceScheduleMetadata(const std::size_t schedule_id_param,
                           const std::string seq_id_param,
                           const std::size_t num_q_tokens_param,
                           const std::unordered_map<std::size_t, std::size_t>
                               kvp_group_block_counter_param,
                           const std::vector<std::size_t> kvp_group_ids_param)
      : schedule_id(schedule_id_param),
        seq_id(seq_id_param),
        num_q_tokens(num_q_tokens_param),
        kvp_group_block_counter(kvp_group_block_counter_param),
        kvp_group_ids(kvp_group_ids_param),
        is_kvp_request(kvp_group_ids_param.size() > 1) {}

  /// @brief Convert to string representation
  /// @return String representation of the SequenceScheduleMetadata
  [[nodiscard]] std::string ToString() const {
    return std::format(
        "SequenceScheduleMetadata(schedule_id={}, seq_id={}, num_q_tokens={}, "
        "is_kvp_request={}, kvp_group_ids=[{}], kvp_group_blocks={})",
        schedule_id, seq_id, num_q_tokens, is_kvp_request,
        JoinStrings(kvp_group_ids, ", "), kvp_group_block_counter.size());
  }

  const std::size_t schedule_id;
  const std::string seq_id;
  const std::size_t num_q_tokens;
  const std::unordered_map<std::size_t, std::size_t> kvp_group_block_counter;
  const std::vector<std::size_t> kvp_group_ids;
  const bool is_kvp_request;
};
//==============================================================================
using SequenceScheduleMetadataPtr =
    std::shared_ptr<const SequenceScheduleMetadata>;
using SequenceScheduleMetadataPtrList =
    std::vector<SequenceScheduleMetadataPtr>;
//==============================================================================
}  // namespace vajra
//==============================================================================
