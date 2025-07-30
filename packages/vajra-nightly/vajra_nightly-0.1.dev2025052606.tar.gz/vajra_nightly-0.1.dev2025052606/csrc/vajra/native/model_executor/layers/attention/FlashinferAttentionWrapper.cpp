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
#include "native/model_executor/layers/attention/FlashinferAttentionWrapper.h"
//==============================================================================
using vajra::FlashinferAttentionWrapper;
//==============================================================================
FlashinferAttentionWrapper::FlashinferAttentionWrapper(
    std::size_t num_q_heads /*[in]*/, std::size_t num_kv_heads /*[in]*/,
    std::size_t head_dim /*[in]*/, std::size_t block_size /*[in]*/,
    torch::Device device /*[in]*/)
    : num_q_heads_(num_q_heads),
      num_kv_heads_(num_kv_heads),
      head_dim_(head_dim),
      block_size_(block_size),
      device_(device),
      is_no_op_(false),
      should_save_kv_cache_(false),
      metadata_initialized_(false),
      num_q_tokens_(0),
      kvp_seqs_offset_(0),
      kvp_seqs_qo_indptr_({0}),
      workspace_buffer_(torch::empty(
          FLASHINFER_WORKSPACE_SIZE,
          torch::TensorOptions().dtype(torch::kUInt8).device(device))),
      wrapper_(workspace_buffer_) {
  // Initialize empty tensors
  auto options = torch::TensorOptions().dtype(torch::kInt32).device(device_);
  qo_indptr_tensor_ = torch::empty(0, options);
  kv_page_indptr_tensor_ = torch::empty(0, options);
  kv_page_indices_tensor_ = torch::empty(0, options);
  kv_last_page_len_tensor_ = torch::empty(0, options);
}
//==============================================================================
torch::Tensor FlashinferAttentionWrapper::ToIntTensor(
    const std::vector<int32_t>& data /*[in]*/) const {
  return torch::tensor(
      data, torch::TensorOptions().dtype(torch::kInt32).device(device_));
}
//==============================================================================
torch::Tensor FlashinferAttentionWrapper::ToLongTensor(
    const std::vector<int64_t>& data /*[in]*/) const {
  return torch::tensor(
      data, torch::TensorOptions().dtype(torch::kInt64).device(device_));
}
//==============================================================================
void FlashinferAttentionWrapper::BeginForward(
    const SequenceMetadataVector& seq_metadata_list /*[in]*/) {
  // Reset metadata initialization flag at the beginning of forward pass
  ASSERT_VALID_RUNTIME(!metadata_initialized_,
                       "Metadata already initialized. Call EndForward first.");

  metadata_initialized_ = true;

  is_no_op_ = seq_metadata_list.empty();
  num_q_tokens_ = 0;

  if (is_no_op_) {
    return;
  }

  // The indptr tensor captures the location query tokens in the input tensor.
  // Flashinfer calls this layout as a raggedtensor. The indptr tensor captures
  // the start of each sequence in the ragged tensor. The length of the indptr
  // tensor is the number of sequences + 1. We perform both prefill and decode
  // attention in a single call to batched prefill kernel.
  std::vector<int32_t> qo_indptr{0};
  // The kv_page_indices tensor captures the pages of the key-value cache that
  // are assigned to each token in the input tensor. Since there is a variable
  // number of pages assigned to each sequence, a ragged tensor to represent
  // this.
  std::vector<int32_t> kv_page_indices;
  // the last page might not be full, so we need to keep track of the length of
  // the last page
  std::vector<int32_t> kv_last_page_len;
  // Since the prefill_kv_page_indices tensor is a ragged tensor, we also need
  // to keep track of the indptr tensor for the prefill_kv_page_indices tensor.
  // This tensor captures the start of each sequence in the ragged tensor.
  std::vector<int32_t> kv_page_indptr{0};
  std::vector<int64_t> slot_mapping;

  // We need to maintain additional metadata for KVP sequences.
  // This is metadata is required to perform the online softmax reduction
  // operation
  kvp_seqs_offset_ = 0;
  kvp_seqs_qo_indptr_ = {0};
  kvp_seqs_group_ids_.clear();

  // In kvp seqs, sometimes, we might not want to save the KV cache.
  // When this is true, we can't perform causal attention. So, we can either
  // execute requests which all require saving KV cache or none of them.
  bool all_save_kv_cache = true;
  bool none_save_kv_cache = true;
  for (const auto& seq_metadata : seq_metadata_list) {
    if (seq_metadata->save_kv_cache) {
      none_save_kv_cache = false;
    } else {
      all_save_kv_cache = false;
    }
  }

  ASSERT_VALID_RUNTIME(
      all_save_kv_cache || none_save_kv_cache,
      "All KVP sequences should either save KV cache or not save KV cache.");

  should_save_kv_cache_ = all_save_kv_cache;

  // The sequences are sorted as
  // | non kvp seqs | kvp seqs |
  bool started_kvp_seqs = false;

  for (const auto& seq_metadata : seq_metadata_list) {
    std::size_t num_q_tokens = seq_metadata->num_q_tokens;
    std::size_t num_kv_tokens = seq_metadata->num_kv_tokens;

    if (seq_metadata->is_kvp_request) {
      if (!started_kvp_seqs) {
        kvp_seqs_offset_ = qo_indptr.back();
        started_kvp_seqs = true;
      }

      kvp_seqs_qo_indptr_.push_back(kvp_seqs_qo_indptr_.back() + num_q_tokens);
      kvp_seqs_group_ids_.push_back(seq_metadata->kvp_group_ids);
    } else {
      ASSERT_VALID_RUNTIME(!started_kvp_seqs,
                           "Non-KVP sequences should come first.");
      ASSERT_VALID_RUNTIME(seq_metadata->save_kv_cache,
                           "Non-KVP sequences should save KV cache.");
    }

    if (should_save_kv_cache_) {
      num_kv_tokens += num_q_tokens;
    }

    std::size_t num_blocks_in_use =
        (num_kv_tokens + block_size_ - 1) / block_size_;
    num_blocks_in_use =
        std::min(num_blocks_in_use,
                 static_cast<std::size_t>(seq_metadata->block_table.size()));

    qo_indptr.push_back(qo_indptr.back() + num_q_tokens);
    kv_page_indices.insert(
        kv_page_indices.end(), seq_metadata->block_table.begin(),
        seq_metadata->block_table.begin() + num_blocks_in_use);
    kv_page_indptr.push_back(kv_page_indptr.back() + num_blocks_in_use);
    kv_last_page_len.push_back(num_kv_tokens % block_size_
                                   ? num_kv_tokens % block_size_
                                   : block_size_);

    if (!should_save_kv_cache_) {
      continue;
    }

    for (std::size_t i = 0; i < num_q_tokens; ++i) {
      std::size_t position_in_kv = i + seq_metadata->num_kv_tokens;
      std::size_t block_index = position_in_kv / block_size_;
      std::size_t block_offset = position_in_kv % block_size_;
      std::size_t block_num = seq_metadata->block_table[block_index];
      std::size_t slot = block_num * block_size_ + block_offset;
      slot_mapping.push_back(slot);
    }
  }

  num_q_tokens_ = qo_indptr.back();

  // Create the tensors internally
  qo_indptr_tensor_ = ToIntTensor(qo_indptr);
  kv_page_indptr_tensor_ = ToIntTensor(kv_page_indptr);
  kv_page_indices_tensor_ = ToIntTensor(kv_page_indices);
  kv_last_page_len_tensor_ = ToIntTensor(kv_last_page_len);

  wrapper_.Plan(qo_indptr_tensor_, kv_page_indptr_tensor_,
                kv_page_indices_tensor_, kv_last_page_len_tensor_, num_q_heads_,
                num_kv_heads_, head_dim_, block_size_, true,
                should_save_kv_cache_);

  if (should_save_kv_cache_) {
    slot_mapping_tensor_ = ToLongTensor(slot_mapping);
  }
}
//==============================================================================
void FlashinferAttentionWrapper::EndForward() {
  ASSERT_VALID_RUNTIME(metadata_initialized_,
                       "Metadata not initialized. Call BeginForward first.");

  // Reset the metadata initialization flag
  metadata_initialized_ = false;
}
//==============================================================================
void FlashinferAttentionWrapper::Run(const torch::Tensor& query /*[in]*/,
                                     torch::Tensor& output /*[out]*/,
                                     torch::Tensor& logsumexp /*[out]*/,
                                     const torch::Tensor& kv_cache /*[in]*/) {
  ASSERT_VALID_RUNTIME(metadata_initialized_,
                       "Metadata not initialized. Call BeginForward first.");

  if (is_no_op_) {
    return;
  }
  wrapper_.Run(query, kv_cache,
               std::nullopt,  // k_scale
               std::nullopt,  // v_scale
               output,        // out tensor to update
               logsumexp,     // lse tensor to update
               true           // return_lse
  );

  if (kvp_seqs_group_ids_.size() > 0) {
    // Perform online softmax reduction
    // TODO(Amey, Kasra): Integrate the new online softmax reduction kernel
  }
}
//==============================================================================
void FlashinferAttentionWrapper::SaveKVCache(
    const torch::Tensor& key /*[in]*/, const torch::Tensor& value /*[in]*/,
    torch::Tensor& kv_cache /*[out]*/) {
  ASSERT_VALID_RUNTIME(metadata_initialized_,
                       "Metadata not initialized. Call BeginForward first.");

  if (!should_save_kv_cache_ || is_no_op_) {
    return;
  }

  ASSERT_VALID_RUNTIME(slot_mapping_tensor_.has_value(),
                       "Slot mapping tensor not initialized.");

  torch::Tensor k_cache = kv_cache.index({torch::indexing::Slice(), 0});
  torch::Tensor v_cache = kv_cache.index({torch::indexing::Slice(), 1});

  reshape_and_cache_flashinfer(key, value, k_cache, v_cache,
                               slot_mapping_tensor_.value());
}
//==============================================================================
