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
#include "native/model_executor/layers/attention/flashinfer/BatchPrefillWithPagedKVCacheWrapper.h"
//==============================================================================
namespace vajra::flashinfer {
//==============================================================================
BatchPrefillWithPagedKVCacheWrapper::BatchPrefillWithPagedKVCacheWrapper(
    torch::Tensor float_workspace_buffer /*[in]*/,
    std::string kv_layout /*[in]*/, std::string backend /*[in]*/
    )
    : float_workspace_buffer_(float_workspace_buffer),
      kv_layout_(kv_layout),
      backend_(backend),
      use_cuda_graph_(false),
      causal_(false),
      pos_encoding_mode_("NONE"),
      use_fp16_qk_reduction_(false),
      window_left_(-1),
      logits_soft_cap_(0.0),
      rope_scale_(1.0),
      rope_theta_(10000.0),
      device_(float_workspace_buffer.device()),
      fixed_batch_size_(0) {
  // Initialize FA3 backend specific buffers
  if (backend_ == "auto" || backend_ == "fa3") {
    vector_sparse_indices_buffer_ = torch::empty(
        {16 * 1024 * 1024}, torch::dtype(torch::kInt32).device(device_));
    vector_sparse_indptr_buffer_ =
        torch::empty({32768}, torch::dtype(torch::kInt32).device(device_));
  }

  // Initialize workspace buffers
  kv_lens_buffer_ =
      torch::empty({32768}, torch::dtype(torch::kInt32).device(device_));
  int_workspace_buffer_ = torch::empty(
      {8 * 1024 * 1024}, torch::dtype(torch::kUInt8).device(device_));
  pin_memory_int_workspace_buffer_ =
      torch::empty(int_workspace_buffer_.sizes(),
                   torch::dtype(int_workspace_buffer_.scalar_type())
                       .device(torch::kCPU)
                       .pinned_memory(true));

  // Initialize max_total_num_rows_ to std::nullopt
  max_total_num_rows_ = std::nullopt;

  // Initialize plan_info_ tensor
  plan_info_ = torch::empty({0}, torch::dtype(torch::kInt32).device(device_));
}
//==============================================================================
void BatchPrefillWithPagedKVCacheWrapper::Plan(
    const torch::Tensor& qo_indptr /*[in]*/,
    const torch::Tensor& paged_kv_indptr /*[in]*/,
    const torch::Tensor& paged_kv_indices /*[in]*/,
    const torch::Tensor& paged_kv_last_page_len /*[in]*/,
    int64_t num_qo_heads /*[in]*/, int64_t num_kv_heads /*[in]*/,
    int64_t head_dim_qk /*[in]*/, int64_t page_size /*[in]*/,
    bool non_blocking /*[in]*/, bool causal /*[in]*/,
    std::optional<int64_t> head_dim_vo /*[in]*/,
    std::optional<torch::Tensor> custom_mask /*[in]*/,
    std::optional<torch::Tensor> packed_custom_mask /*[inout]*/,
    const std::string& pos_encoding_mode /*[in]*/,
    bool use_fp16_qk_reduction /*[in]*/,
    std::optional<double> sm_scale /*[in]*/, int64_t window_left /*[in]*/,
    std::optional<double> logits_soft_cap /*[in]*/,
    std::optional<double> rope_scale /*[in]*/,
    std::optional<double> rope_theta /*[in]*/,
    const std::string& q_data_type /*[in]*/,
    std::optional<std::string> kv_data_type /*[in]*/) {
  // Set data types
  cached_q_data_type_ = GetScalarTypeFromString(q_data_type);
  if (kv_data_type.has_value()) {
    cached_kv_data_type_ = GetScalarTypeFromString(kv_data_type.value());
  } else {
    cached_kv_data_type_ = cached_q_data_type_;
  }

  if (!logits_soft_cap.has_value()) {
    logits_soft_cap = 0.0;
  }

  if (!head_dim_vo.has_value()) {
    head_dim_vo = head_dim_qk;
  }

  int64_t batch_size = qo_indptr.size(0) - 1;

  torch::Tensor mask_indptr;
  if (custom_mask.has_value() || packed_custom_mask.has_value()) {
    mask_indptr = ComputePageMaskIndptr(qo_indptr, paged_kv_indptr,
                                        paged_kv_last_page_len, page_size);
  }

  if (!packed_custom_mask.has_value() && custom_mask.has_value()) {
    std::tie(packed_custom_mask, mask_indptr) = SegmentPackbits(
        custom_mask.value().contiguous().flatten(), mask_indptr, "little");
  }

  // Copy tensors to host for processing
  auto qo_indptr_host = qo_indptr.to(torch::kCPU);
  auto paged_kv_indptr_host = paged_kv_indptr.to(torch::kCPU);
  auto paged_kv_last_page_len_host = paged_kv_last_page_len.to(torch::kCPU);

  // Calculate kv_lens_arr
  auto kv_lens_arr_host =
      GetSeqLens(paged_kv_indptr_host, paged_kv_last_page_len_host, page_size);

  // Copy to kv_lens_buffer_
  kv_lens_buffer_.slice(0, 0, kv_lens_arr_host.size(0))
      .copy_(kv_lens_arr_host, non_blocking);

  // Get total number of rows
  int64_t total_num_rows = qo_indptr_host.index({-1}).item<int32_t>();

  // Copy to buffers
  qo_indptr_buf_ = qo_indptr.to(device_, non_blocking);
  paged_kv_indptr_buf_ = paged_kv_indptr.to(device_, non_blocking);
  paged_kv_indices_buf_ = paged_kv_indices.to(device_, non_blocking);
  paged_kv_last_page_len_buf_ =
      paged_kv_last_page_len.to(device_, non_blocking);

  if (packed_custom_mask.has_value()) {
    custom_mask_buf_ = packed_custom_mask.value().to(device_, non_blocking);
    mask_indptr_buf_ = mask_indptr.to(device_, non_blocking);
  } else {
    custom_mask_buf_.reset();
    mask_indptr_buf_.reset();
  }

  if (backend_ == "auto") {
    backend_ = DetermineAttentionBackend(
        device_, PosEncodingMode::FromString(pos_encoding_mode),
        use_fp16_qk_reduction, custom_mask_buf_.has_value(),
        cached_q_data_type_, cached_kv_data_type_);
  }

  bool use_sm90 = backend_ == "fa3";

  // Prepare head_dim_vo if not provided
  int64_t head_dim_v = head_dim_vo.value_or(head_dim_qk);

  // Handle FA3 backend specific processing
  if (backend_ == "fa3" && page_size != 1) {
    // Convert block sparse indices to vector sparse offsets
    auto vector_sparse_indptr_host = torch::cat(
        {torch::tensor(
             {0},
             torch::dtype(torch::kInt32).device(kv_lens_arr_host.device())),
         torch::cumsum(kv_lens_arr_host, 0, torch::kInt32)},
        0);

    // Copy to buffer
    vector_sparse_indptr_buffer_.slice(0, 0, vector_sparse_indptr_host.size(0))
        .copy_(vector_sparse_indptr_host, non_blocking);

    paged_kv_indptr_host = vector_sparse_indptr_host;
  }

  // Call the appropriate plan function based on compute capability
  if (use_sm90) {
    plan_info_ = BatchPrefillWithKVCacheSM90Plan(
        float_workspace_buffer_, int_workspace_buffer_,
        pin_memory_int_workspace_buffer_, qo_indptr_host, paged_kv_indptr_host,
        kv_lens_arr_host,
        (max_total_num_rows_.has_value() && max_total_num_rows_.value())
            ? max_total_num_rows_.value()
            : total_num_rows,
        batch_size, num_qo_heads, num_kv_heads, page_size, use_cuda_graph_,
        head_dim_qk, head_dim_v, causal);
  } else {
    plan_info_ = BatchPrefillWithKVCachePlan(
        float_workspace_buffer_, int_workspace_buffer_,
        pin_memory_int_workspace_buffer_, qo_indptr_host, paged_kv_indptr_host,
        kv_lens_arr_host,
        (max_total_num_rows_.has_value() && max_total_num_rows_.value())
            ? max_total_num_rows_.value()
            : total_num_rows,
        batch_size, num_qo_heads, num_kv_heads, page_size, use_cuda_graph_,
        head_dim_qk, head_dim_v, causal);
  }

  // Save configuration parameters
  causal_ = causal;
  pos_encoding_mode_ = pos_encoding_mode;
  use_fp16_qk_reduction_ = use_fp16_qk_reduction;
  window_left_ = window_left;
  logits_soft_cap_ = logits_soft_cap;
  sm_scale_ = sm_scale;
  rope_scale_ = rope_scale;
  rope_theta_ = rope_theta;
}
//==============================================================================
RunOutput BatchPrefillWithPagedKVCacheWrapper::Run(
    const torch::Tensor& q /*[in]*/, const KVTensor& paged_kv_cache /*[in]*/,
    std::optional<double> k_scale /*[in]*/,
    std::optional<double> v_scale /*[in]*/,
    std::optional<torch::Tensor> out /*[out]*/,
    std::optional<torch::Tensor> lse /*[out]*/, bool return_lse /*[in]*/
) {
  // Unpack paged KV cache
  torch::Tensor k_cache, v_cache;
  std::tie(k_cache, v_cache) = UnpackPagedKVCache(paged_kv_cache, kv_layout_);

  // Check data types
  CheckCachedQKVDataType(q, k_cache, cached_q_data_type_, cached_kv_data_type_);

  // Get stride information for KV cache
  int64_t stride_block = k_cache.stride(0);
  int64_t stride_n;
  int64_t page_size;

  if (kv_layout_ == "NHD") {
    page_size = k_cache.size(1);
    stride_n = k_cache.stride(1);
  } else {  // HND
    page_size = k_cache.size(2);
    stride_n = k_cache.stride(2);
  }

  // Set default values for optional parameters
  double logits_soft_cap_val = logits_soft_cap_.value_or(0.0);
  double sm_scale_val =
      sm_scale_.value_or(1.0 / std::sqrt(static_cast<double>(q.size(-1))));
  double rope_scale_val = rope_scale_.value_or(1.0);
  double rope_theta_val = rope_theta_.value_or(10000.0);

  // Apply k_scale to sm_scale if provided
  if (k_scale.has_value()) {
    sm_scale_val *= k_scale.value();
  }

  // Create or check LSE tensor if return_lse is true
  if (return_lse) {
    if (lse.has_value()) {
      // Check shape, dtype, and device
      CheckShapeDtypeAndDevice(lse.value(), {q.size(0), q.size(1)},
                               torch::kFloat32, q.device(), "lse");
    } else {
      lse = torch::empty({q.size(0), q.size(1)},
                         torch::dtype(torch::kFloat32).device(q.device()));
    }
  }

  // Create or check output tensor
  std::vector<int64_t> out_shape = q.sizes().vec();
  out_shape.back() = v_cache.size(-1);

  if (out.has_value()) {
    // Check shape, dtype, and device
    CheckShapeDtypeAndDevice(out.value(), out_shape, q.scalar_type(),
                             q.device(), "out");
  } else {
    out = torch::empty(out_shape,
                       torch::dtype(q.scalar_type()).device(q.device()));
  }

  // Determine mask mode
  MaskMode mask_mode;
  if (custom_mask_buf_.has_value()) {
    mask_mode = MaskMode::CUSTOM;
  } else if (causal_) {
    mask_mode = MaskMode::CAUSAL;
  } else {
    mask_mode = MaskMode::NON_CAUSAL;
  }

  torch::Tensor sparse_indices, sparse_indptr;
  if (backend_ == "fa3") {
    // Prepare sparse indices and indptr based on backend
    sparse_indices = BlockSparseIndicesToVectorSparseOffsets(
        paged_kv_indices_buf_, paged_kv_indptr_buf_,
        vector_sparse_indices_buffer_, vector_sparse_indptr_buffer_,
        kv_lens_buffer_, stride_block / stride_n, 1, page_size);
    sparse_indptr = vector_sparse_indptr_buffer_;
  } else {
    sparse_indices = paged_kv_indices_buf_;
    sparse_indptr = paged_kv_indptr_buf_;
  }

  // Determine if we should use SM90 kernels
  bool use_sm90 = backend_ == "fa3";

  // Create alibi slopes tensor (empty for now, not used in our implementation)
  auto alibi_slopes = GetCacheAlibiSlopesBuf(q.size(1), q.device());

  // Call the appropriate run function based on compute capability
  if (use_sm90) {
    // For SM90, we use a simplified interface that doesn't support all features
    BatchPrefillWithPagedKVCacheSM90Run(
        float_workspace_buffer_, int_workspace_buffer_, plan_info_, q, k_cache,
        v_cache, qo_indptr_buf_, sparse_indptr, sparse_indices,
        paged_kv_last_page_len_buf_, out.value(), lse, mask_mode,
        TensorLayout::FromString(kv_layout_), window_left_, logits_soft_cap_val,
        sm_scale_val);
  } else {
    // For other architectures, we use the full interface
    BatchPrefillWithPagedKVCacheRun(
        float_workspace_buffer_, int_workspace_buffer_, plan_info_, q, k_cache,
        v_cache, qo_indptr_buf_, sparse_indptr, sparse_indices,
        paged_kv_last_page_len_buf_, out.value(), lse, mask_mode,
        TensorLayout::FromString(kv_layout_), window_left_, custom_mask_buf_,
        mask_indptr_buf_, alibi_slopes, logits_soft_cap_val, sm_scale_val,
        1.0 / rope_scale_val, 1.0 / rope_theta_val);
  }

  // Apply v_scale if provided
  if (v_scale.has_value()) {
    out.value().mul_(v_scale.value());
  }

  // Return output or (output, lse) based on return_lse flag
  if (return_lse) {
    return std::make_pair(out.value(), lse.value());
  } else {
    return out.value();
  }
}
//==============================================================================
}  // namespace vajra::flashinfer
//==============================================================================
