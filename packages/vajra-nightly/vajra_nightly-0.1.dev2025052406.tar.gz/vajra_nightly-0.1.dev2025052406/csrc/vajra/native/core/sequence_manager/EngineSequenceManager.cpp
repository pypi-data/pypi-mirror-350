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
#include "native/core/sequence_manager/EngineSequenceManager.h"

namespace vajra {
void EngineSequenceManager::OnAppendToken(MutableSequencePtr, std::size_t) {
  // No-op
  // This is left empty since engine sequence manager append token happens async
  // directly invoked from the controller
}

void EngineSequenceManager::OnAppendTokenImpl(MutableSequencePtr seq) {
  ASSERT_VALID_POINTER_ARGUMENT(seq);

  auto [new_text, prefix_offset, read_offset] = tokenizer_->PartialDecode(
      *seq->GetOutputTokenIds(), seq->prefix_offset, seq->read_offset);
  seq->output_text += new_text;
  seq->prefix_offset = prefix_offset;
  seq->read_offset = read_offset;
}
}  // namespace vajra
