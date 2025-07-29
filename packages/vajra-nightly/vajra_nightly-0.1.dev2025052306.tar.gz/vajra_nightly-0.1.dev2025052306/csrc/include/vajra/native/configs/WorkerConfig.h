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
struct WorkerConfig final {
  WorkerConfig(float gpu_memory_utilization_param,
               bool use_native_execution_backend_param)
      : gpu_memory_utilization(gpu_memory_utilization_param),
        use_native_execution_backend(use_native_execution_backend_param) {}

  /// @brief Convert to string representation
  /// @return String representation of the WorkerConfig
  [[nodiscard]] std::string ToString() const {
    return std::format(
        "WorkerConfig(gpu_memory_utilization={}, "
        "use_native_execution_backend={})",
        gpu_memory_utilization, use_native_execution_backend);
  }

  const float gpu_memory_utilization;
  const bool use_native_execution_backend;
};
//==============================================================================
}  // namespace vajra
//==============================================================================
