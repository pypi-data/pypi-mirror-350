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
#include "native/datatypes/TokenRangeTracker.h"

using vajra::TokenRange;
using vajra::TokenRangeState;
using vajra::TokenRangeTracker;

TokenRangeTracker::TokenRangeTracker(
    /*[in]*/ const std::size_t length,
    /*[in]*/ const TokenRangeState initial_state) {
  if (length > 0) AppendRange(length, initial_state);
}

void TokenRangeTracker::UpdateRange(
    /*[in]*/ const std::size_t range_start,
    /*[in]*/ const std::size_t range_end,
    /*[in]*/ const TokenRangeState range_state) {
  auto seq_length = GetLength();
  ASSERT_VALID_ARGUMENTS(
      (range_start < seq_length) && (range_end <= seq_length),
      "range_start={}, range_end={}, seq_length={}", range_start, range_end,
      seq_length);

  // Find the first range whose start position is >= range_start
  // Note: We maintain the invariant that all ranges are non-overlapping
  auto range_itr =
      std::lower_bound(token_ranges_.begin(), token_ranges_.end(), range_start,
                       [](const TokenRange& range, std::size_t other_start) {
                         return range.start < other_start;
                       });

  // adjust to include overlapping ranges
  // this ensures it->start <= range_start
  if (range_itr == token_ranges_.end() || range_itr->start > range_start) {
    range_itr--;
  }

  // process existing ranges and remove the interval [range_start, range_end)
  while (range_itr != token_ranges_.end() && range_itr->start < range_end) {
    auto existing_range = *range_itr;
    token_ranges_.erase(range_itr++);

    // Handle the portion of the existing range that comes before our target
    // range
    if (existing_range.start < range_start) {
      // Preserve the unmodified segment [existingRange.start, rangeStart)
      InsertRange(existing_range.start, range_start, existing_range.state,
                  /*merge_adjacent=*/false);
    }
    // Handle the portion of the existing range that extends beyond our target
    // range
    if (existing_range.end > range_end) {
      // Preserve the unmodified segment [rangeEnd, existingRange.end)
      InsertRange(range_end, existing_range.end, existing_range.state,
                  /*merge_adjacent=*/false);
    }

    // this is the intersection with the existing range
    auto intersection =
        TokenRange{.start = std::max(existing_range.start, range_start),
                   .end = std::min(existing_range.end, range_end),
                   .state = existing_range.state};
    // check if this state transition is allowed
    CheckStateTransition(intersection, range_state);
  }

  // finally, add [range_start, range_end)
  InsertRange(range_start, range_end, range_state, /*merge_adjacent=*/true);
}

void TokenRangeTracker::InsertRange(/*[in]*/ const std::size_t range_start,
                                    /*[in]*/ const std::size_t range_end,
                                    /*[in]*/ const TokenRangeState range_state,
                                    /*[in]*/ const bool merge_adjacent) {
  ASSERT_VALID_RUNTIME(range_start < range_end,
                       "range_start={} must be less than range_end={}",
                       range_start, range_end);

  auto [range_itr, inserted] = token_ranges_.emplace(
      TokenRange{.start = range_start, .end = range_end, .state = range_state});
  ASSERT_VALID_RUNTIME(inserted, "Range with same start already exists");

  if (!merge_adjacent) {
    return;
  }

  // Try to merge with next range
  auto next_itr = std::next(range_itr);
  if (next_itr != token_ranges_.end()) {
    ASSERT_VALID_RUNTIME(range_itr->end == next_itr->start,
                         "Ranges are not adjacent");

    // should have the same state
    if (range_itr->state == next_itr->state) {
      TokenRange merged_range{.start = range_itr->start,
                              .end = next_itr->end,
                              .state = range_itr->state};

      // erase existing ranges
      token_ranges_.erase(next_itr);
      token_ranges_.erase(range_itr);

      // add merged range
      auto [new_itr, success] = token_ranges_.insert(merged_range);
      ASSERT_VALID_RUNTIME(success, "Failed to insert merged range");
      range_itr = new_itr;
    }
  }

  // Try to merge with previous range
  if (range_itr != token_ranges_.begin()) {
    auto prev_itr = std::prev(range_itr);
    ASSERT_VALID_RUNTIME(prev_itr->end == range_itr->start,
                         "Ranges are not adjacent");

    if (prev_itr->state == range_itr->state) {
      TokenRange merged_range{.start = prev_itr->start,
                              .end = range_itr->end,
                              .state = prev_itr->state};

      token_ranges_.erase(range_itr);
      token_ranges_.erase(prev_itr);

      auto [new_itr, success] = token_ranges_.insert(merged_range);
      ASSERT_VALID_RUNTIME(success, "Failed to insert merged range");
    }
  }
}

void TokenRangeTracker::AppendRange(/*[in]*/ const std::size_t length,
                                    /*[in]*/ const TokenRangeState state) {
  auto seq_length = GetLength();
  InsertRange(seq_length, seq_length + length, state, /*merge_adjacent=*/true);
}

[[nodiscard]] TokenRange TokenRangeTracker::GetNextUnprocessedRange() const {
  for (const auto& range : token_ranges_) {
    if (range.state == TokenRangeState::Unprocessed) {
      return range;
    }
  }
  return TokenRange{
      .start = 0, .end = 0, .state = TokenRangeState::Unavailable};
}

[[nodiscard]] std::size_t TokenRangeTracker::GetStageProcessedPrefixLength()
    const {
  std::size_t processed = 0;
  for (const auto& range : token_ranges_) {
    if (range.state == TokenRangeState::Processed ||
        range.state == TokenRangeState::StageProcessed) {
      processed = std::max(processed, range.end);
    }
  }
  return processed;
}

[[nodiscard]] std::size_t TokenRangeTracker::GetProcessedPrefixLength() const {
  std::size_t processed = 0;
  for (const auto& range : token_ranges_) {
    if (range.state == TokenRangeState::Processed) {
      processed = std::max(processed, range.end);
    }
  }
  return processed;
}

[[nodiscard]] const std::set<TokenRange>& TokenRangeTracker::GetTokenRanges()
    const {
  return token_ranges_;
}

[[nodiscard]] std::size_t TokenRangeTracker::GetLength() const {
  if (token_ranges_.empty()) {
    return 0;
  }
  return token_ranges_.rbegin()->end;
}

[[nodiscard]] std::string TokenRangeTracker::ToString() const {
  std::vector<std::string> range_strs;
  for (const auto& range : token_ranges_) {
    range_strs.push_back(range.ToString());
  }

  return std::format("TokenRangeTracker(length={}, token_ranges={})",
                     GetLength(), JoinStrings(range_strs, ", "));
}

void TokenRangeTracker::CheckStateTransition(
    /*[in]*/ const TokenRange& range,
    /*[in]*/ const TokenRangeState new_state) {
  const auto old_state = range.state;
  if (old_state == new_state) {
    return;
  }

  if (old_state == TokenRangeState::StageProcessed) {
    switch (new_state) {
      case TokenRangeState::Processed:  // pipeline parallelism
        break;
      default:
        THROW_RUNTIME_ERROR("Invalid state transition for range {} to {}",
                            range.ToString(),
                            TokenRangeStateToString(new_state));
    }
  }
  if (old_state == TokenRangeState::Processed) {
    switch (new_state) {
      case TokenRangeState::Unprocessed:  // evicted
        break;
      default:
        THROW_RUNTIME_ERROR("Invalid state transition for range {} to {}",
                            range.ToString(),
                            TokenRangeStateToString(new_state));
    }
  }
  if (old_state == TokenRangeState::Unprocessed) {
    switch (new_state) {
      case TokenRangeState::Unavailable:
        THROW_RUNTIME_ERROR("Invalid state transition for range {} to {}",
                            range.ToString(),
                            TokenRangeStateToString(new_state));
      default:
        break;
    }
  }
}

void TokenRangeTracker::Reset() { token_ranges_.clear(); }
