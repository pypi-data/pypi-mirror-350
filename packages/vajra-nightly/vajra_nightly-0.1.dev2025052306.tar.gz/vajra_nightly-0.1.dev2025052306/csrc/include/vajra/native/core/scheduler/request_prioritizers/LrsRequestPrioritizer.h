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
// clang-format off
// Include vidur headers
#include "vidur/entities/batch.h"
#include "vidur/execution_time_predictor/execution_time_predictor.h"
// clang-format on
//==============================================================================
#include "commons/Time.h"
#include "native/core/scheduler/request_prioritizers/EdfRequestPrioritizer.h"
#include "native/core/scheduler/utils/PrefillTimeCalculator.h"
#include "native/datatypes/BaseSequenceWithPriority.h"
//==============================================================================
namespace vajra {
//==============================================================================
class SequenceWithLrsPriority : public BaseSequenceWithPriority {
 public:
  SequenceWithLrsPriority(MutableSequencePtr seq, float deadline_time,
                          const std::shared_ptr<const PrefillTimeCalculator>&
                              prefetch_time_calculator)
      : BaseSequenceWithPriority(seq),
        deadline_time_(deadline_time),
        prefill_time_calculator_(prefetch_time_calculator) {
    ASSERT_VALID_POINTER_ARGUMENT(seq);
    ASSERT_VALID_POINTER_ARGUMENT(prefetch_time_calculator);
  }

  [[nodiscard]] float GetPriority() const override {
    auto seq = GetSequence();
    auto remaining_prefill_time = prefill_time_calculator_->GetPrefillTime(
        GetSequence()->GetPromptLength(),
        GetSequence()->GetNumPromptTokensStageProcessed());
    auto slack = GetSequence()->arrival_time + deadline_time_ -
                 time_utils::now_s() - remaining_prefill_time;
    return slack / deadline_time_;
  }

 private:
  const float deadline_time_;
  const std::shared_ptr<const PrefillTimeCalculator> prefill_time_calculator_;
};
//==============================================================================
class LrsRequestPrioritizer : public EdfRequestPrioritizer {
 public:
  LrsRequestPrioritizer(
      const LrsRequestPrioritizerConfig& config,
      const ParallelConfig& parallel_config,
      const std::shared_ptr<BaseReplicaSchedulerConfig>&
          replica_scheduler_config,
      const std::shared_ptr<ExecutionTimePredictor>& execution_time_predictor)
      : EdfRequestPrioritizer(config, parallel_config, replica_scheduler_config,
                              execution_time_predictor) {
    ASSERT_VALID_POINTER_ARGUMENT(execution_time_predictor);
    ASSERT_VALID_POINTER_ARGUMENT(replica_scheduler_config);
  }

  [[nodiscard]] MutableBaseSequenceWithPriorityPtr GetSeqWithPriority(
      MutableSequencePtr seq) override {
    ASSERT_VALID_POINTER_ARGUMENT(seq);
    auto prefill_time =
        prefill_time_calculator_->GetPrefillTime(seq->GetPromptLength());

    double deadline_time = std::max(prefill_time * config_.deadline_multiplier,
                                    config_.min_deadline);
    return std::make_shared<SequenceWithLrsPriority>(
        seq, static_cast<float>(deadline_time), prefill_time_calculator_);
  }
};
//==============================================================================
}  // namespace vajra
//==============================================================================
