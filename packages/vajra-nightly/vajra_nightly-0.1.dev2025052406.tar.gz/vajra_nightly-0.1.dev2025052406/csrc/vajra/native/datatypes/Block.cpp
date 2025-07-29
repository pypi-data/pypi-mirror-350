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
#include "native/datatypes/LogicalTokenBlock.h"

using vajra::LogicalTokenBlock;

void LogicalTokenBlock::AppendTokens(
    const std::vector<std::size_t>& token_ids /*[in]*/) {
  ASSERT_VALID_RUNTIME(token_ids.size() <= NumEmptySlots(),
                       "Not enough empty slots");
  std::size_t curr_idx = num_tokens_;
  std::copy(token_ids.begin(), token_ids.end(),
            this->token_ids_.begin() + curr_idx);
  num_tokens_ += token_ids.size();
}
