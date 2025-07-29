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
#include "commons/ClassTraits.h"
#include "commons/Logging.h"
#include "commons/StdCommon.h"
#include "commons/TorchCommon.h"
//==============================================================================
namespace vajra {
//==============================================================================
class RotaryEmbedding : public NonCopyableNonMovable {
 public:
  RotaryEmbedding(int head_size /*[in]*/, int rotary_dim /*[in]*/,
                  int64_t max_position_embeddings /*[in]*/,
                  int64_t base /*[in]*/, bool is_neox_style /*[in]*/,
                  const torch::Tensor& cos_sin_cache /*[in]*/);

  std::pair<torch::Tensor, torch::Tensor> Forward(
      const torch::Tensor& positions /*[in]*/, torch::Tensor& query /*[inout]*/,
      torch::Tensor& key /*[inout]*/
  ) const;

 private:
  const int head_size_;
  const int rotary_dim_;
  const int64_t max_position_embeddings_;
  const int64_t base_;
  const bool is_neox_style_;
  const torch::Tensor cos_sin_cache_;
};
//==============================================================================
using RotaryEmbeddingPtr = std::shared_ptr<const RotaryEmbedding>;
//==============================================================================
}  // namespace vajra
//==============================================================================
