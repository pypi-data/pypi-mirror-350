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
#include "native/enums/Enums.h"
//==============================================================================
namespace vajra {
//==============================================================================
//==============================================================================
struct BaseReplicasetSchedulerConfig {
  virtual ~BaseReplicasetSchedulerConfig() = default;
  virtual ReplicasetSchedulerType GetType() const = 0;

  /// @brief Convert to string representation
  /// @return String representation of the BaseReplicasetSchedulerConfig
  [[nodiscard]] virtual std::string ToString() const {
    return std::format("BaseReplicasetSchedulerConfig(type={})", GetType());
  }
};
//==============================================================================
struct PullReplicasetSchedulerConfig final
    : public BaseReplicasetSchedulerConfig {
  ReplicasetSchedulerType GetType() const override {
    return ReplicasetSchedulerType::PULL;
  }

  /// @brief Convert to string representation
  /// @return String representation of the PullReplicasetSchedulerConfig
  [[nodiscard]] std::string ToString() const override {
    return std::format("PullReplicasetSchedulerConfig()");
  }
};
//==============================================================================
struct RoundRobinReplicasetSchedulerConfig final
    : public BaseReplicasetSchedulerConfig {
  ReplicasetSchedulerType GetType() const override {
    return ReplicasetSchedulerType::ROUND_ROBIN;
  }

  /// @brief Convert to string representation
  /// @return String representation of the RoundRobinReplicasetSchedulerConfig
  [[nodiscard]] std::string ToString() const override {
    return std::format("RoundRobinReplicasetSchedulerConfig()");
  }
};
//==============================================================================
}  // namespace vajra
//==============================================================================
