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
#include "native/datatypes/SequenceState.h"

using vajra::SequenceState;
using vajra::SequenceStatus;

void SequenceState::SetStatus(SequenceStatus status /*[in]*/) {
  double current_time = time_utils::now_s();

  switch (status_) {
    case SequenceStatus::Waiting:
    case SequenceStatus::WaitingPreempted:
      HandleTransitionsFromWaitingStatus(current_time, status);
      break;
    case SequenceStatus::Running:
      HandleTransitionsFromRunningStatus(current_time, status);
      break;
    case SequenceStatus::Paused:
      HandleTransitionsFromPausedState(current_time, status);
      break;
    default:
      ASSERT_VALID_RUNTIME(
          false, "Invalid state transition from {} to {} for request {}",
          status_, status, id_);
      break;
  }

  status_ = status;
}

void SequenceState::OnTokenGenerated() {
  double current_time = time_utils::now_s();
  num_output_tokens_ += 1;
  if (last_token_generated_at_.has_value()) {
    last_token_generation_time_ =
        current_time - last_token_generated_at_.value();
  } else {
    last_token_generation_time_ = 0.0;
  }
  last_token_generated_at_ = current_time;
}

void SequenceState::HandleTransitionsFromWaitingStatus(
    double current_time /*[in]*/, SequenceStatus status /*[in]*/) {
  switch (status) {
    case SequenceStatus::Running:
      // request is starting execution now
      if (scheduled_at_.has_value()) {
        ASSERT_VALID_RUNTIME(num_restarts_ > 0,
                             "num_restarts must be greater than zero. Got {}",
                             num_restarts_);
        ASSERT_VALID_RUNTIME(last_restart_at_.has_value(),
                             "last_restart_at must be set");
        preempted_time_ += current_time - last_restart_at_.value();
      } else {
        // restarting
        ASSERT_VALID_RUNTIME(num_restarts_ == 0,
                             "num_restarts must be zero. Got {}",
                             num_restarts_);
        is_scheduled_ = true;
        scheduled_at_ = current_time;
      }
      last_execution_start_at_ = current_time;
      break;
    case SequenceStatus::FinishedIgnored:
      is_ignore_finished_ = true;
      is_completed_ = true;
      completed_at_ = current_time;
      // The scheduler will not schedule this request again
      scheduled_at_ = current_time;
      break;
    default:
      ASSERT_VALID_RUNTIME(
          false, "Invalid state transition from {} to {} for request {}",
          status_, status, id_);
  }
}

void SequenceState::HandleTransitionsFromRunningStatus(
    double current_time /*[in]*/, SequenceStatus status /*[in]*/) {
  ASSERT_VALID_RUNTIME(
      last_execution_start_at_.has_value(),
      "Invalid state transition: last_execution_start_at_ not set");
  execution_time_ += current_time - last_execution_start_at_.value();

  switch (status) {
    case SequenceStatus::Paused:
      num_pauses_ += 1;
      last_pause_at_ = current_time;
      break;
    case SequenceStatus::WaitingPreempted:
      num_restarts_ += 1;
      last_restart_at_ = current_time;
      break;
    default:
      ASSERT_VALID_RUNTIME(
          false, "Invalid state transition from {} to {} for request {}",
          status_, status, id_);
  }
}

void SequenceState::HandleTransitionsFromPausedState(
    double current_time /*[in]*/, SequenceStatus status /*[in]*/) {
  ASSERT_VALID_RUNTIME(last_pause_at_.has_value(),
                       "Invalid state transition: last_pause_at_ not set");
  preempted_time_ += current_time - last_pause_at_.value();

  switch (status) {
    case SequenceStatus::FinishedStopped:
    case SequenceStatus::FinishedLengthCapped:
      is_completed_ = true;
      completed_at_ = current_time;
      break;
    case SequenceStatus::Running:
      last_execution_start_at_ = current_time;
      break;
    case SequenceStatus::WaitingPreempted:
      num_restarts_ += 1;
      last_restart_at_ = current_time;
      break;
    default:
      ASSERT_VALID_RUNTIME(
          false, "Invalid state transition from {} to {} for request {}",
          status_, status, id_);
  }
}
