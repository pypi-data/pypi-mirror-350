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

#include <gtest/gtest.h>

using vajra::TokenRange;
using vajra::TokenRangeState;
using vajra::TokenRangeTracker;

TEST(TokenRangeTracker, Basic) {
  TokenRangeTracker tracker(10, TokenRangeState::Unprocessed);

  auto range = tracker.GetNextUnprocessedRange();
  EXPECT_EQ(range.start, 0);
  EXPECT_EQ(range.end, 10);

  tracker.UpdateRange(0, 5, TokenRangeState::Processed);

  range = tracker.GetNextUnprocessedRange();
  EXPECT_EQ(range.start, 5) << tracker.ToString();
  EXPECT_EQ(range.end, 10);

  tracker.UpdateRange(3, 8, TokenRangeState::Processed);

  range = tracker.GetNextUnprocessedRange();
  EXPECT_EQ(range.start, 8);
  EXPECT_EQ(range.end, 10);
}

TEST(TokenRangeTracker, AppendRange) {
  TokenRangeTracker tracker(10, TokenRangeState::Processed);
  tracker.AppendRange(5, TokenRangeState::Unprocessed);

  auto range = tracker.GetNextUnprocessedRange();
  EXPECT_EQ(range.start, 10);
  EXPECT_EQ(range.end, 15);
}

TEST(TokenRangeTracker, UpdateRangeComplete) {
  TokenRangeTracker tracker(10, TokenRangeState::Unprocessed);
  tracker.UpdateRange(0, 10, TokenRangeState::Processed);

  EXPECT_EQ(tracker.GetLength(), 10);

  auto ranges = tracker.GetTokenRanges();
  EXPECT_EQ(ranges.size(), 1) << tracker.ToString();
  EXPECT_EQ(ranges.begin()->start, 0);
  EXPECT_EQ(ranges.begin()->end, 10);
  EXPECT_EQ(ranges.begin()->state, TokenRangeState::Processed);
}

TEST(TokenRangeTracker, UpdateRangePartial) {
  TokenRangeTracker tracker(10, TokenRangeState::Unprocessed);
  tracker.UpdateRange(2, 5, TokenRangeState::Processed);

  EXPECT_EQ(tracker.GetLength(), 10);

  auto ranges = tracker.GetTokenRanges();
  EXPECT_EQ(ranges.size(), 3) << tracker.ToString();

  auto it = ranges.begin();
  EXPECT_EQ(it->start, 0);
  EXPECT_EQ(it->end, 2);
  EXPECT_EQ(it->state, TokenRangeState::Unprocessed);

  it++;
  EXPECT_EQ(it->start, 2);
  EXPECT_EQ(it->end, 5);
  EXPECT_EQ(it->state, TokenRangeState::Processed);

  it++;
  EXPECT_EQ(it->start, 5);
  EXPECT_EQ(it->end, 10);
  EXPECT_EQ(it->state, TokenRangeState::Unprocessed);
}

TEST(TokenRangeTracker, UpdateRangeOverlappingMultiple) {
  TokenRangeTracker tracker(0, TokenRangeState::Unprocessed);
  tracker.AppendRange(5, TokenRangeState::Unprocessed);
  tracker.AppendRange(5, TokenRangeState::Processed);
  tracker.AppendRange(5, TokenRangeState::Unavailable);

  EXPECT_EQ(tracker.GetLength(), 15);

  // Now we have [0-5:Unprocessed][5-10:Processed][10-15:Unavailable]
  // Update to make [3-12:Processed]
  tracker.UpdateRange(3, 12, TokenRangeState::Processed);

  auto ranges = tracker.GetTokenRanges();
  EXPECT_EQ(ranges.size(), 3) << tracker.ToString();

  auto it = ranges.begin();
  EXPECT_EQ(it->start, 0);
  EXPECT_EQ(it->end, 3);
  EXPECT_EQ(it->state, TokenRangeState::Unprocessed);

  it++;
  EXPECT_EQ(it->start, 3);
  EXPECT_EQ(it->end, 12);
  EXPECT_EQ(it->state, TokenRangeState::Processed);

  it++;
  EXPECT_EQ(it->start, 12);
  EXPECT_EQ(it->end, 15);
  EXPECT_EQ(it->state, TokenRangeState::Unavailable);
}

TEST(TokenRangeTracker, EmptyTracker) {
  TokenRangeTracker tracker(0, TokenRangeState::Unprocessed);
  EXPECT_EQ(tracker.GetLength(), 0);

  auto range = tracker.GetNextUnprocessedRange();
  EXPECT_EQ(range.start, 0);
  EXPECT_EQ(range.end, 0);
  EXPECT_EQ(range.state, TokenRangeState::Unavailable);
}

TEST(TokenRangeTracker, UpdateEdgeCases) {
  TokenRangeTracker tracker(10, TokenRangeState::Unprocessed);

  // Update at the start
  tracker.UpdateRange(0, 3, TokenRangeState::Processed);
  EXPECT_EQ(tracker.GetTokenRanges().size(), 2);

  // Update at the end
  tracker.UpdateRange(7, 10, TokenRangeState::Processed);
  EXPECT_EQ(tracker.GetTokenRanges().size(), 3);

  // Update exactly matching an existing range
  tracker.UpdateRange(3, 7, TokenRangeState::Processed);

  // Should now have one continuous processed range
  auto ranges = tracker.GetTokenRanges();
  EXPECT_EQ(ranges.size(), 1) << tracker.ToString();
  EXPECT_EQ(ranges.begin()->start, 0);
  EXPECT_EQ(ranges.begin()->end, 10);
  EXPECT_EQ(ranges.begin()->state, TokenRangeState::Processed);
}

TEST(TokenRangeTracker, ComplexSequence) {
  TokenRangeTracker tracker(20, TokenRangeState::Unprocessed);

  // Create a complex mix of states
  tracker.UpdateRange(0, 5, TokenRangeState::StageProcessed);
  tracker.UpdateRange(10, 15, TokenRangeState::StageProcessed);
  tracker.UpdateRange(7, 12, TokenRangeState::Processed);

  auto ranges = tracker.GetTokenRanges();
  EXPECT_EQ(ranges.size(), 5) << tracker.ToString();

  // Find and process the next unprocessed range
  auto unprocessed = tracker.GetNextUnprocessedRange();
  EXPECT_EQ(unprocessed.start, 5);
  EXPECT_EQ(unprocessed.end, 7);

  // Mark it as processed
  tracker.UpdateRange(unprocessed.start, unprocessed.end,
                      TokenRangeState::Processed);

  // Next unprocessed should be the one after the unavailable section
  unprocessed = tracker.GetNextUnprocessedRange();
  EXPECT_EQ(unprocessed.start, 15);
  EXPECT_EQ(unprocessed.end, 20);
}
