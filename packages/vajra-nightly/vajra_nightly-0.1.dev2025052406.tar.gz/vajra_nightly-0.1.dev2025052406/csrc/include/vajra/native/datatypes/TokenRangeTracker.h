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
enum class TokenRangeState : int {
  Unavailable,  // Tokens not available for processing (no token ids available)
  Unprocessed,  // Tokens available but not processed
  StageProcessed,  // Tokens processed by this stage in the pipeline (when using
                   // Pipeline Parallelism)
  Processed

  /* State Transitions:
   * - Unprocessed -> StageProcessed (processed by this stage in the pipeline)
   * - StageProcessed -> Processed   (fully processed)
   * - Unprocessed -> Processed      (fully processed)
   * - Processed -> Unprocessed      (evicted)
   */
};
//==============================================================================
inline std::string TokenRangeStateToString(TokenRangeState state) {
  switch (state) {
    case TokenRangeState::Unavailable:
      return "Unavailable";
    case TokenRangeState::Unprocessed:
      return "Unprocessed";
    case TokenRangeState::StageProcessed:
      return "StageProcessed";
    case TokenRangeState::Processed:
      return "Processed";
    default:
      return "Unknown";
  }
}
//==============================================================================
struct TokenRange {
  std::size_t start;
  std::size_t end;  // exclusive
  TokenRangeState state;

  bool operator<(const TokenRange& other) const {
    // we should never have overlapping ranges
    return start < other.start;
  }

  [[nodiscard]] std::string ToString() const {
    return std::format("TokenRange(start={}, end={}, state={})", start, end,
                       TokenRangeStateToString(state));
  }
};
//==============================================================================
class TokenRangeTracker {
 public:
  TokenRangeTracker(
      /*[in]*/ const std::size_t length,
      /*[in]*/ const TokenRangeState initial_state =
          TokenRangeState::Unprocessed);

  void UpdateRange(
      /*[in]*/ const std::size_t start,
      /*[in]*/ const std::size_t end,
      /*[in]*/ const TokenRangeState state);

  void AppendRange(
      /*[in]*/ const std::size_t length,
      /*[in]*/ const TokenRangeState state);

  void Reset();

  [[nodiscard]] TokenRange GetNextUnprocessedRange() const;
  [[nodiscard]] std::size_t GetProcessedPrefixLength() const;
  [[nodiscard]] std::size_t GetStageProcessedPrefixLength() const;
  [[nodiscard]] std::size_t GetLength() const;
  [[nodiscard]] const std::set<TokenRange>& GetTokenRanges() const;

  [[nodiscard]] std::string ToString() const;

 private:
  static void CheckStateTransition(
      /*[in]*/ const TokenRange& range,
      /*[in]*/ const TokenRangeState new_state);

  void InsertRange(
      /*[in]*/ const std::size_t start,
      /*[in]*/ const std::size_t end,
      /*[in]*/ const TokenRangeState state,
      /*[in]*/ const bool merge_adjacent);

  std::set<TokenRange> token_ranges_;
};
//==============================================================================
}  // namespace vajra
//==============================================================================
