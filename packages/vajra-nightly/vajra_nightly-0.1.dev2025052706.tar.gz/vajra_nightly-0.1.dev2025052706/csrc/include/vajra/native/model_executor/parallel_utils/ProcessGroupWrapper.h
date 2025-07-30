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
//==============================================================================
namespace vajra {
//==============================================================================
class ProcessGroupWrapper : public NonCopyableNonMovable {
 public:
  ProcessGroupWrapper(
      c10::intrusive_ptr<c10d::ProcessGroup>
          tensor_model_parallel_group /*[in]*/,
      c10::intrusive_ptr<c10d::ProcessGroup>
          pipeline_model_parallel_group /*[in]*/,
      c10::intrusive_ptr<c10d::ProcessGroup> kv_parallel_group /*[in]*/);

  [[nodiscard]] c10::intrusive_ptr<c10d::ProcessGroup>
  GetTensorModelParallelGroup() const;
  [[nodiscard]] c10::intrusive_ptr<c10d::ProcessGroup>
  GetPipelineModelParallelGroup() const;
  [[nodiscard]] c10::intrusive_ptr<c10d::ProcessGroup> GetKvParallelGroup()
      const;

  /**
   * @brief Get the rank of the previous stage in the pipeline
   * @return The rank of the previous pipeline stage
   */
  [[nodiscard]] int GetPipelineModelParallelPrevRank() const;

  /**
   * @brief Get the rank of the next stage in the pipeline
   * @return The rank of the next pipeline stage
   */
  [[nodiscard]] int GetPipelineModelParallelNextRank() const;

  /**
   * @brief Check if the current process is in the first pipeline stage
   * @return True if in the first pipeline model-parallel stage, False otherwise
   */
  [[nodiscard]] bool IsPipelineFirstStage() const;

  /**
   * @brief Check if the current process is in the last pipeline stage
   * @return True if in the last pipeline model-parallel stage, False otherwise
   */
  [[nodiscard]] bool IsPipelineLastStage() const;

 private:
  const c10::intrusive_ptr<c10d::ProcessGroup> tensor_model_parallel_group_;
  const c10::intrusive_ptr<c10d::ProcessGroup> pipeline_model_parallel_group_;
  const c10::intrusive_ptr<c10d::ProcessGroup> kv_parallel_group_;
};
//==============================================================================
using ProcessGroupWrapperPtr = std::shared_ptr<const ProcessGroupWrapper>;
//==============================================================================
}  // namespace vajra
//==============================================================================
