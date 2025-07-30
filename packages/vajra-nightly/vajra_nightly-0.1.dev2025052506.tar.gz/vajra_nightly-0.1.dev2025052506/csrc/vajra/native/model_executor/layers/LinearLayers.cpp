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
#include "native/model_executor/layers/LinearLayers.h"

#include "kernels/ops.h"
//==============================================================================
using vajra::ColumnParallelLinear;
using vajra::RowParallelLinear;
using vajra::VocabParallelEmbedding;
//==============================================================================
ColumnParallelLinear::ColumnParallelLinear(
    int input_size /*[in]*/, int output_size /*[in]*/,
    bool gather_output /*[in]*/, int world_size /*[in]*/,
    bool skip_bias_add /*[in]*/, const torch::Tensor& weight /*[in]*/,
    const std::optional<torch::Tensor>& bias /*[in]*/,
    ProcessGroupWrapperPtr process_group_wrapper /*[in]*/)
    : input_size_(input_size),
      output_size_(output_size),
      gather_output_(gather_output),
      world_size_(world_size),
      output_size_per_partition_(output_size / world_size),
      skip_bias_add_(skip_bias_add),
      weight_(weight),
      bias_(bias),
      process_group_(process_group_wrapper->GetTensorModelParallelGroup()) {
  ASSERT_VALID_POINTER_ARGUMENT(process_group_wrapper);
}
//==============================================================================
torch::Tensor ColumnParallelLinear::Forward(
    const torch::Tensor& input /*[in]*/) const {
  auto output_parallel = torch::linear(input, weight_, bias_);

  if (gather_output_) {
    output_parallel = ParallelOps::GatherFromTensorModelParallelRegion(
        output_parallel, process_group_);
  }

  return output_parallel;
}
//==============================================================================
RowParallelLinear::RowParallelLinear(
    int input_size /*[in]*/, int output_size /*[in]*/,
    bool input_is_parallel /*[in]*/, bool reduce_results /*[in]*/,
    int world_size /*[in]*/, int input_size_per_partition /*[in]*/,
    bool skip_bias_add /*[in]*/, const torch::Tensor& weight /*[in]*/,
    const std::optional<torch::Tensor>& bias /*[in]*/,
    ProcessGroupWrapperPtr process_group_wrapper /*[in]*/)
    : input_size_(input_size),
      output_size_(output_size),
      input_is_parallel_(input_is_parallel),
      reduce_results_(reduce_results),
      world_size_(world_size),
      input_size_per_partition_(input_size_per_partition),
      skip_bias_add_(skip_bias_add),
      weight_(weight),
      bias_(bias),
      process_group_(process_group_wrapper->GetTensorModelParallelGroup()) {
  ASSERT_VALID_POINTER_ARGUMENT(process_group_wrapper);
}
//==============================================================================
torch::Tensor RowParallelLinear::Forward(
    const torch::Tensor& input /*[in]*/) const {
  auto input_parallel = input;
  if (!input_is_parallel_) {
    input_parallel =
        ParallelOps::ScatterToTensorModelParallelRegion(input, process_group_);
  }

  auto output_parallel = torch::matmul(input_parallel, weight_.t());
  auto output = output_parallel;
  if (reduce_results_ && world_size_ > 1) {
    output = ParallelOps::ReduceFromTensorModelParallelRegion(output_parallel,
                                                              process_group_);
  }

  if (!skip_bias_add_ && bias_.has_value()) {
    output.add_(bias_.value());
  }

  return output;
}
//==============================================================================
VocabParallelEmbedding::VocabParallelEmbedding(
    int num_embeddings /*[in]*/, int embedding_dim /*[in]*/,
    int tensor_model_parallel_size /*[in]*/, int rank /*[in]*/,
    bool reduce_results /*[in]*/, int vocab_start_index /*[in]*/,
    int vocab_end_index /*[in]*/, int num_embeddings_per_partition /*[in]*/,
    const torch::Tensor& weight /*[in]*/,
    ProcessGroupWrapperPtr process_group_wrapper /*[in]*/)
    : num_embeddings_(num_embeddings),
      embedding_dim_(embedding_dim),
      tensor_model_parallel_size_(tensor_model_parallel_size),
      rank_(rank),
      reduce_results_(reduce_results),
      vocab_start_index_(vocab_start_index),
      vocab_end_index_(vocab_end_index),
      num_embeddings_per_partition_(num_embeddings_per_partition),
      weight_(weight),
      process_group_(process_group_wrapper->GetTensorModelParallelGroup()) {
  ASSERT_VALID_POINTER_ARGUMENT(process_group_wrapper);
}
//==============================================================================
torch::Tensor VocabParallelEmbedding::Forward(
    const torch::Tensor& input /*[in]*/) const {
  int world_size = process_group_->getSize();
  auto masked_input = input;

  if (world_size > 1) {
    auto input_mask =
        (input < vocab_start_index_) | (input >= vocab_end_index_);
    masked_input = input.clone() - vocab_start_index_;
    masked_input = masked_input.masked_fill_(input_mask, 0);
  }

  auto options = torch::nn::functional::EmbeddingFuncOptions()
                     .norm_type(2.0)
                     .scale_grad_by_freq(false)
                     .sparse(false);

  auto output_parallel =
      torch::nn::functional::embedding(masked_input, weight_, options);

  if (world_size > 1) {
    auto input_mask =
        (input < vocab_start_index_) | (input >= vocab_end_index_);
    output_parallel.index_put_({input_mask, torch::indexing::Ellipsis}, 0.0);
  }

  auto output = output_parallel;
  if (reduce_results_ && world_size > 1) {
    output = ParallelOps::ReduceFromTensorModelParallelRegion(output_parallel,
                                                              process_group_);
  }

  return output;
}
//==============================================================================
