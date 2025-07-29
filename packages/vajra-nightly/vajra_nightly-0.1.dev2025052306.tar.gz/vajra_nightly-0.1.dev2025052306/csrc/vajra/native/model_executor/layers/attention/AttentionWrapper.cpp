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
#include "native/model_executor/layers/attention/AttentionWrapper.h"
//==============================================================================
using vajra::AttentionWrapper;
using vajra::AttentionWrapperArgs;
using vajra::AttentionWrapperPtr;
//==============================================================================
// Initialize the static members
std::optional<AttentionWrapperArgs> AttentionWrapper::args_ = std::nullopt;
thread_local AttentionWrapperPtr AttentionWrapper::instance_ = nullptr;
//==============================================================================
AttentionWrapper::AttentionWrapper(std::size_t num_q_heads /*[in]*/,
                                   std::size_t num_kv_heads /*[in]*/,
                                   std::size_t head_dim /*[in]*/,
                                   std::size_t block_size /*[in]*/,
                                   torch::Device device /*[in]*/,
                                   torch::ScalarType dtype /*[in]*/)
    : num_q_heads_(num_q_heads),
      num_kv_heads_(num_kv_heads),
      head_dim_(head_dim),
      block_size_(block_size),
      device_(device),
      dtype_(dtype),
      is_metadata_initialized_(false),
      is_profiling_iteration_(false) {
  std::size_t num_sequence_splits = sequence_arrangement_.GetNumSplits();
  LOG_INFO("Creating {} native FlashinferAttentionWrapper instances.",
           num_sequence_splits);

  for (std::size_t i = 0; i < num_sequence_splits; ++i) {
    wrappers_.emplace_back(std::make_unique<FlashinferAttentionWrapper>(
        num_q_heads, num_kv_heads, head_dim, block_size, device));
  }
}
//==============================================================================
void AttentionWrapper::BeginForward(
    const SequenceMetadataVector& seq_metadata_list /*[in]*/) {
  ASSERT_VALID_RUNTIME(!is_metadata_initialized_,
                       "Metadata already initialized. Call EndForward first.");
  is_metadata_initialized_ = true;
  is_profiling_iteration_ = false;

  if (seq_metadata_list.empty() || seq_metadata_list[0]->block_table.empty()) {
    is_profiling_iteration_ = true;
    return;
  }

  sequence_arrangement_.CheckArrangementAndExtend(seq_metadata_list);
  auto split_seq_metadata_list = sequence_arrangement_.GetSplits();

  ASSERT_VALID_RUNTIME(split_seq_metadata_list.size() == wrappers_.size(),
                       "Invalid number of splits. Expected: {} Got: {}",
                       wrappers_.size(), split_seq_metadata_list.size());
  for (std::size_t i = 0; i < split_seq_metadata_list.size(); ++i) {
    wrappers_[i]->BeginForward(split_seq_metadata_list[i]);
  }
}
//==============================================================================
void AttentionWrapper::EndForward() {
  ASSERT_VALID_RUNTIME(is_metadata_initialized_,
                       "Metadata not initialized. Call BeginForward first.");
  is_metadata_initialized_ = false;

  if (is_profiling_iteration_) {
    return;
  }

  for (auto& wrapper : wrappers_) {
    wrapper->EndForward();
  }

  sequence_arrangement_.Clear();
}
//==============================================================================
torch::Tensor AttentionWrapper::Forward(const torch::Tensor& query /*[in]*/,
                                        const torch::Tensor& key /*[in]*/,
                                        const torch::Tensor& value /*[in]*/,
                                        torch::Tensor& kv_cache /*[inout]*/,
                                        std::size_t /*[in]*/) {
  ASSERT_VALID_RUNTIME(is_metadata_initialized_,
                       "Metadata not initialized. Call BeginForward first.");

  if (is_profiling_iteration_) {
    return torch::empty_like(query);
  }

  auto output = torch::empty(
      {query.size(0), static_cast<int64_t>(num_q_heads_),
       static_cast<int64_t>(head_dim_)},
      torch::TensorOptions().dtype(query.dtype()).device(query.device()));

  auto logsumexp = torch::empty(
      {query.size(0), static_cast<int64_t>(num_q_heads_)},
      torch::TensorOptions().dtype(torch::kFloat32).device(query.device()));

  // TODO(rayyan): [Add timer] Reshape inputs ATTN_INPUT_RESHAPE
  auto query_reshaped = query.reshape({-1, static_cast<int64_t>(num_q_heads_),
                                       static_cast<int64_t>(head_dim_)});
  auto key_reshaped = key.reshape({-1, static_cast<int64_t>(num_kv_heads_),
                                   static_cast<int64_t>(head_dim_)});
  auto value_reshaped = value.reshape({-1, static_cast<int64_t>(num_kv_heads_),
                                       static_cast<int64_t>(head_dim_)});

  // TODO(rayyan): [Add timer] Save kv_cache ATTN_KV_CACHE_SAVE
  {
    std::size_t q_offset = 0;
    for (auto& wrapper : wrappers_) {
      std::size_t q_len = wrapper->GetNumQTokens();

      if (q_len == 0) {
        continue;
      }

      wrapper->SaveKVCache(key_reshaped.slice(0, q_offset, q_offset + q_len),
                           value_reshaped.slice(0, q_offset, q_offset + q_len),
                           kv_cache);

      q_offset += q_len;
    }
  }

  // TODO(rayyan): [Add timer] Attention computation ATTN
  {
    std::size_t q_offset = 0;
    for (auto& wrapper : wrappers_) {
      std::size_t q_len = wrapper->GetNumQTokens();

      if (q_len == 0) {
        continue;
      }

      auto output_slice = output.slice(0, q_offset, q_offset + q_len);
      auto logsumexp_slice = logsumexp.slice(0, q_offset, q_offset + q_len);

      wrapper->Run(query_reshaped.slice(0, q_offset, q_offset + q_len),
                   output_slice, logsumexp_slice, kv_cache);

      q_offset += q_len;
    }
  }

  // TODO(rayyan): [Add timer] Reshape outputs ATTN_OUTPUT_RESHAPE
  auto output_reshaped =
      output.reshape({-1, static_cast<int64_t>(num_q_heads_ * head_dim_)});

  return output_reshaped;
}
//==============================================================================
torch::Tensor AttentionWrapper::GetCacheBlock(std::size_t num_blocks /*[in]*/) {
  // Create a tensor for the KV cache with the specified number of blocks
  // The shape is [num_blocks, 2, block_size, num_kv_heads, head_dim]
  // where 2 is for key and value
  ASSERT_VALID_RUNTIME(
      args_.has_value(),
      "InitializeStaticArgs must be called before GetCacheBlock");
  return torch::randn({static_cast<int64_t>(num_blocks), 2,
                       static_cast<int64_t>(args_.value().block_size),
                       static_cast<int64_t>(args_.value().num_kv_heads),
                       static_cast<int64_t>(args_.value().head_dim)},
                      torch::TensorOptions()
                          .dtype(args_.value().dtype)
                          .device(args_.value().device));
}
//==============================================================================
void AttentionWrapper::InitializeStaticArgs(std::size_t num_q_heads /*[in]*/,
                                            std::size_t num_kv_heads /*[in]*/,
                                            std::size_t head_dim /*[in]*/,
                                            std::size_t block_size /*[in]*/,
                                            torch::Device device /*[in]*/,
                                            torch::ScalarType dtype /*[in]*/) {
  args_ = AttentionWrapperArgs{num_q_heads, num_kv_heads, head_dim,
                               block_size,  device,       dtype};
}
//==============================================================================
AttentionWrapperPtr AttentionWrapper::GetOrCreateThreadLocalInstance() {
  ASSERT_VALID_RUNTIME(args_.has_value(),
                       "InitializeStaticArgs must be called before "
                       "GetOrCreateThreadLocalInstance");
  if (instance_ == nullptr) {
    instance_ = std::make_shared<AttentionWrapper>(
        args_.value().num_q_heads, args_.value().num_kv_heads,
        args_.value().head_dim, args_.value().block_size, args_.value().device,
        args_.value().dtype);
  }
  return instance_;
}
//==============================================================================
