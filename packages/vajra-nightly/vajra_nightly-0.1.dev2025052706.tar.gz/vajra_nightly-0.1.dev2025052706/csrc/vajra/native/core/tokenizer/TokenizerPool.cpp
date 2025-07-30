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
#include "native/core/tokenizer/TokenizerPool.h"
//==============================================================================
namespace vajra {
//==============================================================================
void TokenizerPool::Start() {
  std::lock_guard<std::mutex> lk(mutex_);
  if (running_) return;
  running_ = true;

  for (std::size_t i = 0; i < num_workers_; i++) {
    workers_.emplace_back(std::thread(&TokenizerPool::Loop, this));
  }
}
//==============================================================================
void TokenizerPool::AddRequest(TokenizerPoolInput input) {
  input_queue_.push(input);
}
//==============================================================================
void TokenizerPool::AddOutput(TokenizerPoolOutput output) {
  output_queue_.push(output);
}
//==============================================================================
std::optional<TokenizerPoolOutput> TokenizerPool::GetOutput() {
  try {
    return output_queue_.pull();
  } catch (const boost::sync_queue_is_closed& e) {
    return std::nullopt;
  }
}
//==============================================================================
void TokenizerPool::Loop() {
  auto tokenizer = Tokenizer::FromPath(tokenizer_path_);
  while (running_) {
    try {
      auto input = input_queue_.pull();
      auto token_ids = tokenizer.Encode(input.prompt);
      output_queue_.push(TokenizerPoolOutput(
          input.seq_id, input.arrival_time, input.prompt,
          std::make_shared<TokenIds>(token_ids), input.sampling_params));
    } catch (const boost::sync_queue_is_closed& e) {
      return;
    }
  }
}
//==============================================================================
void TokenizerPool::Shutdown() {
  std::lock_guard<std::mutex> lk(mutex_);

  if (!running_) return;

  running_ = false;

  input_queue_.close();
  output_queue_.close();

  for (auto& worker : workers_) {
    if (worker.joinable()) {
      worker.join();
    }
  }
}
//==============================================================================
}  // namespace vajra
//==============================================================================
