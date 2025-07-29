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
//==============================================================================
namespace vajra {
//==============================================================================
struct ParallelConfig final {
  ParallelConfig(std::size_t pipeline_parallel_size_param,
                 std::size_t tensor_parallel_size_param,
                 bool enable_expert_parallel_param,
                 bool enable_sequence_pipeline_parallel_param,
                 bool enable_chunked_pipeline_comm_opt,
                 std::size_t kv_parallel_size_param,
                 std::size_t max_num_tokens_per_kvp_group_param)
      : pipeline_parallel_size(pipeline_parallel_size_param),
        tensor_parallel_size(tensor_parallel_size_param),
        enable_expert_parallel(enable_expert_parallel_param),
        enable_sequence_pipeline_parallel(
            enable_sequence_pipeline_parallel_param),
        enable_chunked_pipeline_comm_opt(enable_chunked_pipeline_comm_opt),
        kv_parallel_size(kv_parallel_size_param),
        max_num_tokens_per_kvp_group(max_num_tokens_per_kvp_group_param),
        world_size(pipeline_parallel_size_param * tensor_parallel_size_param *
                   kv_parallel_size_param) {}

  /// @brief Convert to string representation
  /// @return String representation of the ParallelConfig
  [[nodiscard]] std::string ToString() const {
    return std::format(
        "ParallelConfig(pipeline_parallel_size={}, tensor_parallel_size={}, "
        "enable_expert_parallel={}, enable_sequence_pipeline_parallel={}, "
        "enable_chunked_pipeline_comm_opt={}, kv_parallel_size={}, "
        "max_num_tokens_per_kvp_group={}, world_size={})",
        pipeline_parallel_size, tensor_parallel_size, enable_expert_parallel,
        enable_sequence_pipeline_parallel, enable_chunked_pipeline_comm_opt,
        kv_parallel_size, max_num_tokens_per_kvp_group, world_size);
  }

  const std::size_t pipeline_parallel_size;
  const std::size_t tensor_parallel_size;
  const bool enable_expert_parallel;
  const bool enable_sequence_pipeline_parallel;
  const bool enable_chunked_pipeline_comm_opt;
  const std::size_t kv_parallel_size;
  const std::size_t max_num_tokens_per_kvp_group;
  const std::size_t world_size;
};
//==============================================================================
}  // namespace vajra
//==============================================================================
