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
#include "native/datatypes/SequenceMetadata.h"
#include "native/model_executor/layers/attention/FlashinferAttentionWrapper.h"
#include "native/model_executor/layers/attention/SequenceArrangement.h"
//==============================================================================
namespace vajra {
//==============================================================================
class AttentionWrapper;
//==============================================================================
using AttentionWrapperPtr = std::shared_ptr<AttentionWrapper>;
//==============================================================================
struct AttentionWrapperArgs {
  std::size_t num_q_heads;
  std::size_t num_kv_heads;
  std::size_t head_dim;
  std::size_t block_size;
  torch::Device device;
  torch::ScalarType dtype;
};
//==============================================================================
class AttentionWrapper : public NonCopyableNonMovable {
 public:
  AttentionWrapper() = delete;

  AttentionWrapper(std::size_t num_q_heads /*[in]*/,
                   std::size_t num_kv_heads /*[in]*/,
                   std::size_t head_dim /*[in]*/,
                   std::size_t block_size /*[in]*/,
                   torch::Device device /*[in]*/,
                   torch::ScalarType dtype /*[in]*/);

  void BeginForward(const SequenceMetadataVector& seq_metadata_list /*[in]*/);

  void EndForward();

  [[nodiscard]] torch::Tensor Forward(const torch::Tensor& query /*[in]*/,
                                      const torch::Tensor& key /*[in]*/,
                                      const torch::Tensor& value /*[in]*/,
                                      torch::Tensor& kv_cache /*[inout]*/,
                                      std::size_t layer_id /*[in]*/);

  // Get a cache block tensor with the specified number of blocks
  [[nodiscard]] static torch::Tensor GetCacheBlock(
      std::size_t num_blocks /*[in]*/);

  // Thread local instance methods
  static void InitializeStaticArgs(std::size_t num_q_heads /*[in]*/,
                                   std::size_t num_kv_heads /*[in]*/,
                                   std::size_t head_dim /*[in]*/,
                                   std::size_t block_size /*[in]*/,
                                   torch::Device device /*[in]*/,
                                   torch::ScalarType dtype /*[in]*/
  );

  [[nodiscard]] static AttentionWrapperPtr GetOrCreateThreadLocalInstance();

 private:
  // Configuration
  const std::size_t num_q_heads_;
  const std::size_t num_kv_heads_;
  const std::size_t head_dim_;
  const std::size_t block_size_;
  const torch::Device device_;
  const torch::ScalarType dtype_;

  // State
  bool is_metadata_initialized_;
  bool is_profiling_iteration_;

  SequenceArrangement sequence_arrangement_;
  std::vector<std::unique_ptr<FlashinferAttentionWrapper>> wrappers_;

  // Static initialization args
  static std::optional<AttentionWrapperArgs> args_;

  // Thread local instance
  static thread_local AttentionWrapperPtr instance_;
};
//==============================================================================
}  // namespace vajra
//==============================================================================
