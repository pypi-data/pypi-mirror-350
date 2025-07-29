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
#include "commons/Logging.h"
#include "commons/StdCommon.h"
//==============================================================================
namespace vajra {
//==============================================================================
constexpr float SAMPLING_EPS = 1e-5f;

enum class SamplingType { Greedy, Random };

class SamplingParams {
 public:
  SamplingParams(float temperature_param = 1.0f /*[in]*/,
                 float top_p_param = 1.0f /*[in]*/,
                 int top_k_param = -1 /*[in]*/,
                 bool ignore_eos_param = false /*[in]*/,
                 std::size_t max_tokens_param = 2048 /*[in]*/)
      : temperature(temperature_param),
        top_p(top_p_param),
        top_k(top_k_param),
        ignore_eos(ignore_eos_param),
        max_tokens(max_tokens_param) {
    VerifyArgs();
    if (temperature < SAMPLING_EPS) VerifyGreedySampling();
  }

  // define copy constructor
  SamplingParams(const SamplingParams& other)
      : temperature(other.temperature),
        top_p(other.top_p),
        top_k(other.top_k),
        ignore_eos(other.ignore_eos),
        max_tokens(other.max_tokens) {}

  inline SamplingType GetSamplingType() const {
    return (temperature < SAMPLING_EPS) ? SamplingType::Greedy
                                        : SamplingType::Random;
  }

  std::string ToString() const {
    return std::format(
        "SamplingParams("
        "Temperature: {},"
        "TopP: {},"
        "TopK: {},"
        "IgnoreEos: {},"
        "NumMaxtokens: {})",
        temperature, top_p, top_k, ignore_eos, max_tokens);
  }

  const float temperature;
  const float top_p;
  const int top_k;
  const bool ignore_eos;
  const std::size_t max_tokens;

 private:
  void VerifyArgs() const;
  void VerifyGreedySampling() const;
};
}  // namespace vajra
