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
#include <zmq.hpp>
//==============================================================================
#include "commons/StdCommon.h"
//==============================================================================
namespace vajra {
//==============================================================================
enum class ReplicasetSchedulerType { PULL, ROUND_ROBIN };
//==============================================================================
enum class ReplicasetControllerType { LLM };
//==============================================================================
enum class ReplicaControllerType { LLM_BASE, LLM_PIPELINE_PARALLEL };
//==============================================================================
enum class ReplicaSchedulerType { FIXED_CHUNK, DYNAMIC_CHUNK, SPACE_SHARING };
//==============================================================================
enum class RequestPrioritizerType { FCFS, EDF, LRS };
//==============================================================================
enum class MetricsStoreType { ENGINE, WORKER };
//==============================================================================
enum class TransferBackendType { TORCH = 0 };
//==============================================================================
enum class TransferOperationRanksType { MATCHING = 0, ALL = 1, SINGLE = 2 };
//==============================================================================
enum class ZmqConstants {
  PUB = ZMQ_PUB,
  SUB = ZMQ_SUB,
  PUSH = ZMQ_PUSH,
  PULL = ZMQ_PULL,
  SUBSCRIBE = ZMQ_SUBSCRIBE
};
//==============================================================================
}  // namespace vajra
//==============================================================================
// std::formatter specializations for enums
//==============================================================================
template <>
struct std::formatter<vajra::ReplicasetSchedulerType>
    : std::formatter<std::string_view> {
  template <typename FormatContext>
  auto format(vajra::ReplicasetSchedulerType type, FormatContext& ctx) const {
    std::string_view name = "UNKNOWN";
    switch (type) {
      case vajra::ReplicasetSchedulerType::PULL:
        name = "PULL";
        break;
      case vajra::ReplicasetSchedulerType::ROUND_ROBIN:
        name = "ROUND_ROBIN";
        break;
    }
    return std::formatter<std::string_view>::format(name, ctx);
  }
};
//==============================================================================
template <>
struct std::formatter<vajra::ReplicasetControllerType>
    : std::formatter<std::string_view> {
  template <typename FormatContext>
  auto format(vajra::ReplicasetControllerType type, FormatContext& ctx) const {
    std::string_view name = "UNKNOWN";
    switch (type) {
      case vajra::ReplicasetControllerType::LLM:
        name = "LLM";
        break;
    }
    return std::formatter<std::string_view>::format(name, ctx);
  }
};
//==============================================================================
template <>
struct std::formatter<vajra::ReplicaControllerType>
    : std::formatter<std::string_view> {
  template <typename FormatContext>
  auto format(vajra::ReplicaControllerType type, FormatContext& ctx) const {
    std::string_view name = "UNKNOWN";
    switch (type) {
      case vajra::ReplicaControllerType::LLM_BASE:
        name = "LLM_BASE";
        break;
      case vajra::ReplicaControllerType::LLM_PIPELINE_PARALLEL:
        name = "LLM_PIPELINE_PARALLEL";
        break;
    }
    return std::formatter<std::string_view>::format(name, ctx);
  }
};
//==============================================================================
template <>
struct std::formatter<vajra::ReplicaSchedulerType>
    : std::formatter<std::string_view> {
  template <typename FormatContext>
  auto format(vajra::ReplicaSchedulerType type, FormatContext& ctx) const {
    std::string_view name = "UNKNOWN";
    switch (type) {
      case vajra::ReplicaSchedulerType::FIXED_CHUNK:
        name = "FIXED_CHUNK";
        break;
      case vajra::ReplicaSchedulerType::DYNAMIC_CHUNK:
        name = "DYNAMIC_CHUNK";
        break;
      case vajra::ReplicaSchedulerType::SPACE_SHARING:
        name = "SPACE_SHARING";
        break;
    }
    return std::formatter<std::string_view>::format(name, ctx);
  }
};
//==============================================================================
template <>
struct std::formatter<vajra::RequestPrioritizerType>
    : std::formatter<std::string_view> {
  template <typename FormatContext>
  auto format(vajra::RequestPrioritizerType type, FormatContext& ctx) const {
    std::string_view name = "UNKNOWN";
    switch (type) {
      case vajra::RequestPrioritizerType::FCFS:
        name = "FCFS";
        break;
      case vajra::RequestPrioritizerType::EDF:
        name = "EDF";
        break;
      case vajra::RequestPrioritizerType::LRS:
        name = "LRS";
        break;
    }
    return std::formatter<std::string_view>::format(name, ctx);
  }
};
//==============================================================================
template <>
struct std::formatter<vajra::MetricsStoreType>
    : std::formatter<std::string_view> {
  template <typename FormatContext>
  auto format(vajra::MetricsStoreType type, FormatContext& ctx) const {
    std::string_view name = "UNKNOWN";
    switch (type) {
      case vajra::MetricsStoreType::ENGINE:
        name = "ENGINE";
        break;
      case vajra::MetricsStoreType::WORKER:
        name = "WORKER";
        break;
    }
    return std::formatter<std::string_view>::format(name, ctx);
  }
};
//==============================================================================
template <>
struct std::formatter<vajra::TransferBackendType>
    : std::formatter<std::string_view> {
  template <typename FormatContext>
  auto format(vajra::TransferBackendType type, FormatContext& ctx) const {
    std::string_view name = "UNKNOWN";
    switch (type) {
      case vajra::TransferBackendType::TORCH:
        name = "TORCH";
        break;
    }
    return std::formatter<std::string_view>::format(name, ctx);
  }
};
//==============================================================================
template <>
struct std::formatter<vajra::TransferOperationRanksType>
    : std::formatter<std::string_view> {
  template <typename FormatContext>
  auto format(vajra::TransferOperationRanksType type,
              FormatContext& ctx) const {
    std::string_view name = "UNKNOWN";
    switch (type) {
      case vajra::TransferOperationRanksType::MATCHING:
        name = "MATCHING";
        break;
      case vajra::TransferOperationRanksType::ALL:
        name = "ALL";
        break;
      case vajra::TransferOperationRanksType::SINGLE:
        name = "SINGLE";
        break;
    }
    return std::formatter<std::string_view>::format(name, ctx);
  }
};
//==============================================================================
