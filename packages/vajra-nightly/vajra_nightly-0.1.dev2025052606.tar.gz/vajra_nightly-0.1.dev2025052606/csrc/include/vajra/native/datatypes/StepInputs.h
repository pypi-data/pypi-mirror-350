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
#include "native/datatypes/PendingStepOutput.h"
#include "native/datatypes/SamplerOutput.h"
#include "native/datatypes/SchedulerOutput.h"
#include "native/datatypes/Sequence.h"
//==============================================================================
namespace vajra {
//==============================================================================
struct StepInputs {
  StepInputs(
      const SchedulerOutputPtr scheduler_output_param,
      const std::vector<SequenceParams> new_seq_params_param = {},
      const std::vector<PendingStepOutput> pending_step_outputs_param = {})
      : scheduler_output(scheduler_output_param),
        new_seq_params(new_seq_params_param),
        pending_step_outputs(pending_step_outputs_param) {
    ASSERT_VALID_POINTER_ARGUMENT(scheduler_output);
  }

  /// @brief Convert to string representation
  /// @return String representation of the StepInputs
  [[nodiscard]] std::string ToString() const {
    return std::format(
        "StepInputs(scheduler_output={}, new_seq_params_count={}, "
        "pending_step_outputs_count={})",
        scheduler_output, new_seq_params.size(), pending_step_outputs.size());
  }

  const SchedulerOutputPtr scheduler_output;
  const std::vector<SequenceParams> new_seq_params;
  const std::vector<PendingStepOutput> pending_step_outputs;
};
using StepInputsPtr = std::shared_ptr<const StepInputs>;
//==============================================================================
}  // namespace vajra
//==============================================================================
