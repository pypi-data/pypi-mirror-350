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
#include "commons/Logging.h"
#include "commons/StdCommon.h"
#include "commons/Time.h"
#include "native/datatypes/SequenceStatus.h"
//==============================================================================
namespace vajra {
//==============================================================================
class SequenceState {
 public:
  SequenceState(const std::string id_param /*[in]*/,
                double arrived_at_param /*[in]*/,
                std::size_t num_prompt_tokens_param /*[in]*/)
      : id_(id_param),
        arrived_at_(arrived_at_param),
        num_prompt_tokens_(num_prompt_tokens_param),
        num_output_tokens_(0),
        status_(SequenceStatus::Waiting),
        is_scheduled_(false),
        is_completed_(false),
        scheduled_at_(std::nullopt),
        completed_at_(std::nullopt),
        prompt_processing_completed_at_(std::nullopt),
        last_restart_at_(std::nullopt),
        last_pause_at_(std::nullopt),
        execution_time_(0.0),
        preempted_time_(0.0),
        last_execution_start_at_(std::nullopt),
        num_restarts_(0),
        num_pauses_(0),
        is_ignore_finished_(false),
        last_token_generated_at_(std::nullopt),
        last_token_generation_time_(0.0) {}

  [[nodiscard]] inline std::string GetId() const { return id_; }

  [[nodiscard]] inline std::size_t GetNumPromptTokens() const {
    return num_prompt_tokens_;
  }

  [[nodiscard]] inline std::size_t GetNumOutputTokens() const {
    return num_output_tokens_;
  }

  [[nodiscard]] inline std::size_t GetNumTotalTokens() const {
    return num_prompt_tokens_ + num_output_tokens_;
  }

  [[nodiscard]] inline SequenceStatus GetStatus() const { return status_; }

  [[nodiscard]] inline bool GetIsScheduled() const { return is_scheduled_; }

  [[nodiscard]] inline bool GetIsCompleted() const { return is_completed_; }

  [[nodiscard]] inline double GetArrivedAt() const { return arrived_at_; }

  inline double GetScheduledAt() const {
    ASSERT_VALID_RUNTIME(scheduled_at_.has_value(),
                         "Sequence not yet scheduled");
    return scheduled_at_.value();
  }

  inline double GetCompletedAt() const {
    ASSERT_VALID_RUNTIME(completed_at_.has_value(),
                         "Sequence not yet completed");
    return completed_at_.value();
  }

  inline double GetPromptProcessingCompletedAt() const {
    ASSERT_VALID_RUNTIME(prompt_processing_completed_at_.has_value(),
                         "Prompt processing not yet completed");
    return prompt_processing_completed_at_.value();
  }

  inline double GetE2ETime() const { return GetCompletedAt() - GetArrivedAt(); }

  inline double GetE2ETimePiecewiseNormalized() const {
    return GetSchedulingDelay() +
           (GetExecutionPlusPreemptionTime() / GetNumOutputTokens());
  }

  inline double GetE2ETimeNormalized() const {
    return GetE2ETime() / GetNumOutputTokens();
  }

  inline double GetE2EPrefillTime() const {
    return GetPromptProcessingCompletedAt() - GetArrivedAt();
  }

  inline double GetE2EPrefillTimeNormalized() const {
    ASSERT_VALID_RUNTIME(GetNumPromptTokens() > 0,
                         "No prompt tokens available");
    return GetE2EPrefillTime() / GetNumPromptTokens();
  }

  inline double GetE2EPrefillTimePiecewiseNormalized() const {
    ASSERT_VALID_RUNTIME(GetNumPromptTokens() > 0,
                         "No prompt tokens in the sequence");
    return GetSchedulingDelay() +
           (GetPrefillExecutionPlusPreemptionTime() / GetNumPromptTokens());
  }

  inline double GetPrefillExecutionPlusPreemptionTime() const {
    return GetPromptProcessingCompletedAt() - GetScheduledAt();
  }

  inline double GetDecodeExecutionPlusPreemptionTime() const {
    return GetCompletedAt() - GetPromptProcessingCompletedAt();
  }

  inline double GetPrefillExecutionPlusPreemptionTimeNormalized() const {
    ASSERT_VALID_RUNTIME(GetNumPromptTokens() > 0,
                         "No prompt tokens in the sequence");
    return GetPrefillExecutionPlusPreemptionTime() / GetNumPromptTokens();
  }

  inline double GetDecodeExecutionPlusPreemptionTimeNormalized() const {
    return GetDecodeExecutionPlusPreemptionTime() / GetNumOutputTokens();
  }

  inline double GetSchedulingDelay() const {
    return GetScheduledAt() - GetArrivedAt();
  }

  inline double GetExecutionTime() const { return execution_time_; }

  inline double GetExecutionTimeNormalized() const {
    return GetExecutionTime() / GetNumOutputTokens();
  }

  inline double GetPreemptedTime() const { return preempted_time_; }

  inline double GetExecutionPlusPreemptionTime() const {
    return GetExecutionTime() + GetPreemptedTime();
  }

  inline double GetExecutionPlusPreemptionTimeNormalized() const {
    return GetExecutionPlusPreemptionTime() / GetNumOutputTokens();
  }

  inline double GetLastTokenGenerationTime() const {
    return last_token_generation_time_;
  }

  inline std::size_t GetNumRestarts() const { return num_restarts_; }

  inline std::size_t GetNumPauses() const { return num_pauses_; }

  inline bool GetIsIgnoreFinished() const { return is_ignore_finished_; }

  void SetStatus(SequenceStatus status /*[in]*/);

  inline void OnPromptProcessingCompleted() {
    prompt_processing_completed_at_ = time_utils::now_s();
  }

  void OnTokenGenerated();

  /// @brief Convert to string representation
  /// @return String representation of the SequenceState
  [[nodiscard]] std::string ToString() const {
    return std::format(
        "SequenceState(id={}, status={}, num_prompt_tokens={}, "
        "num_output_tokens={}, is_scheduled={}, is_completed={}, "
        "execution_time={:.3f}s, preempted_time={:.3f}s, num_restarts={}, "
        "num_pauses={})",
        id_, status_, num_prompt_tokens_, num_output_tokens_, is_scheduled_,
        is_completed_, execution_time_, preempted_time_, num_restarts_,
        num_pauses_);
  }

 private:
  void HandleTransitionsFromWaitingStatus(double current_time /*[in]*/,
                                          SequenceStatus status /*[in]*/);
  void HandleTransitionsFromRunningStatus(double current_time /*[in]*/,
                                          SequenceStatus status /*[in]*/);

  void HandleTransitionsFromPausedState(double current_time /*[in]*/,
                                        SequenceStatus status /*[in]*/);

  std::string id_;
  double arrived_at_;
  std::size_t num_prompt_tokens_;
  std::size_t num_output_tokens_;
  SequenceStatus status_;
  bool is_scheduled_;
  bool is_completed_;
  std::optional<double> scheduled_at_;
  std::optional<double> completed_at_;
  std::optional<double> prompt_processing_completed_at_;
  std::optional<double> last_restart_at_;
  std::optional<double> last_pause_at_;
  double execution_time_;
  double preempted_time_;
  std::optional<double> last_execution_start_at_;
  std::size_t num_restarts_;
  std::size_t num_pauses_;
  bool is_ignore_finished_;
  std::optional<double> last_token_generated_at_;
  double last_token_generation_time_;
};
//==============================================================================
}  // namespace vajra
//==============================================================================
