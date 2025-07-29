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
#include <gtest/gtest.h>
//==============================================================================
#include "commons/TorchCommon.h"
#include "native/transfer_engine/backend/TransferEngineUtils.h"
//==============================================================================
namespace vajra {
namespace {

class TransferEngineUtilsTest : public ::testing::Test {
 protected:
  void SetUp() override {}
};

TEST_F(TransferEngineUtilsTest,
       GatherSplitTensorAlongLastDimValidSplitAllPages) {
  std::vector<std::vector<int64_t>> tensor_shapes = {
      {2, 2, 4, 8, 128},
      {1, 2, 5, 12, 128},
      {3, 2, 2, 7, 128},
      {4, 2, 6, 16, 128},
      {1, 2, 1, 2, 128}  // minimal case
  };
  std::vector<std::size_t> num_splits = {2, 4, 8, 16, 32};

  auto opts = torch::TensorOptions().device(torch::kCUDA, 0);
  for (std::size_t i = 0; i < tensor_shapes.size(); ++i) {
    torch::Tensor page_tensor =
        torch::arange(
            torch::prod(torch::tensor(tensor_shapes[i])).item<int64_t>(), opts)
            .reshape(tensor_shapes[i]);
    std::size_t num_split = num_splits[i];

    std::vector<std::size_t> page_list;
    for (auto j = 0; j < tensor_shapes[i][0]; ++j) {
      page_list.push_back(j);
    }

    std::vector<std::vector<torch::Tensor>> gathered_tensors =
        TransferEngineUtils::GatherMaybeSplitTensorAlongLastDim(
            page_tensor, page_list, num_split, true);
    ASSERT_EQ(gathered_tensors.size(), num_split) << "Test case: " << i;
    ASSERT_EQ(gathered_tensors[0].size(), 1) << "Test case: " << i;

    std::vector<int64_t> expected_shape = tensor_shapes[i];
    expected_shape[4] = expected_shape[4] / num_split;

    for (std::size_t j = 0; j < num_split; ++j) {
      ASSERT_TRUE(gathered_tensors[j][0].is_contiguous())
          << "Gathered tensor is not contiguous for test case: " << i;
      ASSERT_TRUE(gathered_tensors[j][0].sizes().vec() == expected_shape)
          << "Gathered tensor has incorrect shape in test case: " << i
          << " Expected: " << expected_shape
          << " Got: " << gathered_tensors[j][0].sizes().vec();
      ASSERT_TRUE(gathered_tensors[j][0].is_cuda())
          << "Tensors must all be on CUDA!";
      ASSERT_TRUE(gathered_tensors[j][0].device().index() ==
                  page_tensor.device().index())
          << "Mismatched device index for copy pages cache, must "
             "be on same device!";
    }
  }
}

TEST_F(TransferEngineUtilsTest,
       GatherSplitTensorAlongLastDimValidSplitPartialPages) {
  std::vector<std::vector<int64_t>> tensor_shapes = {{2, 2, 4, 8, 128},
                                                     {4, 2, 5, 12, 128},
                                                     {8, 2, 2, 7, 128},
                                                     {16, 2, 6, 16, 128},
                                                     {132, 2, 1, 2, 128}};
  std::vector<std::size_t> num_splits = {2, 4, 8, 16, 32};
  std::vector<std::vector<std::size_t>> page_lists = {
      {0}, {1, 3}, {0, 2, 4, 6}, {1, 3, 5, 7, 9, 11, 13, 15}, {0, 31}};

  for (std::size_t i = 0; i < tensor_shapes.size(); ++i) {
    auto opts = torch::TensorOptions().device(torch::kCUDA, 0);
    torch::Tensor page_tensor =
        torch::arange(
            torch::prod(torch::tensor(tensor_shapes[i])).item<int64_t>(), opts)
            .reshape(tensor_shapes[i]);
    std::size_t num_split = num_splits[i];
    std::vector<std::size_t> page_list = page_lists[i];

    std::vector<std::vector<torch::Tensor>> gathered_tensors =
        TransferEngineUtils::GatherMaybeSplitTensorAlongLastDim(
            page_tensor, page_list, num_split, true);
    ASSERT_EQ(gathered_tensors.size(), num_split) << "Test case: " << i;
    ASSERT_EQ(gathered_tensors[0].size(), 1) << "Test case: " << i;

    // Expected shape changes based on how many pages we gather
    std::vector<int64_t> expected_shape = tensor_shapes[i];
    expected_shape[4] = expected_shape.back() / num_split;
    expected_shape[0] = page_list.size();
    for (std::size_t j = 0; j < num_split; ++j) {
      ASSERT_TRUE(gathered_tensors[j].size() == 1)
          << "Should only be 1 tensor in each split tensor for test case: " << i
          << " At split num: " << j
          << " Got num tensors: " << gathered_tensors[j].size();
      ASSERT_TRUE(gathered_tensors[j][0].is_contiguous())
          << "Gathered tensor is not contiguous for test case: " << i;
      ASSERT_TRUE(gathered_tensors[j][0].sizes().vec() == expected_shape)
          << "Gathered tensor has incorrect shape in test case: " << i
          << " Expected: " << expected_shape
          << " Got: " << gathered_tensors[j][0].sizes().vec();
      ASSERT_TRUE(gathered_tensors[j][0].is_cuda())
          << "Tensors must all be on CUDA!";
      ASSERT_TRUE(gathered_tensors[j][0].device().index() ==
                  page_tensor.device().index())
          << "Mismatched device index for copy pages cache, must "
             "be on same device!";
    }
  }
}

TEST_F(TransferEngineUtilsTest,
       GatherSplitTensorAlongLastDimValidSplitPartialPagesCorrectness) {
  std::vector<std::vector<int64_t>> tensor_shapes = {{2, 2, 1, 1, 128}};
  std::vector<std::vector<int64_t>> expected_shape_before_split = {
      {1, 2, 1, 1, 128}};
  std::vector<std::size_t> num_splits = {2};
  std::vector<std::vector<std::size_t>> page_lists = {{0}};

  auto opts = torch::TensorOptions().device(torch::kCUDA, 0);
  torch::Tensor page_tensor =
      torch::arange(
          torch::prod(torch::tensor(tensor_shapes[0])).item<int64_t>(), opts)
          .reshape(tensor_shapes[0]);
  std::size_t num_split = num_splits[0];
  std::vector<std::size_t> page_list = page_lists[0];

  std::vector<std::vector<torch::Tensor>> gathered_tensors =
      TransferEngineUtils::GatherMaybeSplitTensorAlongLastDim(
          page_tensor, page_list, num_split, true);
  ASSERT_EQ(gathered_tensors.size(), num_split);
  ASSERT_EQ(gathered_tensors[0].size(), 1);

  // Expected shape changes based on how many pages we gather
  std::vector<int64_t> expected_shape = tensor_shapes[0];
  expected_shape[4] = expected_shape.back() / num_split;
  expected_shape[0] = page_list.size();
  torch::Tensor expected_tensor =
      torch::arange(torch::prod(torch::tensor(expected_shape_before_split[0]))
                        .item<int64_t>(),
                    opts)
          .reshape(expected_shape_before_split[0]);
  auto expected_split_tensors = expected_tensor.chunk(num_split, -1);
  for (std::size_t i = 0; i < num_split; ++i) {
    ASSERT_TRUE(
        torch::allclose(gathered_tensors[i][0], expected_split_tensors[i]));
    ASSERT_TRUE(gathered_tensors[i][0].is_contiguous());
    ASSERT_TRUE(gathered_tensors[i][0].sizes().vec() == expected_shape);
    ASSERT_TRUE(gathered_tensors[i][0].is_cuda())
        << "Tensors must all be on CUDA!";
    ASSERT_TRUE(gathered_tensors[i][0].device().index() ==
                page_tensor.device().index())
        << "Mismatched device index for copy pages cache, must "
           "be on same device!";
  }
}

TEST_F(TransferEngineUtilsTest, GatherSplitTensorAlongLastDimInvalidSplit) {
  std::vector<std::vector<int64_t>> tensor_shapes = {
      {2, 2, 4, 8, 128}, {50, 2, 5, 12, 128}, {100, 2, 2, 7, 128}};
  std::vector<std::size_t> num_splits = {3, 6, 9};
  std::vector<std::vector<std::size_t>> page_lists = {
      {0},
      {1, 3},
      {0, 2, 4, 6},
  };

  auto opts = torch::TensorOptions().device(torch::kCUDA, 0);
  for (std::size_t i = 0; i < tensor_shapes.size(); ++i) {
    torch::Tensor page_tensor =
        torch::arange(
            torch::prod(torch::tensor(tensor_shapes[i])).item<int64_t>(), opts)
            .reshape(tensor_shapes[i]);
    std::size_t num_split = num_splits[i];
    std::vector<std::size_t> page_list = page_lists[i];
    EXPECT_THROW(TransferEngineUtils::GatherMaybeSplitTensorAlongLastDim(
                     page_tensor, page_list, num_split, true),
                 std::invalid_argument);
  }
}

TEST_F(TransferEngineUtilsTest, GatherSplitTensorAlongLastDimInvalidPageList) {
  std::vector<std::vector<int64_t>> tensor_shapes = {
      {2, 2, 4, 8, 128}, {1, 2, 5, 12, 128}, {3, 2, 2, 7, 128}};
  std::vector<std::size_t> num_splits = {2, 4, 8};
  std::vector<std::vector<std::size_t>> page_lists = {
      {0, 2},
      {1, 4},
      {0, 9},
  };
  auto opts = torch::TensorOptions().device(torch::kCUDA, 0);

  for (std::size_t i = 0; i < tensor_shapes.size(); ++i) {
    torch::Tensor page_tensor =
        torch::arange(
            torch::prod(torch::tensor(tensor_shapes[i])).item<int64_t>(), opts)
            .reshape(tensor_shapes[i]);
    std::size_t num_split = num_splits[i];
    std::vector<std::size_t> page_list = page_lists[i];
    EXPECT_THROW(TransferEngineUtils::GatherMaybeSplitTensorAlongLastDim(
                     page_tensor, page_list, num_split, true),
                 std::invalid_argument);
  }
}
}  // namespace
}  // namespace vajra
