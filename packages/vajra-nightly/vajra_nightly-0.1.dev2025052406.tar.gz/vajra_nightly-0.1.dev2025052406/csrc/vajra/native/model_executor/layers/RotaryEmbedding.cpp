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
#include "native/model_executor/layers/RotaryEmbedding.h"

#include "kernels/ops.h"
//==============================================================================
using vajra::RotaryEmbedding;
//==============================================================================
RotaryEmbedding::RotaryEmbedding(int head_size /*[in]*/,
                                 int rotary_dim /*[in]*/,
                                 int64_t max_position_embeddings /*[in]*/,
                                 int64_t base /*[in]*/,
                                 bool is_neox_style /*[in]*/,
                                 const torch::Tensor& cos_sin_cache /*[in]*/)
    : head_size_(head_size),
      rotary_dim_(rotary_dim),
      max_position_embeddings_(max_position_embeddings),
      base_(base),
      is_neox_style_(is_neox_style),
      cos_sin_cache_(cos_sin_cache) {}
//==============================================================================
std::pair<torch::Tensor, torch::Tensor> RotaryEmbedding::Forward(
    const torch::Tensor& positions /*[in]*/, torch::Tensor& query /*[inout]*/,
    torch::Tensor& key /*[inout]*/
) const {
  rotary_embedding(positions, query, key, head_size_, cos_sin_cache_,
                   is_neox_style_);
  return std::make_pair(query, key);
}
//==============================================================================
