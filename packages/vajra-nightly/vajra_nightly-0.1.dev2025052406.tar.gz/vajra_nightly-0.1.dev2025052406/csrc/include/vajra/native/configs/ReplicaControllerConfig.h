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
#include "commons/Logging.h"
#include "commons/StdCommon.h"
#include "native/configs/CacheConfig.h"
#include "native/configs/ModelConfig.h"
#include "native/configs/ParallelConfig.h"
#include "native/configs/ReplicaSchedulerConfig.h"
#include "native/configs/WorkerConfig.h"
#include "native/enums/Enums.h"
//==============================================================================
namespace vajra {
//==============================================================================
struct BaseReplicaControllerConfig {
  BaseReplicaControllerConfig(
      const ModelConfig& model_config_param,
      const WorkerConfig& worker_config_param,
      const CacheConfig& cache_config_param,
      const ParallelConfig& parallel_config_param,
      const std::shared_ptr<BaseReplicaSchedulerConfig>& scheduler_config_param)
      : model_config(model_config_param),
        worker_config(worker_config_param),
        cache_config(cache_config_param),
        parallel_config(parallel_config_param),
        scheduler_config(scheduler_config_param) {
    ASSERT_VALID_POINTER_ARGUMENT(scheduler_config_param);
  }

  virtual ~BaseReplicaControllerConfig() = default;
  virtual ReplicaControllerType GetType() const = 0;

  /// @brief Convert to string representation
  /// @return String representation of the BaseReplicaControllerConfig
  [[nodiscard]] virtual std::string ToString() const {
    return std::format(
        "BaseReplicaControllerConfig(type={}, model_config={}, "
        "worker_config={}, cache_config={}, parallel_config={}, "
        "scheduler_config={})",
        GetType(), model_config.ToString(), worker_config.ToString(),
        cache_config.ToString(), parallel_config.ToString(),
        scheduler_config ? scheduler_config->ToString() : kNullString);
  }

  const ModelConfig model_config;
  const WorkerConfig worker_config;
  const CacheConfig cache_config;
  const ParallelConfig parallel_config;
  const std::shared_ptr<BaseReplicaSchedulerConfig> scheduler_config;
};
//==============================================================================
struct LlmReplicaControllerConfig final : public BaseReplicaControllerConfig {
  LlmReplicaControllerConfig(
      const ModelConfig& model_config_param,
      const WorkerConfig& worker_config_param,
      const CacheConfig& cache_config_param,
      const ParallelConfig& parallel_config_param,
      const std::shared_ptr<BaseReplicaSchedulerConfig>& scheduler_config_param)
      : BaseReplicaControllerConfig(model_config_param, worker_config_param,
                                    cache_config_param, parallel_config_param,
                                    scheduler_config_param) {
    ASSERT_VALID_POINTER_ARGUMENT(scheduler_config_param);
  }

  ReplicaControllerType GetType() const override {
    return ReplicaControllerType::LLM_BASE;
  }

  /// @brief Convert to string representation
  /// @return String representation of the LlmReplicaControllerConfig
  [[nodiscard]] std::string ToString() const override {
    return std::format("LlmReplicaControllerConfig({})",
                       BaseReplicaControllerConfig::ToString());
  }
};
//==============================================================================
}  // namespace vajra
//==============================================================================
