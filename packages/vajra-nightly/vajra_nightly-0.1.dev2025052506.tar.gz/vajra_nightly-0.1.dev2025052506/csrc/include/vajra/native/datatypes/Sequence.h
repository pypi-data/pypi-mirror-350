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
#include "commons/BoostCommon.h"
#include "commons/Logging.h"
#include "commons/StdCommon.h"
#include "native/core/Types.h"
#include "native/datatypes/LogicalTokenBlock.h"
#include "native/datatypes/SamplingParams.h"
#include "native/datatypes/SequenceState.h"
#include "native/datatypes/TokenRangeTracker.h"
//==============================================================================
namespace vajra {
//==============================================================================
struct UserSequenceParams final {
  UserSequenceParams(const std::string seq_id_param,
                     const std::string prompt_param,
                     const TokenIdsPtr prompt_token_ids_param,
                     const TimeS arrival_time_param,
                     const SamplingParams sampling_params_param)
      : seq_id(seq_id_param),
        prompt(prompt_param),
        prompt_token_ids(prompt_token_ids_param),
        arrival_time(arrival_time_param),
        sampling_params(sampling_params_param) {
    ASSERT_VALID_POINTER_ARGUMENT(prompt_token_ids);
  }

  /// @brief Convert to string representation
  /// @return String representation of the UserSequenceParams
  [[nodiscard]] std::string ToString() const {
    return std::format(
        "UserSequenceParams(seq_id={}, prompt_len={}, arrival_time={}, "
        "sampling_params={})",
        seq_id, prompt_token_ids ? prompt_token_ids->size() : 0, arrival_time,
        sampling_params.ToString());
  }

  const std::string seq_id;
  const std::string prompt;
  const TokenIdsPtr prompt_token_ids;
  const TimeS arrival_time;
  const SamplingParams sampling_params;
};
//==============================================================================
struct SequenceParams final {
  SequenceParams(const std::string seq_id_param, const std::string prompt_param,
                 const TokenIdsPtr prompt_token_ids_param,
                 const std::size_t block_size_param,
                 const TokenId eos_token_id_param,
                 const TimeS arrival_time_param,
                 const SamplingParams sampling_params_param)
      : seq_id(seq_id_param),
        prompt(prompt_param),
        prompt_token_ids(prompt_token_ids_param),
        block_size(block_size_param),
        eos_token_id(eos_token_id_param),
        arrival_time(arrival_time_param),
        sampling_params(sampling_params_param) {
    ASSERT_VALID_POINTER_ARGUMENT(prompt_token_ids);
  }

  /// @brief Convert to string representation
  /// @return String representation of the SequenceParams
  [[nodiscard]] std::string ToString() const {
    return std::format(
        "SequenceParams(seq_id={}, prompt_len={}, block_size={}, "
        "eos_token_id={}, arrival_time={}, sampling_params={})",
        seq_id, prompt_token_ids ? prompt_token_ids->size() : 0, block_size,
        eos_token_id, arrival_time, sampling_params.ToString());
  }

  const std::string seq_id;
  const std::string prompt;
  const TokenIdsPtr prompt_token_ids;
  const std::size_t block_size;
  const TokenId eos_token_id;
  const TimeS arrival_time;
  const SamplingParams sampling_params;
};
//==============================================================================
class Sequence {
 public:
  Sequence(const std::string seq_id_param, const std::string prompt_param,
           const TokenIdsPtr prompt_token_ids_param,
           const std::size_t block_size_param, const TokenId eos_token_id_param,
           const TimeS arrival_time_param,
           const SamplingParams sampling_params_param);

  explicit Sequence(const SequenceParams& params)
      : Sequence(params.seq_id, params.prompt, params.prompt_token_ids,
                 params.block_size, params.eos_token_id, params.arrival_time,
                 params.sampling_params) {}

  inline SequenceStatus GetStatus() const { return state_.GetStatus(); }

  inline void SetStatus(SequenceStatus status /*[in]*/) {
    state_.SetStatus(status);
  }

  inline TokenIdsPtr GetPromptTokenIds() const { return prompt_token_ids_; }

  inline TokenIdsPtr GetOutputTokenIds() const { return output_token_ids_; }

  inline const std::vector<std::shared_ptr<vajra::LogicalTokenBlock>>&
  GetLogicalTokenBlocks() const {
    return logical_token_blocks_;
  }

  inline bool GetPromptProcessingFinished() const {
    return prompt_processing_finished_;
  }

  inline bool GetPromptStageProcessingFinished() const {
    return prompt_stage_processing_finished_;
  }

  inline const SequenceState& GetState() const { return state_; }

  void UpdateTokensProcessed(std::size_t num_tokens /*[in]*/);

  void UpdatePromptTokensProcessed(std::size_t num_tokens /*[in]*/);

  void UpdatePromptTokensStageProcessed(std::size_t num_tokens /*[in]*/);

  void AppendTokenId(TokenId token_id /*[in]*/);

  std::size_t GetNumProcessableTokens() const {
    auto next_unprocessed_range =
        token_range_tracker_.GetNextUnprocessedRange();
    return next_unprocessed_range.end - next_unprocessed_range.start;
  }

  inline std::size_t Length() const {
    return output_token_ids_->size() + prompt_token_ids_->size();
  }

  inline std::size_t GetPromptLength() const {
    return prompt_token_ids_->size();
  }

  inline std::size_t GetOutputLength() const {
    return output_token_ids_->size();
  }

  inline std::size_t GetNumPromptTokensProcessed() const {
    return std::min(GetPromptLength(), GetNumTokensProcessed());
  }

  inline std::size_t GetNumPromptTokensStageProcessed() const {
    return std::min(GetPromptLength(), GetNumTokensStageProcessed());
  }

  inline std::size_t GetNumTokensProcessed() const {
    return token_range_tracker_.GetProcessedPrefixLength();
  }

  inline std::size_t GetNumTokensStageProcessed() const {
    return token_range_tracker_.GetStageProcessedPrefixLength();
  }

  inline std::size_t GetLastTokenId() const {
    return output_token_ids_->size() > 0 ? output_token_ids_->back()
                                         : prompt_token_ids_->back();
  }

  std::vector<TokenId> GetLastNTokenIds(std::size_t n /*[in]*/,
                                        bool truncate = false) const;

  inline const std::vector<std::string>& GetTokens() const { return tokens_; }

  inline void SetTokens(const std::vector<std::string>& tokens /*[in]*/) {
    tokens_ = tokens;
  }

  inline void ExtendTokens(const std::vector<std::string>& tokens /*[in]*/) {
    tokens_.insert(tokens_.end(), tokens.begin(), tokens.end());
  }

  inline bool IsFinished() const {
    return sequence_status::IsFinished(state_.GetStatus());
  }
  inline bool IsExecuting() const {
    return sequence_status::IsExecuting(state_.GetStatus());
  }
  inline bool IsWaiting() const {
    return sequence_status::IsWaiting(state_.GetStatus());
  }
  inline bool IsPaused() const {
    return sequence_status::IsPaused(state_.GetStatus());
  }
  inline bool IsRunning() const {
    return sequence_status::IsRunning(state_.GetStatus());
  }
  inline bool IsWaitingPreempted() const {
    return sequence_status::IsWaitingPreempted(state_.GetStatus());
  }

  void Reset();

  void CheckStop(std::size_t num_new_tokens /*[in]*/);

  std::string ToString() {
    return std::format(
        "Sequence(seq_id={}, "
        "status={}, "
        "num_blocks={}, "
        "num_prompt_tokens={}, "
        "num_output_tokens={}, "
        "prompt_processing_finished={}, "
        "num_prompt_tokens_processed={}, "
        "num_prompt_tokens_stage_processed={}, "
        "prompt_stage_processing_finished={})",
        seq_id, GetStatus(), logical_token_blocks_.size(), GetPromptLength(),
        GetOutputLength(), prompt_processing_finished_,
        GetNumPromptTokensProcessed(), GetNumPromptTokensStageProcessed(),
        prompt_stage_processing_finished_);
  }

  [[nodiscard]] SequenceParams GetParams() const {
    return SequenceParams(seq_id, prompt, prompt_token_ids_, block_size,
                          eos_token_id, arrival_time, sampling_params);
  }

  const std::string seq_id;
  const std::string prompt;
  const std::size_t block_size;
  const TokenId eos_token_id;
  const TimeS arrival_time;
  const SamplingParams sampling_params;

  std::string output_text;

  std::size_t prefix_offset = 0;
  std::size_t read_offset = 0;

 private:
  void AppendLogicalBlock();

  void AppendTokensToBlocks(const TokenIds& token_ids /*[in]*/);

  TokenIdsPtr prompt_token_ids_ =
      std::make_shared<TokenIds>(std::vector<TokenId>());
  TokenIdsPtr output_token_ids_ =
      std::make_shared<TokenIds>(std::vector<TokenId>());
  bool prompt_processing_finished_ = false;
  bool prompt_stage_processing_finished_ = false;

  std::vector<std::shared_ptr<vajra::LogicalTokenBlock>> logical_token_blocks_;
  SequenceState state_;
  std::vector<std::string> tokens_;

  TokenRangeTracker token_range_tracker_;
};
//==============================================================================
using SequencePtr = std::shared_ptr<const Sequence>;
using Sequences = std::vector<SequencePtr>;

using MutableSequencePtr = std::shared_ptr<Sequence>;
using MutableSequences = std::vector<MutableSequencePtr>;

using UserSequenceParamsPtr = std::shared_ptr<const UserSequenceParams>;
using MutableUserSequenceParamsPtr = std::shared_ptr<UserSequenceParams>;
//==============================================================================
inline const vajra::Sequences& AsConstSequences(
    const vajra::MutableSequences& seqs) {
  // reinterpret_cast is typically forbidden in this codebase
  // but we use it for fast conversion of MutableSequences to Sequences (as
  // const)
  return *reinterpret_cast<const vajra::Sequences*>(&seqs);
}
//==============================================================================
}  // namespace vajra
//==============================================================================
