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
#include "native/model_executor/layers/Activation.h"

#include "kernels/ops.h"
//==============================================================================
using vajra::FastGELU;
using vajra::NewGELU;
using vajra::SiluAndMul;
//==============================================================================
torch::Tensor SiluAndMul::Forward(const torch::Tensor& input /*[in]*/) {
  const int64_t num_tokens = input.size(0);
  const int64_t d = input.size(1) / 2;
  torch::Tensor out = torch::empty({num_tokens, d}, input.options());
  silu_and_mul(out, input);
  return out;
}
//==============================================================================
torch::Tensor NewGELU::Forward(const torch::Tensor& input /*[in]*/) {
  const int64_t num_tokens = input.size(0);
  const int64_t d = input.size(1);
  torch::Tensor out = torch::empty({num_tokens, d}, input.options());
  gelu_new(out, input);
  return out;
}
//==============================================================================
torch::Tensor FastGELU::Forward(const torch::Tensor& input /*[in]*/) {
  const int64_t num_tokens = input.size(0);
  const int64_t d = input.size(1);
  torch::Tensor out = torch::empty({num_tokens, d}, input.options());
  gelu_fast(out, input);
  return out;
}
//==============================================================================
