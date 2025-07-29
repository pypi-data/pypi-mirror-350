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
#include "native/model_executor/layers/NormLayers.h"

#include "kernels/ops.h"
//==============================================================================
using vajra::RMSNorm;
//==============================================================================
RMSNorm::RMSNorm(const torch::Tensor& weight /*[in]*/,
                 double variance_epsilon /*[in]*/)
    : weight_(weight), variance_epsilon_(variance_epsilon) {}
//==============================================================================
torch::Tensor RMSNorm::Forward(const torch::Tensor& input /*[in]*/) const {
  torch::Tensor out = torch::empty_like(input);
  rms_norm(out, input, weight_, variance_epsilon_);
  return out;
}
//==============================================================================
