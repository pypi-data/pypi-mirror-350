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
#include "native/datatypes/Sequence.h"

namespace vajra {

Sequence::Sequence(const std::string seq_id_param,
                   const std::string prompt_param,
                   const TokenIdsPtr prompt_token_ids_param,
                   const std::size_t block_size_param,
                   const TokenId eos_token_id_param,
                   const TimeS arrival_time_param,
                   const SamplingParams sampling_params_param)
    : seq_id(seq_id_param),
      prompt(prompt_param),
      block_size(block_size_param),
      eos_token_id(eos_token_id_param),
      arrival_time(arrival_time_param),
      sampling_params(sampling_params_param),
      prompt_token_ids_(prompt_token_ids_param),
      state_(seq_id_param, arrival_time_param, prompt_token_ids_param->size()),
      token_range_tracker_(0, TokenRangeState::Unprocessed) {
  if (prompt_token_ids_param) AppendTokensToBlocks(*prompt_token_ids_param);
}

void Sequence::UpdateTokensProcessed(std::size_t num_tokens /*[in]*/) {
  ASSERT_VALID_RUNTIME(prompt_processing_finished_,
                       "prompt processing not finished!");
  ASSERT_VALID_RUNTIME(num_tokens > 0,
                       "num_tokens must be greater than zero. Got {}",
                       num_tokens);
  std::size_t tokens_processed = GetNumTokensProcessed();
  std::size_t total_num_processed = tokens_processed + num_tokens;
  ASSERT_VALID_RUNTIME(total_num_processed <= prompt_token_ids_->size() +
                                                  output_token_ids_->size(),
                       "number of processed tokens (from {} to {}) exceeds the "
                       "total number of tokens ({} + {})",
                       tokens_processed, total_num_processed,
                       prompt_token_ids_->size(), output_token_ids_->size());
  token_range_tracker_.UpdateRange(
      /*start=*/tokens_processed,
      /*end=*/total_num_processed,
      /*status=*/TokenRangeState::Processed);
}

void Sequence::UpdatePromptTokensProcessed(std::size_t num_tokens /*[in]*/) {
  ASSERT_VALID_RUNTIME(!prompt_processing_finished_,
                       "prompt processing finished!");
  ASSERT_VALID_RUNTIME(num_tokens > 0,
                       "num_tokens must be greater than zero. Got {}",
                       num_tokens);
  std::size_t prompt_tokens_processed = GetNumPromptTokensProcessed();
  std::size_t num_processed = prompt_tokens_processed + num_tokens;
  ASSERT_VALID_RUNTIME(
      num_processed <= prompt_token_ids_->size(),
      "number of processed prompt tokens (from {} to {}) exceeds the "
      "number of prompt "
      "tokens {}",
      prompt_tokens_processed, num_processed, prompt_token_ids_->size());

  token_range_tracker_.UpdateRange(
      /*start=*/prompt_tokens_processed,
      /*end=*/num_processed,
      /*state=*/TokenRangeState::Processed);

  if (num_processed == prompt_token_ids_->size()) {
    ASSERT_VALID_RUNTIME(
        prompt_stage_processing_finished_,
        "prompt stage processing has not finished even though the number of "
        "processed prompt tokens equals number of prompt token ids");
    prompt_processing_finished_ = true;
    state_.OnPromptProcessingCompleted();
  }
}

void Sequence::UpdatePromptTokensStageProcessed(
    std::size_t num_tokens /*[in]*/) {
  ASSERT_VALID_RUNTIME(!prompt_processing_finished_,
                       "prompt processing finished!");
  ASSERT_VALID_RUNTIME(!prompt_stage_processing_finished_,
                       "prompt stage processing finished!");
  ASSERT_VALID_RUNTIME(num_tokens > 0,
                       "num_tokens must be greater than zero. Got {}",
                       num_tokens);

  std::size_t prompt_tokens_stage_processed =
      GetNumPromptTokensStageProcessed();
  std::size_t num_processed = prompt_tokens_stage_processed + num_tokens;
  ASSERT_VALID_RUNTIME(
      num_processed <= prompt_token_ids_->size(),
      "number of processed stage prompt tokens (from {} to {}) exceeds the "
      "number of prompt "
      "tokens {}",
      prompt_tokens_stage_processed, num_processed, prompt_token_ids_->size());

  token_range_tracker_.UpdateRange(
      /*start=*/prompt_tokens_stage_processed,
      /*end=*/num_processed,
      /*state=*/TokenRangeState::StageProcessed);

  if (num_processed == prompt_token_ids_->size()) {
    prompt_stage_processing_finished_ = true;
  }
}

void Sequence::AppendTokenId(TokenId token_id /*[in]*/) {
  // The token need not be appended to the sequence when processing partial
  // prefill chunks
  ASSERT_VALID_RUNTIME(prompt_processing_finished_,
                       "prompt processed not finished!");

  output_token_ids_->push_back(token_id);
  AppendTokensToBlocks(std::vector<TokenId>{token_id});
  state_.OnTokenGenerated();
}

// TODO(elton): I don't like that we have to create a new vector here. But it
// turned out to be the simplest to crank out.
//
// I looked into returning a const_iterator, but C++ does not have a native
// mechanism to connect two iterators together. We need this because the
// returned iterator could potentially have to iterator over two vectors
// (`prompt_token_ids_` and `output_token_ids_`).
std::vector<TokenId> Sequence::GetLastNTokenIds(
    std::size_t n /*[in]*/, bool truncate /*= false*/) const {
  if (!truncate) {
    ASSERT_VALID_RUNTIME(
        n <= Length(),
        "n must not exceed total number of tokens (prompt {} + output {} = "
        "{}). Got {}",
        GetPromptLength(), GetOutputLength(), Length(), n);
  } else {
    n = std::min(n, Length());
  }

  if (n <= GetOutputLength()) {
    return std::vector<TokenId>(output_token_ids_->end() - n,
                                output_token_ids_->end());
  }

  std::size_t remaining = n - output_token_ids_->size();
  std::vector<TokenId> result;
  result.insert(result.end(), prompt_token_ids_->end() - remaining,
                prompt_token_ids_->end());
  result.insert(result.end(), output_token_ids_->begin(),
                output_token_ids_->end());
  return result;
}

void Sequence::Reset() {
  SetStatus(SequenceStatus::WaitingPreempted);
  prompt_processing_finished_ = false;
  prompt_stage_processing_finished_ = false;
  prompt_token_ids_->insert(prompt_token_ids_->end(),
                            output_token_ids_->begin(),
                            output_token_ids_->end());
  output_token_ids_->clear();
}

void Sequence::CheckStop(std::size_t num_new_tokens /*[in]*/) {
  if (GetOutputLength() == sampling_params.max_tokens) {
    SetStatus(SequenceStatus::FinishedLengthCapped);
    return;
  }
  auto token_ids = GetLastNTokenIds(num_new_tokens);
  bool found_eos_id = false;
  for (auto token_id : token_ids) {
    if (token_id == eos_token_id) {
      found_eos_id = true;
      break;
    }
  }
  if (!sampling_params.ignore_eos && found_eos_id) {
    SetStatus(SequenceStatus::FinishedStopped);
    return;
  }
}

void Sequence::AppendLogicalBlock() {
  auto block = std::make_shared<LogicalTokenBlock>(logical_token_blocks_.size(),
                                                   block_size);
  logical_token_blocks_.emplace_back(block);
}

void Sequence::AppendTokensToBlocks(const TokenIds& token_ids /*[in]*/) {
  std::size_t cursor = 0;

  if (logical_token_blocks_.size() == 0) {
    AppendLogicalBlock();
  }

  while (cursor < token_ids.size()) {
    auto last_block = logical_token_blocks_.back();
    if (last_block->IsFull()) {
      AppendLogicalBlock();
      last_block = logical_token_blocks_.back();
    }
    std::size_t num_empty_slots = last_block->NumEmptySlots();
    last_block->AppendTokens(std::vector<std::size_t>(
        token_ids.begin() + cursor,
        min(token_ids.begin() + cursor + num_empty_slots, token_ids.end())));
    cursor += num_empty_slots;
  }

  token_range_tracker_.AppendRange(token_ids.size(),
                                   TokenRangeState::Unprocessed);
}

}  // namespace vajra
