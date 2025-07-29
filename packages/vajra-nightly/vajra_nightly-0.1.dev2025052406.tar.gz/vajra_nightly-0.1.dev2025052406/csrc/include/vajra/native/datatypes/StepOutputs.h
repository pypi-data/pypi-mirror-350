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
#include "commons/StringUtils.h"
#include "native/datatypes/SamplerOutput.h"
//==============================================================================
namespace vajra {
struct StepOutputs {
  StepOutputs(std::size_t schedule_id_param /*[in]*/,
              const SamplerOutputs sampler_outputs_param /*[in]*/)
      : schedule_id(schedule_id_param),
        sampler_outputs(sampler_outputs_param) {}

  std::string ToString() const {
    std::vector<std::string> sampler_output_strings;
    for (const auto& output : sampler_outputs) {
      sampler_output_strings.push_back(std::format(
          "{}", output.has_value() ? output.value()->ToString() : kNullString));
    }
    return std::format("StepOutputs(ScheduleId: {}, SamplerOutputs: {})",
                       schedule_id, JoinStrings(sampler_output_strings, ", "));
  }

  const std::size_t schedule_id;
  const SamplerOutputs sampler_outputs;
};
//==============================================================================
using StepOutputsPtr = std::shared_ptr<const StepOutputs>;
//==============================================================================
}  // namespace vajra
//==============================================================================
