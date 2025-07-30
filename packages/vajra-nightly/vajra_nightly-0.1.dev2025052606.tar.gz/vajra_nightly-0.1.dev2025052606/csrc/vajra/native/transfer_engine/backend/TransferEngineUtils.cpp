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
#include "native/transfer_engine/backend/TransferEngineUtils.h"

#include "commons/Logging.h"
//==============================================================================
using torch::indexing::Ellipsis;
using torch::indexing::Slice;
using vajra::TransferEngineUtils;
//==============================================================================
void TransferEngineUtils::CopyMergePagesCache(
    const std::vector<std::vector<torch::Tensor>>& src_page_tensors,
    torch::Tensor const& dst_page_tensor,
    const std::vector<std::size_t>& page_list) {
  torch::Device dst_device = dst_page_tensor.device();
  const std::size_t num_pages = page_list.size();
  const std::size_t num_src = src_page_tensors.size();
  ASSERT_VALID_ARGUMENTS(num_src > 0,
                         "Num of src page tensors must be greater than 0!");
  std::size_t dst_head_dim = dst_page_tensor.size(-1);
  std::size_t head_dim_per_src = dst_head_dim / (num_src);

  ASSERT_VALID_ARGUMENTS(dst_head_dim % (num_src) == 0,
                         "Invalid head dim for copy pages cache!");

  for (std::size_t idx = 0; idx < src_page_tensors.size(); ++idx) {
    const auto& src_page_tensor = src_page_tensors[idx][0];
    torch::Device src_device = src_page_tensor.device();
    ASSERT_VALID_ARGUMENTS(src_device.is_cuda(),
                           "Source tensors must all be on CUDA!");
    ASSERT_VALID_ARGUMENTS(src_device.index() == dst_device.index(),
                           "Mismatched device index for copy pages cache, must "
                           "be on same device!");
    for (std::size_t n = 0; n < num_pages; ++n) {
      std::size_t dst_page_number = page_list[n];
      std::size_t src_page_number = n;

      torch::Tensor src_page = src_page_tensor[src_page_number];

      dst_page_tensor
          .index({Slice(dst_page_number, dst_page_number + 1), Ellipsis,
                  Slice((idx)*head_dim_per_src, (idx + 1) * head_dim_per_src)})
          .copy_(src_page);
    }
  }
}

std::vector<std::vector<torch::Tensor>>
TransferEngineUtils::GatherSplitTensorAlongLastDim(
    const torch::Tensor& page_tensor, const std::vector<std::size_t>& page_list,
    std::size_t num_split) {
  ASSERT_VALID_ARGUMENTS(page_tensor.is_cuda(),
                         "Page tensor must be on CUDA device for GatherSplit!");
  std::size_t last_dim_size = page_tensor.size(-1);
  ASSERT_VALID_ARGUMENTS(last_dim_size % (num_split) == 0,
                         "Invalid last dim size {} for num splits {}!",
                         last_dim_size, num_split);
  auto gather_page_tensor = GatherPageTensor(page_tensor, page_list);
  auto split_page_tensors = gather_page_tensor.chunk(num_split, -1);
  std::vector<std::vector<torch::Tensor>> split_page_tensors_vec;
  for (auto& split_page_tensor : split_page_tensors) {
    ASSERT_VALID_RUNTIME(
        page_tensor.device().index() == split_page_tensor.device().index(),
        "Split page tensors should be on the same CUDA device {} as the "
        "original "
        "page tensor for GatherSplit but was on {}!",
        page_tensor.device().index(), split_page_tensor.device().index());
    split_page_tensors_vec.push_back({{split_page_tensor.contiguous()}});
  }

  return split_page_tensors_vec;
}

std::vector<std::vector<torch::Tensor>>
TransferEngineUtils::GatherMaybeSplitTensorAlongLastDim(
    const torch::Tensor& page_tensor, const std::vector<std::size_t>& page_list,
    std::size_t num_gather, bool split_along_last_dim) {
  if (split_along_last_dim) {
    return GatherSplitTensorAlongLastDim(page_tensor, page_list, num_gather);
  } else {
    auto gather_page_tensor = GatherPageTensor(page_tensor, page_list);
    std::vector<std::vector<torch::Tensor>> gather_page_tensors;
    for (std::size_t i = 0; i < num_gather; i++) {
      gather_page_tensors.push_back({{gather_page_tensor}});
    }
    return gather_page_tensors;
  }
}

torch::Tensor TransferEngineUtils::GatherPageTensor(
    const torch::Tensor& page_tensor,
    const std::vector<std::size_t>& page_list) {
  std::vector<int64_t> gather_page_list;
  for (std::size_t i = 0; i < page_list.size(); ++i) {
    ASSERT_VALID_ARGUMENTS(
        static_cast<int64_t>(page_list[i]) < page_tensor.size(0),
        "Invalid page list index {} for page tensor size {}!", page_list[i],
        page_tensor.size(0));
    gather_page_list.push_back(static_cast<int64_t>(page_list[i]));
  }
  auto opts = torch::TensorOptions().dtype(torch::kInt64);
  auto page_list_tensor =
      torch::from_blob(gather_page_list.data(),
                       {static_cast<int64_t>(gather_page_list.size())}, opts)
          .clone();
  torch::Tensor page_list_tensor_gpu = page_list_tensor.to(
      torch::Device(torch::kCUDA, page_tensor.device().index()));

  auto gathered_page_tensor =
      torch::index_select(page_tensor, 0, page_list_tensor_gpu);
  return gathered_page_tensor;
}

std::vector<std::vector<torch::Tensor>>
TransferEngineUtils::PreparePageTensorBuffers(
    const torch::Tensor& page_tensor, const std::vector<std::size_t>& page_list,
    std::size_t num_recv) {
  std::vector<std::vector<torch::Tensor>> recv_buffers;
  ASSERT_VALID_ARGUMENTS(
      !page_list.empty(),
      "Page list is empty when calling to prepare page tensor buffers!");
  ASSERT_VALID_ARGUMENTS(
      page_tensor.is_cuda(),
      "Page tensor must be on CUDA device for PreparePageTensorBuffers!");
  for (std::size_t i = 0; i < num_recv; i++) {
    auto page_tensor_shape = page_tensor.sizes();
    torch::ScalarType page_tensor_dtype = page_tensor.dtype().toScalarType();

    auto opts = torch::TensorOptions()
                    .dtype(page_tensor_dtype)
                    .device(page_tensor.device());

    std::vector<int64_t> new_shape = {static_cast<int64_t>(
        page_list.size())};  // needs to be int64_t for torch
    new_shape.insert(new_shape.end(), page_tensor_shape.begin() + 1,
                     page_tensor_shape.end());
    // hidden dim is split across the recv tensors
    new_shape.back() /= num_recv;

    torch::Tensor zeros_tensor = torch::zeros(new_shape, opts);

    // Reshape the zeros tensor into a vector of vectors of tensors.
    recv_buffers.push_back({zeros_tensor});
  }

  return recv_buffers;
}
