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
#include "native/configs/ModelConfig.h"
#include "native/configs/ParallelConfig.h"
//==============================================================================
namespace vajra {
//==============================================================================
struct ReplicaResourceConfig final {
  ReplicaResourceConfig(ParallelConfig parallel_config,
                        ModelConfig model_config)
      : pipeline_parallel_size(parallel_config.pipeline_parallel_size),
        tensor_parallel_size(parallel_config.tensor_parallel_size),
        kv_parallel_size(parallel_config.kv_parallel_size),
        world_size(parallel_config.world_size),
        local_num_layers(model_config.total_num_layers /
                         parallel_config.pipeline_parallel_size),
        total_num_layers(model_config.total_num_layers) {
    ASSERT_VALID_ARGUMENTS(local_num_layers >= 1,
                           "Total number of layers must be at least 1. Got {}",
                           local_num_layers);
  }

  std::string ToString() const {
    return std::format(
        "ReplicaResourceConfig("
        "Tensor Parallel Size: {}, "
        "Pipeline Parallel Size: {}, "
        "KV Parallel Size: {}, "
        "Local number of layers: {}, "
        "Total number of layers: {})",
        tensor_parallel_size, pipeline_parallel_size, kv_parallel_size,
        local_num_layers, total_num_layers);
  }

  const std::size_t pipeline_parallel_size;
  const std::size_t tensor_parallel_size;
  const std::size_t kv_parallel_size;
  const std::size_t world_size;
  const std::size_t local_num_layers;
  const std::size_t total_num_layers;
};
//==============================================================================
using GlobalResourceConfig = std::vector<ReplicaResourceConfig>;
//==============================================================================
}  // namespace vajra
//==============================================================================
