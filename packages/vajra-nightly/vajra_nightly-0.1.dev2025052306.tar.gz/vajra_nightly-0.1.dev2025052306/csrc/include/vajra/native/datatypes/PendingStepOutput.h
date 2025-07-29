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
#include "native/datatypes/SamplerOutput.h"
#include "native/datatypes/SchedulerOutput.h"
#include "native/datatypes/Sequence.h"
//==============================================================================
namespace vajra {
//==============================================================================
struct PendingStepOutput final {
  PendingStepOutput(const SchedulerOutputPtr scheduler_output_param,
                    const ValidSamplerOutputs sampler_outputs_param)
      : scheduler_output(scheduler_output_param),
        sampler_outputs(sampler_outputs_param) {
    ASSERT_VALID_POINTER_ARGUMENT(scheduler_output);
  }

  PendingStepOutput(const PendingStepOutput& other)
      : scheduler_output(other.scheduler_output),
        sampler_outputs(other.sampler_outputs) {}

  PendingStepOutput(PendingStepOutput&& other) noexcept
      : scheduler_output(std::move(other.scheduler_output)),
        sampler_outputs(std::move(other.sampler_outputs)) {}

  /// @brief Convert to string representation
  /// @return String representation of the PendingStepOutput
  [[nodiscard]] std::string ToString() const {
    return std::format(
        "PendingStepOutput(scheduler_output={}, sampler_outputs_count={})",
        scheduler_output, sampler_outputs.size());
  }

  const SchedulerOutputPtr scheduler_output;
  const ValidSamplerOutputs sampler_outputs;
};
//==============================================================================
}  // namespace vajra
//==============================================================================
