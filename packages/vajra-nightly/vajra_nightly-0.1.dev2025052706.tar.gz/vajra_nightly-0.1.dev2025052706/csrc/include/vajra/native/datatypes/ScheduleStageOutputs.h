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
#include "native/datatypes/SchedulerOutput.h"
#include "native/datatypes/Sequence.h"
//==============================================================================
namespace vajra {
//==============================================================================
struct ScheduleStageOutputs final {
  ScheduleStageOutputs(const MutableSequences& ignored_seqs_param,
                       const MutableSequences& seqs_param,
                       const SchedulerOutputPtr& scheduler_output_param,
                       const double start_time_param)
      : ignored_seqs(ignored_seqs_param),
        seqs(seqs_param),
        scheduler_output(scheduler_output_param),
        start_time(start_time_param) {
    ASSERT_VALID_POINTER_ARGUMENT(scheduler_output);
  }

  /// @brief Convert to string representation
  /// @return String representation of the ScheduleStageOutputs
  [[nodiscard]] std::string ToString() const {
    return std::format(
        "ScheduleStageOutputs(ignored_seqs_count={}, seqs_count={}, "
        "scheduler_output={}, start_time={})",
        ignored_seqs.size(), seqs.size(), scheduler_output, start_time);
  }

  MutableSequences ignored_seqs;
  MutableSequences seqs;
  SchedulerOutputPtr scheduler_output;
  double start_time;
};
//==============================================================================
typedef std::shared_ptr<ScheduleStageOutputs> ScheduleStageOutputsPtr;
//==============================================================================
}  // namespace vajra
//==============================================================================
