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
#include "commons/ClassTraits.h"
#include "commons/StdCommon.h"
#include "native/core/Types.h"
#include "native/core/tokenizer/Tokenizer.h"
#include "native/datatypes/SamplingParams.h"
#include "native/datatypes/Sequence.h"
//==============================================================================
namespace vajra {
//==============================================================================
struct TokenizerPoolInput {
  TokenizerPoolInput(const std::string& seq_id_param,
                     const TimeS arrival_time_param,
                     const std::string& prompt_param,
                     const SamplingParams sampling_params_param)
      : seq_id(seq_id_param),
        arrival_time(arrival_time_param),
        prompt(prompt_param),
        sampling_params(sampling_params_param) {}

  const std::string seq_id;
  const TimeS arrival_time;
  const std::string prompt;
  const SamplingParams sampling_params;
};
//==============================================================================
struct TokenizerPoolOutput {
  TokenizerPoolOutput(const std::string& seq_id_param,
                      const TimeS arrival_time_param,
                      const std::string& prompt_param,
                      const TokenIdsPtr token_ids_param,
                      const SamplingParams sampling_params_param)
      : seq_id(seq_id_param),
        arrival_time(arrival_time_param),
        prompt(prompt_param),
        token_ids(token_ids_param),
        sampling_params(sampling_params_param) {
    ASSERT_VALID_POINTER_ARGUMENT(token_ids);
  }

  const std::string seq_id;
  const TimeS arrival_time;
  const std::string prompt;
  const TokenIdsPtr token_ids;
  const SamplingParams sampling_params;
};
//==============================================================================
class TokenizerPool : public NonCopyableNonMovable {
 public:
  TokenizerPool(const std::string& tokenizer_path, std::size_t num_workers)
      : tokenizer_path_(tokenizer_path),
        num_workers_(num_workers),
        running_(false) {}

  ~TokenizerPool() { Shutdown(); }

  void Start();

  void AddRequest(TokenizerPoolInput input);

  void AddOutput(TokenizerPoolOutput output);

  std::optional<TokenizerPoolOutput> GetOutput();

  void Shutdown();

 private:
  void Loop();

  std::string tokenizer_path_;
  std::size_t num_workers_;

  std::vector<std::thread> workers_;

  Queue<TokenizerPoolInput> input_queue_;
  Queue<TokenizerPoolOutput> output_queue_;

  std::mutex mutex_;
  std::atomic<bool> running_;
};
//==============================================================================
}  // namespace vajra
//==============================================================================
