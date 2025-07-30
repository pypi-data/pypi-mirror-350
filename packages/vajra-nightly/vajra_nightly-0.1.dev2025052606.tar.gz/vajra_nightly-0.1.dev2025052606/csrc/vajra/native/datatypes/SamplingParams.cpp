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
#include "native/datatypes/SamplingParams.h"

using vajra::SamplingParams;

void SamplingParams::VerifyArgs() const {
  ASSERT_VALID_ARGUMENTS(temperature >= 0.0,
                         "temperature must be non-negative, got {}.",
                         temperature);
  ASSERT_VALID_ARGUMENTS(top_p > 0.0 && top_p <= 1.0,
                         "top_p must be in (0, 1], got {} {}.", top_p,
                         temperature);
  ASSERT_VALID_ARGUMENTS(!(top_k < -1 || top_k == 0),
                         "top_k must be -1 (disable) or at least 1, got {}.",
                         top_k);
  ASSERT_VALID_ARGUMENTS(max_tokens >= 1,
                         "max_tokens must be at least 1, got {}.", max_tokens);
}

void SamplingParams::VerifyGreedySampling() const {
  ASSERT_VALID_ARGUMENTS(!(top_p < 1.0 - SAMPLING_EPS),
                         "top_p must be 1 when using greedy sampling.");
  ASSERT_VALID_ARGUMENTS(top_k == -1,
                         "top_k must be -1 when using greedy sampling.");
}
