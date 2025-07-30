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
#include "commons/TorchCommon.h"
#include "native/configs/ReplicaResourceConfig.h"
#include "native/enums/Enums.h"
//==============================================================================
namespace vajra {
//==============================================================================
struct TransferEngineConfig final {
  TransferEngineConfig(
      TransferBackendType transfer_backend_type_param,
      std::size_t global_rank_param,
      const GlobalResourceConfig& global_resource_config_param,
      const c10::intrusive_ptr<c10d::ProcessGroup> global_process_group_param)
      : transfer_backend_type(transfer_backend_type_param),
        global_rank(global_rank_param),
        global_resource_config(global_resource_config_param),
        global_process_group(global_process_group_param) {}

  /// @brief Convert to string representation
  /// @return String representation of the TransferEngineConfig
  [[nodiscard]] std::string ToString() const {
    return std::format(
        "TransferEngineConfig(transfer_backend_type={}, global_rank={})",
        transfer_backend_type, global_rank);
  }

  const TransferBackendType transfer_backend_type;
  const std::size_t global_rank;
  const GlobalResourceConfig global_resource_config;
  const c10::intrusive_ptr<c10d::ProcessGroup> global_process_group;
};
//==============================================================================
}  // namespace vajra
//==============================================================================
