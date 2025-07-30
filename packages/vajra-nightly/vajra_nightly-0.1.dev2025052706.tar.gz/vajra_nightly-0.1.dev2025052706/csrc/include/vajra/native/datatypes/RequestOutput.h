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
#include "commons/Constants.h"
#include "native/datatypes/Sequence.h"
#include "native/datatypes/SequenceStatus.h"
//==============================================================================
namespace vajra {
//==============================================================================
struct RequestOutput {
  explicit RequestOutput(const SequencePtr seq_param)
      : seq(seq_param),
        finished(seq_param->IsFinished()),
        finish_reason(
            sequence_status::GetFinishedReason(seq_param->GetStatus())) {}

  inline const std::string& GetText() const { return seq->output_text; }
  inline const std::string& GetSeqId() const { return seq->seq_id; }
  inline const std::string& GetPrompt() const { return seq->prompt; }
  inline TokenIdsPtr GetPromptTokenIds() const {
    return seq->GetPromptTokenIds();
  }
  inline TokenIdsPtr GetTokenIds() const { return seq->GetOutputTokenIds(); }

  /// @brief Convert to string representation
  /// @return String representation of the RequestOutput
  [[nodiscard]] std::string ToString() const {
    return std::format(
        "RequestOutput(seq_id={}, finished={}, finish_reason={}, "
        "prompt_len={}, output_len={})",
        GetSeqId(), finished,
        finish_reason.has_value() ? finish_reason.value() : kNoneString,
        seq->GetPromptLength(), seq->GetOutputLength());
  }

  const SequencePtr seq;
  const bool finished;
  const std::optional<std::string> finish_reason;
};
//==============================================================================
using RequestOutputPtr = std::shared_ptr<RequestOutput>;
//==============================================================================
}  // namespace vajra
//==============================================================================
