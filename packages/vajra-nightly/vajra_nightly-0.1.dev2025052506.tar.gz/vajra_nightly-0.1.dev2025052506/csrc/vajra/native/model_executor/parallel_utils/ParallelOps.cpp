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
#include "native/model_executor/parallel_utils/ParallelOps.h"
//==============================================================================
using vajra::ParallelOps;
//==============================================================================
std::vector<torch::Tensor> ParallelOps::SplitTensorAlongLastDim(
    const torch::Tensor& input /*[in]*/, int64_t num_partitions /*[in]*/,
    bool contiguous_split_chunks /*[in]*/
) {
  int last_dim = input.dim() - 1;
  int last_dim_size = input.size(last_dim) / num_partitions;
  // Split
  auto tensor_list = torch::split(input, last_dim_size, last_dim);
  // Note: torch.split does not create contiguous tensors by default.
  if (contiguous_split_chunks) {
    for (auto& tensor : tensor_list) {
      tensor = tensor.contiguous();
    }
  }
  return tensor_list;
}
//==============================================================================
torch::Tensor ParallelOps::ReduceFromCacheModelParallelRegion(
    torch::Tensor& input /*[inout]*/,
    const c10::intrusive_ptr<c10d::ProcessGroup>& process_group /*[in]*/) {
  int world_size = process_group->getSize();
  if (world_size == 1) {
    return input;
  }

  std::vector<at::Tensor> input_vec{input};

  auto work = process_group->allreduce(input_vec, c10d::AllreduceOptions());
  work->wait();
  return input;
}
//==============================================================================
torch::Tensor ParallelOps::ReduceFromTensorModelParallelRegion(
    torch::Tensor& input /*[inout]*/,
    const c10::intrusive_ptr<c10d::ProcessGroup>& process_group /*[in]*/) {
  int world_size = process_group->getSize();
  if (world_size == 1) {
    return input;
  }

  std::vector<at::Tensor> input_vec{input};

  auto work = process_group->allreduce(input_vec, c10d::AllreduceOptions());
  work->wait();
  return input;
}
//==============================================================================
torch::Tensor ParallelOps::ScatterToTensorModelParallelRegion(
    const torch::Tensor& input /*[in]*/,
    const c10::intrusive_ptr<c10d::ProcessGroup>& process_group /*[in]*/) {
  int rank = process_group->getRank();
  int world_size = process_group->getSize();
  if (world_size == 1) {
    return input;
  }
  std::vector<at::Tensor> input_list =
      SplitTensorAlongLastDim(input, world_size, false);
  return input_list[rank].contiguous();
}
//==============================================================================
torch::Tensor ParallelOps::GatherFromGroup(
    const torch::Tensor& input /*[in]*/, int index_rank /*[in]*/,
    int concat_dim /*[in]*/,
    const c10::intrusive_ptr<c10d::ProcessGroup>& process_group /*[in]*/) {
  int world_size = process_group->getSize();

  std::vector<at::Tensor> tensor_list(world_size, torch::empty_like(input));
  tensor_list[index_rank] = input;

  std::vector<std::vector<at::Tensor>> tensor_list_vec{tensor_list};
  std::vector<at::Tensor> input_vec{input};

  auto work = process_group->allgather(tensor_list_vec, input_vec);
  work->wait();
  return torch::cat(tensor_list, concat_dim);
}
//==============================================================================
torch::Tensor ParallelOps::GatherFromTensorModelParallelRegion(
    const torch::Tensor& input /*[in]*/,
    const c10::intrusive_ptr<c10d::ProcessGroup>& process_group /*[in]*/) {
  int world_size = process_group->getSize();
  if (world_size == 1) {
    return input;
  }

  std::vector<at::Tensor> output_tensors;
  for (int i = 0; i < world_size; i++) {
    output_tensors.push_back(torch::empty_like(input));
  }

  std::vector<std::vector<at::Tensor>> output_tensors_vec{output_tensors};
  std::vector<at::Tensor> input_vec{input};

  auto work = process_group->allgather(output_tensors_vec, input_vec);
  work->wait();
  return torch::cat(output_tensors, input.dim() - 1 /*last_dim*/);
}
//==============================================================================
torch::Tensor ParallelOps::GatherFromCacheModelParallelRegion(
    const torch::Tensor& input /*[in]*/, int index_rank /*[in]*/,
    const c10::intrusive_ptr<c10d::ProcessGroup>& process_group /*[in]*/) {
  int world_size = process_group->getSize();
  if (world_size == 1) {
    return input;
  }

  return GatherFromGroup(input, index_rank, 1 /*concat_dim*/, process_group);
}
//==============================================================================
void ParallelOps::SendToNextPipelineStage(
    const torch::Tensor& input /*[in]*/,
    ProcessGroupWrapperPtr process_group_wrapper /*[in]*/,
    bool enable_chunked_pipeline_comm_opt /*[in]*/) {
  ASSERT_VALID_POINTER_ARGUMENT(process_group_wrapper);

  auto pipeline_model_parallel_group =
      process_group_wrapper->GetPipelineModelParallelGroup();
  auto tensor_model_parallel_group =
      process_group_wrapper->GetTensorModelParallelGroup();

  ASSERT_VALID_RUNTIME(
      pipeline_model_parallel_group->getSize() > 1,
      "Pipeline Model Parallel World Size must be greater than 1");

  // Get next rank in pipeline
  int dst_rank = process_group_wrapper->GetPipelineModelParallelNextRank();

  if (enable_chunked_pipeline_comm_opt) {
    // Split tensor along last dim
    int tp_world_size = tensor_model_parallel_group->getSize();
    int tp_rank = tensor_model_parallel_group->getRank();
    auto tensor_chunks = SplitTensorAlongLastDim(input, tp_world_size);

    // Send only this rank's chunk
    std::vector<at::Tensor> chunk_to_send = {
        tensor_chunks[tp_rank].contiguous()};

    auto work =
        pipeline_model_parallel_group->send(chunk_to_send, dst_rank, 0 /*tag*/);
    work->wait();
  } else {
    // No splitting needed if optimization disabled
    std::vector<at::Tensor> input_vec{input};
    auto work =
        pipeline_model_parallel_group->send(input_vec, dst_rank, 0 /*tag*/);
    work->wait();
  }
}
//==============================================================================
torch::Tensor ParallelOps::RecvFromLastPipelineStage(
    const std::vector<int64_t>& output_size /*[in]*/,
    torch::Dtype dtype /*[in]*/, torch::Device device /*[in]*/,
    ProcessGroupWrapperPtr process_group_wrapper /*[in]*/,
    bool enable_chunked_pipeline_comm_opt /*[in]*/) {
  ASSERT_VALID_POINTER_ARGUMENT(process_group_wrapper);

  auto pipeline_model_parallel_group =
      process_group_wrapper->GetPipelineModelParallelGroup();
  auto tensor_model_parallel_group =
      process_group_wrapper->GetTensorModelParallelGroup();

  ASSERT_VALID_RUNTIME(
      pipeline_model_parallel_group->getSize() > 1,
      "Pipeline Model Parallel World Size must be greater than 1");

  // Get previous rank in pipeline
  int src_rank = process_group_wrapper->GetPipelineModelParallelPrevRank();

  if (enable_chunked_pipeline_comm_opt) {
    // Get tensor model parallel world size
    int tp_world_size = tensor_model_parallel_group->getSize();

    // Calculate chunk size
    int64_t chunk_size = output_size.back() / tp_world_size;

    // Create shape tuple for the chunk tensor
    std::vector<int64_t> chunk_shape = output_size;
    chunk_shape.back() = chunk_size;

    // Create a chunk tensor to receive this rank's portion
    torch::Tensor chunk = torch::empty(
        chunk_shape, torch::TensorOptions().dtype(dtype).device(device));

    // Receive this rank's chunk
    std::vector<at::Tensor> chunk_vec{chunk};
    auto work =
        pipeline_model_parallel_group->recv(chunk_vec, src_rank, 0 /*tag*/);
    work->wait();

    // Gather all chunks from tensor model parallel group
    return GatherFromTensorModelParallelRegion(chunk,
                                               tensor_model_parallel_group);
  } else {
    // Fallback: receive full tensor directly
    torch::Tensor output = torch::empty(
        output_size, torch::TensorOptions().dtype(dtype).device(device));
    std::vector<at::Tensor> output_vec{output};
    auto work =
        pipeline_model_parallel_group->recv(output_vec, src_rank, 0 /*tag*/);
    work->wait();

    return output;
  }
}
//==============================================================================
