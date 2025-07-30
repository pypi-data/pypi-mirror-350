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
//==============================================================================
namespace vajra {
//==============================================================================
enum class SequenceStatus {
  Waiting,
  WaitingPreempted,
  Running,
  Paused,
  FinishedStopped,
  FinishedLengthCapped,
  FinishedIgnored
};
//==============================================================================
namespace sequence_status {
//==============================================================================
inline bool IsFinished(SequenceStatus status) {
  return status == SequenceStatus::FinishedStopped ||
         status == SequenceStatus::FinishedLengthCapped ||
         status == SequenceStatus::FinishedIgnored;
}

inline bool IsExecuting(SequenceStatus status) {
  return status == SequenceStatus::Running || status == SequenceStatus::Paused;
}

inline bool IsWaiting(SequenceStatus status) {
  return status == SequenceStatus::Waiting;
}

inline bool IsWaitingPreempted(SequenceStatus status) {
  return status == SequenceStatus::WaitingPreempted;
}

inline bool IsPaused(SequenceStatus status) {
  return status == SequenceStatus::Paused;
}

inline bool IsRunning(SequenceStatus status) {
  return status == SequenceStatus::Running;
}

inline std::optional<std::string> GetFinishedReason(SequenceStatus status) {
  switch (status) {
    case SequenceStatus::FinishedStopped:
      return "stop";
    case SequenceStatus::FinishedLengthCapped:
    case SequenceStatus::FinishedIgnored:
      return "length";
    default:
      return std::nullopt;
  }
}
//==============================================================================
}  // namespace sequence_status
//==============================================================================
}  // namespace vajra
//==============================================================================
// Must be outside the vajra namespaceto ensure the std::formatter can access
// the template specialization
template <>
struct std::formatter<vajra::SequenceStatus>
    : std::formatter<std::string_view> {
  constexpr auto parse(std::format_parse_context& ctx) {
    // Just use the parse from the base class
    return std::formatter<std::string_view>::parse(ctx);
  }

  template <typename FormatContext>
  auto format(vajra::SequenceStatus c, FormatContext& ctx) const {
    std::string_view name = "unknown";
    switch (c) {
      case vajra::SequenceStatus::Waiting:
        name = "waiting";
        break;
      case vajra::SequenceStatus::WaitingPreempted:
        name = "waiting_preempted";
        break;
      case vajra::SequenceStatus::Running:
        name = "running";
        break;
      case vajra::SequenceStatus::Paused:
        name = "paused";
        break;
      case vajra::SequenceStatus::FinishedStopped:
        name = "finished_stopped";
        break;
      case vajra::SequenceStatus::FinishedLengthCapped:
        name = "finished_length_stopped";
        break;
      case vajra::SequenceStatus::FinishedIgnored:
        name = "finished_ignored";
        break;
    }
    return std::formatter<std::string_view>::format(name, ctx);
  }
};
//==============================================================================
