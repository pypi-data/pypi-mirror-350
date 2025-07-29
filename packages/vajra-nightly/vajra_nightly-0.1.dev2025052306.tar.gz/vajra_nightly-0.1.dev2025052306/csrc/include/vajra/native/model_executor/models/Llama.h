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
#include "commons/TorchCommon.h"
#include "native/model_executor/layers/Activation.h"
#include "native/model_executor/layers/LinearLayers.h"
#include "native/model_executor/layers/NormLayers.h"
#include "native/model_executor/layers/RotaryEmbedding.h"
#include "native/model_executor/layers/attention/AttentionWrapper.h"
#include "native/model_executor/models/BaseModel.h"
//==============================================================================
namespace vajra {
class LlamaMLP {
 public:
  LlamaMLP(std::size_t layer_id /*[in]*/,
           ColumnParallelLinearPtr gate_up_proj /*[in]*/,
           RowParallelLinearPtr down_proj /*[in]*/);

  [[nodiscard]] torch::Tensor Forward(
      const torch::Tensor& input /*[in]*/) const;

 private:
  const std::size_t layer_id_;
  const ColumnParallelLinearPtr gate_up_proj_;
  const RowParallelLinearPtr down_proj_;
};
//==============================================================================
using LlamaMLPPtr = std::shared_ptr<const LlamaMLP>;
//==============================================================================
class LlamaAttention {
 public:
  LlamaAttention(int q_size /*[in]*/, int kv_size /*[in]*/,
                 float scaling /*[in]*/, std::size_t layer_id /*[in]*/,
                 ColumnParallelLinearPtr qkv_proj /*[in]*/,
                 RowParallelLinearPtr o_proj /*[in]*/,
                 RotaryEmbeddingPtr rotary_emb /*[in]*/);

  [[nodiscard]] torch::Tensor Forward(
      const torch::Tensor& positions,     /*[in]*/
      const torch::Tensor& hidden_states, /*[in]*/
      torch::Tensor& kv_cache             /*[inout]*/
  ) const;

 private:
  const int q_size_;
  const int kv_size_;
  const float scaling_;
  const std::size_t layer_id_;
  const ColumnParallelLinearPtr qkv_proj_;
  const RowParallelLinearPtr o_proj_;
  const RotaryEmbeddingPtr rotary_emb_;
};
//==============================================================================
using LlamaAttentionPtr = std::shared_ptr<const LlamaAttention>;
//==============================================================================
class LlamaDecoderLayer {
 public:
  LlamaDecoderLayer(std::size_t layer_id /*[in]*/,
                    LlamaAttentionPtr self_attn /*[in]*/,
                    LlamaMLPPtr mlp /*[in]*/,
                    RMSNormPtr input_layernorm /*[in]*/,
                    RMSNormPtr post_attention_layernorm /*[in]*/);

  [[nodiscard]] torch::Tensor Forward(const torch::Tensor& positions, /*[in]*/
                                      torch::Tensor& hidden_states, /*[inout]*/
                                      torch::Tensor& kv_cache       /*[inout]*/
  ) const;

 private:
  const std::size_t layer_id_;
  const LlamaAttentionPtr self_attn_;
  const LlamaMLPPtr mlp_;
  const RMSNormPtr input_layernorm_;
  const RMSNormPtr post_attention_layernorm_;
};
//==============================================================================
using LlamaDecoderLayerPtr = std::shared_ptr<const LlamaDecoderLayer>;
//==============================================================================
class LlamaModel : public BaseModel {
 public:
  LlamaModel(VocabParallelEmbeddingPtr embed_tokens /*[in]*/,
             std::vector<LlamaDecoderLayerPtr> layers /*[in]*/,
             RMSNormPtr norm /*[in]*/);

  ~LlamaModel() override = default;

  [[nodiscard]] torch::Tensor Forward(
      const torch::Tensor& positions /*[in]*/,
      torch::Tensor& hidden_states /*[inout]*/,
      std::vector<torch::Tensor>& kv_caches /*[inout]*/
  ) const override;

 private:
  const VocabParallelEmbeddingPtr embed_tokens_;
  const std::vector<LlamaDecoderLayerPtr> layers_;
  const RMSNormPtr norm_;
};
//==============================================================================
using LlamaModelPtr = std::shared_ptr<const LlamaModel>;
//==============================================================================
}  // namespace vajra
//==============================================================================
