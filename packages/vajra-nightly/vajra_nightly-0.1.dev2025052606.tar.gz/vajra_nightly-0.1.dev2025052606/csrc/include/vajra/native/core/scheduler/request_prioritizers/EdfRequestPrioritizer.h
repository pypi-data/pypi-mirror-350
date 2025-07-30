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
#include "native/configs/ParallelConfig.h"
#include "native/configs/ReplicaSchedulerConfig.h"
#include "native/configs/RequestPrioritizerConfig.h"
#include "native/core/scheduler/request_prioritizers/BaseRequestPrioritizer.h"
#include "native/core/scheduler/utils/PrefillTimeCalculator.h"
#include "native/datatypes/BaseSequenceWithPriority.h"
//==============================================================================
namespace vajra {
//==============================================================================
using ExecutionTimePredictor =
    vidur::execution_time_predictor::ExecutionTimePredictor;
//==============================================================================
class SequenceWithEdfPriority : public BaseSequenceWithPriority {
 public:
  SequenceWithEdfPriority(MutableSequencePtr seq, float deadline)
      : BaseSequenceWithPriority(seq), deadline_(deadline) {}

  [[nodiscard]] float GetPriority() const override { return deadline_; }

 private:
  const float deadline_;
};
//==============================================================================
class EdfRequestPrioritizer : public BaseRequestPrioritizer {
 public:
  EdfRequestPrioritizer(
      const EdfRequestPrioritizerConfig& config,
      const ParallelConfig& parallel_config,
      const std::shared_ptr<BaseReplicaSchedulerConfig>&
          replica_scheduler_config,
      const std::shared_ptr<ExecutionTimePredictor>& execution_time_predictor)
      : config_(config),
        prefill_time_calculator_(std::make_shared<PrefillTimeCalculator>(
            execution_time_predictor, parallel_config.pipeline_parallel_size,
            parallel_config.kv_parallel_size,
            parallel_config.max_num_tokens_per_kvp_group,
            replica_scheduler_config->GetTargetBatchTime(),
            replica_scheduler_config->GetMaxChunkSize(),
            replica_scheduler_config->GetMinChunkSize(),
            parallel_config.enable_sequence_pipeline_parallel)) {
    ASSERT_VALID_POINTER_ARGUMENT(execution_time_predictor);
    ASSERT_VALID_POINTER_ARGUMENT(replica_scheduler_config);
  }

  [[nodiscard]] MutableBaseSequenceWithPriorityPtr GetSeqWithPriority(
      MutableSequencePtr seq) override {
    auto prefill_time =
        prefill_time_calculator_->GetPrefillTime(seq->GetPromptLength());
    double deadline_time = std::max(prefill_time * config_.deadline_multiplier,
                                    config_.min_deadline);
    double deadline = deadline_time + seq->arrival_time;

    return std::make_shared<SequenceWithEdfPriority>(
        seq, static_cast<float>(deadline));
  }

 protected:
  const EdfRequestPrioritizerConfig config_;
  const std::shared_ptr<PrefillTimeCalculator> prefill_time_calculator_;
};
//==============================================================================
}  // namespace vajra
//==============================================================================
