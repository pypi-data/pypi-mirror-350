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
#include "native/configs/ReplicaControllerConfig.h"
#include "native/datatypes/SamplerOutput.h"
#include "native/datatypes/Sequence.h"
#include "native/datatypes/SequenceMetadata.h"
#include "native/metrics_store/WorkerMetricsStore.h"
#include "native/model_executor/models/BaseModel.h"
#include "native/model_executor/parallel_utils/ProcessGroupWrapper.h"
//==============================================================================
namespace vajra {
//==============================================================================
using PreparedInputs = std::pair<torch::Tensor, torch::Tensor>;
//==============================================================================
class BaseModelRunner : public NonCopyableNonMovable {
 public:
  BaseModelRunner(std::shared_ptr<BaseReplicaControllerConfig> config /*[in]*/,
                  torch::Device device /*[in]*/, std::size_t rank /*[in]*/,
                  BaseModelPtr model /*[in]*/,
                  ProcessGroupWrapperPtr process_group_wrapper /*[in]*/,
                  WorkerMetricsStorePtr worker_metrics_store /*[in]*/
                  )
      : config_(config),
        device_(device),
        rank_(rank),
        model_(model),
        process_group_wrapper_(process_group_wrapper),
        worker_metrics_store_(worker_metrics_store) {
    ASSERT_VALID_POINTER_ARGUMENT(config);
    ASSERT_VALID_POINTER_ARGUMENT(model);
    ASSERT_VALID_POINTER_ARGUMENT(process_group_wrapper);
    ASSERT_VALID_POINTER_ARGUMENT(worker_metrics_store);
  }

  virtual ~BaseModelRunner() = default;

  virtual PreparedInputs PrepareInputs(
      const Sequences& seqs /*[in]*/,
      const SequenceMetadataVector& seq_metadata_list /*[in]*/
  ) const = 0;

  virtual SamplerOutputs Run(
      const Sequences& seqs /*[in]*/,
      const SequenceMetadataVector& seq_metadata_list /*[in]*/,
      std::vector<torch::Tensor>& gpu_caches /*[inout]*/
      ) = 0;

 protected:
  const std::shared_ptr<BaseReplicaControllerConfig> config_;
  const torch::Device device_;
  const std::size_t rank_;
  const BaseModelPtr model_;
  const ProcessGroupWrapperPtr process_group_wrapper_;
  const WorkerMetricsStorePtr worker_metrics_store_;
};
//==============================================================================
using BaseModelRunnerPtr = std::shared_ptr<BaseModelRunner>;
//==============================================================================
}  // namespace vajra
//==============================================================================
