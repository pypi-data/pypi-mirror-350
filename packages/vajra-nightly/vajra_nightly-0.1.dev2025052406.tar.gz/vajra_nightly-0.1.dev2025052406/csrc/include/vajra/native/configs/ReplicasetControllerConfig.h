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
#include "native/configs/ReplicaControllerConfig.h"
#include "native/configs/ReplicasetSchedulerConfig.h"
#include "native/configs/RequestPrioritizerConfig.h"
//==============================================================================
namespace vajra {
//==============================================================================
struct BaseReplicasetControllerConfig {
  BaseReplicasetControllerConfig(
      const std::size_t num_replicas_param,
      const std::shared_ptr<BaseReplicaControllerConfig>&
          replica_controller_config_param,
      const std::shared_ptr<BaseRequestPrioritizerConfig>&
          request_prioritizer_config_param,
      const std::shared_ptr<BaseReplicasetSchedulerConfig>&
          replicaset_scheduler_config_param)
      : num_replicas(num_replicas_param),
        replica_controller_config(replica_controller_config_param),
        request_prioritizer_config(request_prioritizer_config_param),
        replicaset_scheduler_config(replicaset_scheduler_config_param) {
    ASSERT_VALID_POINTER_ARGUMENT(replica_controller_config_param);
    ASSERT_VALID_POINTER_ARGUMENT(request_prioritizer_config_param);
    ASSERT_VALID_POINTER_ARGUMENT(replicaset_scheduler_config_param);
  }

  virtual ~BaseReplicasetControllerConfig() = default;
  virtual ReplicasetControllerType GetType() const = 0;

  const std::size_t num_replicas;
  const std::shared_ptr<BaseReplicaControllerConfig> replica_controller_config;
  const std::shared_ptr<BaseRequestPrioritizerConfig>
      request_prioritizer_config;
  const std::shared_ptr<BaseReplicasetSchedulerConfig>
      replicaset_scheduler_config;

  /// @brief Convert to string representation
  /// @return String representation of the BaseReplicasetControllerConfig
  [[nodiscard]] virtual std::string ToString() const {
    return std::format(
        "BaseReplicasetControllerConfig(type={}, num_replicas={}, "
        "replica_controller_config={}, request_prioritizer_config={}, "
        "replicaset_scheduler_config={})",
        GetType(), num_replicas,
        replica_controller_config ? replica_controller_config->ToString()
                                  : kNullString,
        request_prioritizer_config ? request_prioritizer_config->ToString()
                                   : kNullString,
        replicaset_scheduler_config ? replicaset_scheduler_config->ToString()
                                    : kNullString);
  }
};
//==============================================================================
struct LlmReplicasetControllerConfig final
    : public BaseReplicasetControllerConfig {
  LlmReplicasetControllerConfig(
      const std::size_t num_replicas_param,
      const std::shared_ptr<LlmReplicaControllerConfig>&
          replica_controller_config_param,
      const std::shared_ptr<BaseRequestPrioritizerConfig>&
          request_prioritizer_config_param,
      const std::shared_ptr<BaseReplicasetSchedulerConfig>&
          replicaset_scheduler_config_param,
      const std::size_t num_tokenizer_workers_param)
      : BaseReplicasetControllerConfig(num_replicas_param,
                                       replica_controller_config_param,
                                       request_prioritizer_config_param,
                                       replicaset_scheduler_config_param),
        num_tokenizer_workers(num_tokenizer_workers_param) {
    ASSERT_VALID_POINTER_ARGUMENT(replica_controller_config_param);
    ASSERT_VALID_POINTER_ARGUMENT(request_prioritizer_config_param);
    ASSERT_VALID_POINTER_ARGUMENT(replicaset_scheduler_config_param);
  }

  ReplicasetControllerType GetType() const override {
    return ReplicasetControllerType::LLM;
  }

  const std::size_t num_tokenizer_workers;

  /// @brief Convert to string representation
  /// @return String representation of the LlmReplicasetControllerConfig
  [[nodiscard]] std::string ToString() const override {
    return std::format(
        "LlmReplicasetControllerConfig(num_tokenizer_workers={}, base={})",
        num_tokenizer_workers, BaseReplicasetControllerConfig::ToString());
  }
};
//==============================================================================
}  // namespace vajra
//==============================================================================
