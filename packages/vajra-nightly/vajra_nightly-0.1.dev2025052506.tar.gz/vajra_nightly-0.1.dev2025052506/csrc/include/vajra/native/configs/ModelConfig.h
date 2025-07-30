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
#include "commons/Constants.h"
#include "commons/StdCommon.h"
#include "native/configs/ParallelConfig.h"
//==============================================================================
namespace vajra {
//==============================================================================
struct ModelConfig final {
  ModelConfig(std::string model_param, bool trust_remote_code_param,
              std::optional<std::string> download_dir_param,
              std::string load_format_param, std::string dtype_param,
              std::size_t seed_param, std::optional<std::string> revision_param,
              std::size_t max_model_len_param, std::size_t num_layers_param,
              std::size_t total_num_q_heads_param,
              std::size_t total_num_kv_heads_param, std::size_t hidden_size)
      : model(model_param),
        trust_remote_code(trust_remote_code_param),
        download_dir(download_dir_param),
        load_format(load_format_param),
        dtype(dtype_param),
        seed(seed_param),
        revision(revision_param),
        max_model_len(max_model_len_param),
        total_num_layers(num_layers_param),
        total_num_q_heads(total_num_q_heads_param),
        total_num_kv_heads(total_num_kv_heads_param),
        hidden_size(hidden_size) {}

  std::size_t GetHeadSize() const { return hidden_size / total_num_q_heads; }

  std::size_t GetNumLayers(const ParallelConfig& parallel_config) const {
    return total_num_layers / parallel_config.pipeline_parallel_size;
  }

  std::size_t GetNumKVHeads(const ParallelConfig& parallel_config) const {
    return total_num_kv_heads / parallel_config.tensor_parallel_size;
  }

  std::size_t GetNumQHeads(const ParallelConfig& parallel_config) const {
    return total_num_q_heads / parallel_config.tensor_parallel_size;
  }

  /// @brief Convert to string representation
  /// @return String representation of the ModelConfig
  [[nodiscard]] std::string ToString() const {
    return std::format(
        "ModelConfig(model={}, trust_remote_code={}, download_dir={}, "
        "load_format={}, dtype={}, seed={}, revision={}, max_model_len={}, "
        "total_num_layers={}, total_num_q_heads={}, total_num_kv_heads={}, "
        "hidden_size={})",
        model, trust_remote_code,
        download_dir.has_value() ? download_dir.value() : kNullString,
        load_format, dtype, seed,
        revision.has_value() ? revision.value() : kNullString, max_model_len,
        total_num_layers, total_num_q_heads, total_num_kv_heads, hidden_size);
  }

  const std::string model;
  const bool trust_remote_code;
  const std::optional<std::string> download_dir;
  const std::string load_format;
  const std::string dtype;
  const std::size_t seed;
  const std::optional<std::string> revision;
  const std::size_t max_model_len;
  const std::size_t total_num_layers;
  const std::size_t total_num_q_heads;
  const std::size_t total_num_kv_heads;
  const std::size_t hidden_size;
};
//==============================================================================
}  // namespace vajra
//==============================================================================
