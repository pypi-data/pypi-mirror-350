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
#include "FlashinferAll.h"
#include "commons/Logging.h"
#include "commons/StdCommon.h"
#include "commons/TorchCommon.h"
#include "native/model_executor/layers/attention/flashinfer/Utils.h"
//==============================================================================
namespace vajra::flashinfer {
//==============================================================================
class BatchPrefillWithPagedKVCacheWrapper {
 public:
  BatchPrefillWithPagedKVCacheWrapper() = delete;

  BatchPrefillWithPagedKVCacheWrapper(
      torch::Tensor float_workspace_buffer /*[out]*/,
      std::string kv_layout = "NHD" /*[in]*/,
      std::string backend = "auto" /*[in]*/
  );

  ~BatchPrefillWithPagedKVCacheWrapper() = default;

  void Plan(const torch::Tensor& qo_indptr /*[in]*/,
            const torch::Tensor& paged_kv_indptr /*[in]*/,
            const torch::Tensor& paged_kv_indices /*[in]*/,
            const torch::Tensor& paged_kv_last_page_len /*[in]*/,
            int64_t num_qo_heads /*[in]*/, int64_t num_kv_heads /*[in]*/,
            int64_t head_dim_qk /*[in]*/, int64_t page_size /*[in]*/,
            bool non_blocking = false /*[in]*/, bool causal = false /*[in]*/,
            std::optional<int64_t> head_dim_vo = std::nullopt /*[in]*/,
            std::optional<torch::Tensor> custom_mask = std::nullopt /*[in]*/,
            std::optional<torch::Tensor> packed_custom_mask =
                std::nullopt /*[inout]*/,
            const std::string& pos_encoding_mode = "NONE" /*[in]*/,
            bool use_fp16_qk_reduction = false /*[in]*/,
            std::optional<double> sm_scale = std::nullopt /*[in]*/,
            int64_t window_left = -1 /*[in]*/,
            std::optional<double> logits_soft_cap = std::nullopt /*[in]*/,
            std::optional<double> rope_scale = std::nullopt /*[in]*/,
            std::optional<double> rope_theta = std::nullopt /*[in]*/,
            const std::string& q_data_type = "float16" /*[in]*/,
            std::optional<std::string> kv_data_type = std::nullopt /*[in]*/
  );

  RunOutput Run(const torch::Tensor& q /*[in]*/,
                const KVTensor& paged_kv_cache /*[in]*/,
                std::optional<double> k_scale = std::nullopt /*[in]*/,
                std::optional<double> v_scale = std::nullopt /*[in]*/,
                std::optional<torch::Tensor> out = std::nullopt /*[out]*/,
                std::optional<torch::Tensor> lse = std::nullopt /*[out]*/,
                bool return_lse = false /*[in]*/
  );

 private:
  // Workspace buffers
  torch::Tensor float_workspace_buffer_;
  torch::Tensor int_workspace_buffer_;
  torch::Tensor pin_memory_int_workspace_buffer_;

  // Auxiliary buffers
  torch::Tensor kv_lens_buffer_;
  torch::Tensor qo_indptr_buf_;
  torch::Tensor paged_kv_indptr_buf_;
  torch::Tensor paged_kv_indices_buf_;
  torch::Tensor paged_kv_last_page_len_buf_;
  std::optional<torch::Tensor> custom_mask_buf_;
  std::optional<torch::Tensor> mask_indptr_buf_;

  // FA3 backend specific buffers
  torch::Tensor vector_sparse_indices_buffer_;
  torch::Tensor vector_sparse_indptr_buffer_;

  // Plan info tensor
  torch::Tensor plan_info_;

  // Configuration parameters
  const std::string kv_layout_;
  std::string backend_;
  const bool use_cuda_graph_;
  bool causal_;
  std::string pos_encoding_mode_;
  bool use_fp16_qk_reduction_;
  int64_t window_left_;
  std::optional<double> logits_soft_cap_;
  std::optional<double> sm_scale_;
  std::optional<double> rope_scale_;
  std::optional<double> rope_theta_;

  // Data types
  at::ScalarType cached_q_data_type_;
  at::ScalarType cached_kv_data_type_;

  // Device
  const torch::Device device_;

  // Other parameters
  int64_t fixed_batch_size_;
  std::optional<int64_t> max_total_num_rows_;
};
//==============================================================================
using BatchPrefillWithPagedKVCacheWrapperPtr =
    std::shared_ptr<BatchPrefillWithPagedKVCacheWrapper>;
//==============================================================================
}  // namespace vajra::flashinfer
//==============================================================================
