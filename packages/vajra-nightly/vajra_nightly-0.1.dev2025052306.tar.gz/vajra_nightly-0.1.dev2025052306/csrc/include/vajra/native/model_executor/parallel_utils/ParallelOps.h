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
#include "native/model_executor/parallel_utils/ProcessGroupWrapper.h"
//==============================================================================
namespace vajra {
//==============================================================================
class ParallelOps : public StaticClass {
 public:
  [[nodiscard]] static std::vector<torch::Tensor> SplitTensorAlongLastDim(
      const torch::Tensor& input /*[in]*/, int64_t num_partitions /*[in]*/,
      bool contiguous_split_chunks = false /*[in]*/
  );

  [[nodiscard]] static torch::Tensor ReduceFromCacheModelParallelRegion(
      torch::Tensor& input /*[inout]*/,
      const c10::intrusive_ptr<c10d::ProcessGroup>& process_group /*[in]*/
  );

  [[nodiscard]] static torch::Tensor ReduceFromTensorModelParallelRegion(
      torch::Tensor& input /*[inout]*/,
      const c10::intrusive_ptr<c10d::ProcessGroup>& process_group /*[in]*/
  );

  [[nodiscard]] static torch::Tensor ScatterToTensorModelParallelRegion(
      const torch::Tensor& input /*[in]*/,
      const c10::intrusive_ptr<c10d::ProcessGroup>& process_group /*[in]*/
  );

  [[nodiscard]] static torch::Tensor GatherFromGroup(
      const torch::Tensor& input /*[in]*/, int index_rank /*[in]*/,
      int concat_dim /*[in]*/,
      const c10::intrusive_ptr<c10d::ProcessGroup>& process_group /*[in]*/
  );

  [[nodiscard]] static torch::Tensor GatherFromTensorModelParallelRegion(
      const torch::Tensor& input /*[in]*/,
      const c10::intrusive_ptr<c10d::ProcessGroup>& process_group /*[in]*/
  );

  [[nodiscard]] static torch::Tensor GatherFromCacheModelParallelRegion(
      const torch::Tensor& input /*[in]*/, int index_rank /*[in]*/,
      const c10::intrusive_ptr<c10d::ProcessGroup>& process_group /*[in]*/
  );

  static void SendToNextPipelineStage(
      const torch::Tensor& input /*[in]*/,
      ProcessGroupWrapperPtr process_group_wrapper /*[in]*/,
      bool enable_chunked_pipeline_comm_opt = true /*[in]*/
  );

  [[nodiscard]] static torch::Tensor RecvFromLastPipelineStage(
      const std::vector<int64_t>& output_size /*[in]*/,
      torch::Dtype dtype /*[in]*/, torch::Device device /*[in]*/,
      ProcessGroupWrapperPtr process_group_wrapper /*[in]*/,
      bool enable_chunked_pipeline_comm_opt = true /*[in]*/
  );
};
//==============================================================================
}  // namespace vajra
//==============================================================================
