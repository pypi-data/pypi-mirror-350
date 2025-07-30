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
#include "native/model_executor/layers/attention/flashinfer/Utils.h"
//==============================================================================
namespace vajra::flashinfer {
//==============================================================================
bool IsFa3BackendSupported(int pos_encoding_mode /*[in]*/,
                           bool use_fp16_qk_reduction /*[in]*/,
                           bool use_custom_mask /*[in]*/,
                           at::ScalarType dtype_q /*[in]*/,
                           at::ScalarType dtype_kv /*[in]*/
) {
  if (use_custom_mask) {
    return false;
  }
  if (pos_encoding_mode != PosEncodingMode::NONE) {
    return false;
  }
  if (use_fp16_qk_reduction) {
    return false;
  }
  if (dtype_q == at::ScalarType::Float8_e4m3fn ||
      dtype_q == at::ScalarType::Float8_e5m2) {
    return false;
  }
  if (dtype_kv == at::ScalarType::Float8_e4m3fn ||
      dtype_kv == at::ScalarType::Float8_e5m2) {
    return false;
  }
  return true;
}
//==============================================================================
std::string DetermineAttentionBackend(torch::Device device /*[in]*/,
                                      int pos_encoding_mode /*[in]*/,
                                      bool use_fp16_qk_reduction /*[in]*/,
                                      bool use_custom_mask /*[in]*/,
                                      at::ScalarType dtype_q /*[in]*/,
                                      at::ScalarType dtype_kv /*[in]*/
) {
  ASSERT_VALID_RUNTIME(device.is_cuda(), "Expected CUDA device, but got: {}",
                       device.str());
  auto cc = GetCudaComputeCapability(device);
  int cuda_version = GetCudaRuntimeVersion();
  if (cc.major == 9 && cuda_version >= 12030 &&
      IsFa3BackendSupported(pos_encoding_mode, use_fp16_qk_reduction,
                            use_custom_mask, dtype_q, dtype_kv)) {
    return "fa3";
  }
  return "fa2";
}
//==============================================================================
torch::Tensor ComputePageMaskIndptr(
    const torch::Tensor& qo_indptr /*[in]*/,
    const torch::Tensor& paged_kv_indptr /*[in]*/,
    const torch::Tensor& paged_kv_last_page_len /*[in]*/,
    int64_t page_size /*[in]*/
) {
  ASSERT_VALID_RUNTIME(
      qo_indptr.size(0) == paged_kv_indptr.size(0),
      "The length of qo_indptr and paged_kv_indptr should be the same.");
  torch::Tensor mask_indptr = torch::empty_like(qo_indptr);

  // Set first element to 0
  mask_indptr.index_put_({0}, 0);

  // Calculate qo_diff
  auto qo_diff = qo_indptr.slice(0, 1) - qo_indptr.slice(0, 0, -1);

  // Calculate kv_lens
  auto kv_lens =
      (paged_kv_indptr.slice(0, 1) - paged_kv_indptr.slice(0, 0, -1) - 1) *
          page_size +
      paged_kv_last_page_len;

  // Calculate product and cumsum
  auto prod = qo_diff * kv_lens;
  auto cumsum = torch::cumsum(prod, 0);

  // Set remaining elements
  mask_indptr.index_put_({torch::indexing::Slice(1, torch::indexing::None)},
                         cumsum);

  return mask_indptr;
}
//==============================================================================
std::pair<torch::Tensor, torch::Tensor> SegmentPackbits(
    const torch::Tensor& x /*[in]*/, const torch::Tensor& indptr /*[in]*/,
    const std::string& bitorder /*[in]*/
) {
  ASSERT_VALID_RUNTIME(x.device().is_cuda(),
                       "Input tensor x must be on CUDA device");
  ASSERT_VALID_RUNTIME(bitorder == "big" || bitorder == "little",
                       "bitorder must be either 'big' or 'little'");

  // Calculate segment lengths and packed lengths
  auto seglen = indptr.slice(0, 1) - indptr.slice(0, 0, -1);
  auto packed_len = (seglen + 7) / 8;

  // Create new indptr tensor
  auto indptr_new = torch::zeros_like(indptr);
  auto cumsum = torch::cumsum(packed_len, 0);
  indptr_new.index_put_({torch::indexing::Slice(1, torch::indexing::None)},
                        cumsum);

  // Get output size and create output tensor
  int64_t output_nnzs = indptr_new.index({-1}).item<int32_t>();
  auto y = torch::empty({output_nnzs},
                        torch::dtype(torch::kUInt8).device(x.device()));

  // Convert indptrs to int32
  auto indptr_int32 = indptr.to(torch::kInt32);
  auto indptr_new_int32 = indptr_new.to(torch::kInt32);

  // Call FlashInfer's segment_packbits
  segment_packbits(x, indptr_int32, indptr_new_int32, bitorder, y);

  return std::make_pair(y, indptr_new_int32);
}
//==============================================================================
torch::Tensor GetSeqLens(const torch::Tensor& kv_indptr /*[in]*/,
                         const torch::Tensor& kv_last_page_len /*[in]*/,
                         int64_t page_size /*[in]*/
) {
  auto diff = kv_indptr.slice(0, 1) - kv_indptr.slice(0, 0, -1) - 1;
  auto clamped = torch::clamp(diff, 0).mul(page_size);
  return clamped.add(kv_last_page_len);
}
//==============================================================================
torch::Tensor Expand4D(const torch::Tensor& x /*[in]*/,
                       const std::string& kv_layout /*[in]*/
) {
  ASSERT_VALID_RUNTIME(x.dim() == 3 || x.dim() == 4,
                       "x must be a 3D or 4D tensor");
  if (x.dim() == 3) {
    if (kv_layout == "NHD") {
      return x.unsqueeze(-3);
    } else if (kv_layout == "HND") {
      return x.unsqueeze(-2);
    } else {
      ASSERT_VALID_RUNTIME(false, "Invalid kv_layout {}", kv_layout);
    }
  }
  return x;
}
//==============================================================================
torch::Tensor Expand5D(const torch::Tensor& x /*[in]*/,
                       const std::string& kv_layout /*[in]*/
) {
  ASSERT_VALID_RUNTIME(x.dim() == 4 || x.dim() == 5,
                       "x must be a 4D or 5D tensor");
  if (x.dim() == 4) {
    if (kv_layout == "NHD") {
      return x.unsqueeze(-3);
    } else if (kv_layout == "HND") {
      return x.unsqueeze(-2);
    } else {
      ASSERT_VALID_RUNTIME(false, "Invalid kv_layout {}", kv_layout);
    }
  }
  return x;
}
//==============================================================================
SplitKVTensor UnpackPagedKVCache(const KVTensor& paged_kv_cache /*[in]*/,
                                 const std::string& kv_layout /*[in]*/
) {
  if (std::holds_alternative<SplitKVTensor>(paged_kv_cache)) {
    auto& [paged_k_cache, paged_v_cache] =
        std::get<SplitKVTensor>(paged_kv_cache);

    auto paged_k_cache_expanded = Expand4D(paged_k_cache, kv_layout);
    auto paged_v_cache_expanded = Expand4D(paged_v_cache, kv_layout);

    return {paged_k_cache_expanded, paged_v_cache_expanded};
  } else {
    auto& paged_kv_cache_tensor = std::get<UnifiedKVTensor>(paged_kv_cache);
    auto paged_kv_cache_tensor_expanded =
        Expand5D(paged_kv_cache_tensor, kv_layout);
    // Split on second dimension
    auto paged_k_cache = paged_kv_cache_tensor_expanded.select(1, 0);
    auto paged_v_cache = paged_kv_cache_tensor_expanded.select(1, 1);
    return {paged_k_cache, paged_v_cache};
  }
}
//==============================================================================
void CheckCachedQKVDataType(const torch::Tensor& q /*[in]*/,
                            const torch::Tensor& k /*[in]*/,
                            at::ScalarType dtype_q /*[in]*/,
                            at::ScalarType dtype_kv /*[in]*/
) {
  ASSERT_VALID_RUNTIME(q.scalar_type() == dtype_q,
                       "The dtype of q does not match the q_data_type "
                       "specified in plan function.");
  ASSERT_VALID_RUNTIME(k.scalar_type() == dtype_kv,
                       "The dtype of k does not match the kv_data_type "
                       "specified in plan function.");
}
//==============================================================================
torch::Tensor BlockSparseIndicesToVectorSparseOffsets(
    const torch::Tensor& block_sparse_indices /*[in]*/,
    const torch::Tensor& block_sparse_indptr /*[in]*/,
    torch::Tensor& vector_sparse_offsets /*[out]*/,
    torch::Tensor& vector_sparse_indptr /*[out]*/,
    const torch::Tensor& kv_lens /*[in]*/, int64_t stride_block /*[in]*/,
    int64_t stride_n /*[in]*/, int64_t block_size /*[in]*/
) {
  // For block_size == 1, handle as special case
  if (block_size == 1) {
    if (stride_block == 1) {
      return block_sparse_indices;
    } else {
      return block_sparse_indices * stride_block;
    }
  }

  // Check input tensors are on CUDA and have correct dtype
  ASSERT_VALID_RUNTIME(block_sparse_indices.device().is_cuda(),
                       "block_sparse_indices must be on CUDA device");
  ASSERT_VALID_RUNTIME(
      block_sparse_indices.scalar_type() == GetScalarTypeFromString("int32"),
      "block_sparse_indices must be int32");
  ASSERT_VALID_RUNTIME(
      block_sparse_indptr.scalar_type() == GetScalarTypeFromString("int32"),
      "block_sparse_indptr must be int32");
  ASSERT_VALID_RUNTIME(
      vector_sparse_offsets.scalar_type() == GetScalarTypeFromString("int32"),
      "vector_sparse_offsets must be int32");
  ASSERT_VALID_RUNTIME(
      vector_sparse_indptr.scalar_type() == GetScalarTypeFromString("int32"),
      "vector_sparse_indptr must be int32");
  ASSERT_VALID_RUNTIME(
      kv_lens.scalar_type() == GetScalarTypeFromString("int32"),
      "kv_lens must be int32");

  // Get batch size from indptr
  int64_t batch_size = block_sparse_indptr.size(0) - 1;

  // Call FlashInfer's block_sparse_indices_to_vector_sparse_offsets
  block_sparse_indices_to_vector_sparse_offsets(
      block_sparse_indices, block_sparse_indptr, vector_sparse_offsets,
      vector_sparse_indptr, kv_lens, stride_block, stride_n, batch_size,
      block_size);

  return vector_sparse_offsets;
}
//==============================================================================
torch::Tensor GetAlibiSlopesBuf(int64_t num_heads /*[in]*/,
                                torch::Device device /*[in]*/
) {
  // Calculate n as the largest power of 2 less than or equal to num_heads
  int64_t n = 1 << static_cast<int>(std::log2(num_heads));

  // Calculate m_0 and create tensor m
  double m_0 = std::pow(2.0, -8.0 / n);
  auto m = torch::pow(m_0, torch::arange(1, n + 1, device));

  // If n < num_heads, calculate additional slopes
  if (n < num_heads) {
    double m_n = std::pow(2.0, -8.0 / (n + 1));
    auto m_n_tensor = torch::pow(m_n, torch::arange(1, n + 2, device));
    m = torch::cat({m, m_n_tensor}, 0);
  }

  return m.to(torch::kFloat32);
}
//==============================================================================
torch::Tensor GetCacheAlibiSlopesBuf(int64_t num_qo_heads /*[in]*/,
                                     torch::Device device /*[in]*/
) {
  static std::unordered_map<int64_t, torch::Tensor> cache_buf;

  if (cache_buf.find(num_qo_heads) == cache_buf.end()) {
    cache_buf[num_qo_heads] = GetAlibiSlopesBuf(num_qo_heads, device);
  }
  return cache_buf[num_qo_heads];
}
//==============================================================================

torch::Tensor TopKTopPSamplingFromLogits(const torch::Tensor& logits,
                                         const torch::Tensor& top_k_tensor,
                                         const torch::Tensor& top_p_tensor) {
  // Check input tensors are on CUDA and have correct dtype
  ASSERT_VALID_RUNTIME(logits.device().is_cuda(),
                       "logits must be on CUDA device");
  ASSERT_VALID_RUNTIME(
      logits.scalar_type() == GetScalarTypeFromString("float16"),
      "logits must be float16");
  ASSERT_VALID_RUNTIME(
      top_k_tensor.scalar_type() == GetScalarTypeFromString("int32"),
      "top_k_tensor must be int32")
  ASSERT_VALID_RUNTIME(top_p_tensor.scalar_type() == torch::kFloat32,
                       "top_p_tensor must be float32");

  // Get batch size from logits
  int64_t batch_size = logits.size(0);

  // Prepare output tensor
  auto output = torch::empty(
      {batch_size}, torch::dtype(torch::kInt32).device(logits.device()));

  // Prepare top_k and top_p tensors
  auto top_k_arr = top_k_tensor.to(logits.device());
  auto top_p_arr = top_p_tensor.to(logits.device());

  // STEP 1: Apply top-k masking to logits
  auto logits_f32 = logits.to(torch::kFloat32).to(logits.device()).contiguous();
  auto masked_logits = torch::empty_like(logits_f32);
  top_k_mask_logits(logits_f32, masked_logits, top_k_arr, 0);

  // STEP 2: Convert masked logits to probabilities using softmax
  auto probs = torch::softmax(masked_logits, -1).contiguous();

  // STEP 3: Apply top-p sampling on the masked probabilities
  top_p_sampling_from_probs(probs,         // probabilities
                            output,        // output tensor
                            std::nullopt,  // indices (None)
                            top_p_arr,     // top_p tensor
                            0.0,           // scalar top_p value not used
                            true,          // deterministic = true
                            std::nullopt   // generator = None
  );

  return output;
}
//==============================================================================
}  // namespace vajra::flashinfer
//==============================================================================
