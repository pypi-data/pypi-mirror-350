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
#include "kernels/ops.h"
#include "native/datatypes/SequenceMetadata.h"
#include "native/model_executor/layers/attention/flashinfer/BatchPrefillWithPagedKVCacheWrapper.h"
//==============================================================================
namespace vajra {
//==============================================================================
constexpr std::size_t FLASHINFER_WORKSPACE_SIZE = 128 * 1024 * 1024;
//==============================================================================
class FlashinferAttentionWrapper : public NonCopyableNonMovable {
 public:
  FlashinferAttentionWrapper() = delete;

  FlashinferAttentionWrapper(std::size_t num_q_heads /*[in]*/,
                             std::size_t num_kv_heads /*[in]*/,
                             std::size_t head_dim /*[in]*/,
                             std::size_t block_size /*[in]*/,
                             torch::Device device /*[in]*/);

  void BeginForward(const SequenceMetadataVector& seq_metadata_list /*[in]*/);

  void EndForward();

  void Run(const torch::Tensor& query /*[in]*/, torch::Tensor& output /*[out]*/,
           torch::Tensor& logsumexp /*[out]*/,
           const torch::Tensor& kv_cache /*[in]*/);

  void SaveKVCache(const torch::Tensor& key /*[in]*/,
                   const torch::Tensor& value /*[in]*/,
                   torch::Tensor& kv_cache /*[out]*/);

  [[nodiscard]] std::size_t GetNumQTokens() const {
    ASSERT_VALID_RUNTIME(metadata_initialized_,
                         "Metadata not initialized. Call BeginForward first.");
    return num_q_tokens_;
  }

  // Helper methods for testing
  [[nodiscard]] std::size_t GetNumQTokensWithoutValidation() const {
    return num_q_tokens_;
  }
  [[nodiscard]] bool GetIsNoOp() const { return is_no_op_; }
  [[nodiscard]] bool GetShouldSaveKVCache() const {
    return should_save_kv_cache_;
  }
  [[nodiscard]] bool GetIsMetadataInitialized() const {
    return metadata_initialized_;
  }
  [[nodiscard]] std::optional<torch::Tensor> GetSlotMappingTensor() const {
    return slot_mapping_tensor_;
  }

 private:
  torch::Tensor ToIntTensor(const std::vector<int32_t>& data /*[in]*/) const;
  torch::Tensor ToLongTensor(const std::vector<int64_t>& data /*[in]*/) const;

  // Configuration
  const std::size_t num_q_heads_;
  const std::size_t num_kv_heads_;
  const std::size_t head_dim_;
  const std::size_t block_size_;
  const torch::Device device_;

  // State
  bool is_no_op_;
  bool should_save_kv_cache_;
  bool metadata_initialized_;
  std::size_t num_q_tokens_;

  // Tensors
  torch::Tensor qo_indptr_tensor_;
  torch::Tensor kv_page_indptr_tensor_;
  torch::Tensor kv_page_indices_tensor_;
  torch::Tensor kv_last_page_len_tensor_;
  std::optional<torch::Tensor> slot_mapping_tensor_;

  // KVP sequence metadata
  std::size_t kvp_seqs_offset_;
  std::vector<std::size_t> kvp_seqs_qo_indptr_;
  std::vector<std::vector<std::size_t>> kvp_seqs_group_ids_;

  // BatchPrefillWithPagedKVCacheWrapper
  torch::Tensor workspace_buffer_;
  flashinfer::BatchPrefillWithPagedKVCacheWrapper wrapper_;
};
//==============================================================================
using FlashinferAttentionWrapperPtr =
    std::shared_ptr<FlashinferAttentionWrapper>;
//==============================================================================
}  // namespace vajra
//==============================================================================
