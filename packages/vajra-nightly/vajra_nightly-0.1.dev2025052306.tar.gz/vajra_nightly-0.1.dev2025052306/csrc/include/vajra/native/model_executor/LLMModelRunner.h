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
#include "commons/TorchCommon.h"
#include "native/metrics_store/CpuTimer.h"
#include "native/metrics_store/MetricType.h"
#include "native/model_executor/BaseModelRunner.h"
#include "native/model_executor/Utils.h"
#include "native/model_executor/layers/Sampler.h"
#include "native/model_executor/layers/attention/AttentionWrapper.h"
#include "native/model_executor/parallel_utils/ParallelOps.h"
#include "native/utils/CUDAUtils.h"
#include "native/utils/TorchUtils.h"
//==============================================================================
namespace vajra {
//==============================================================================
class LLMModelRunner : public BaseModelRunner {
 public:
  LLMModelRunner(std::shared_ptr<BaseReplicaControllerConfig> config /*[in]*/,
                 torch::Device device /*[in]*/, std::size_t rank /*[in]*/,
                 BaseModelPtr model /*[in]*/,
                 ProcessGroupWrapperPtr process_group_wrapper /*[in]*/,
                 WorkerMetricsStorePtr worker_metrics_store /*[in]*/,
                 SamplerPtr sampler /*[in]*/
  );

  ~LLMModelRunner() override = default;

  [[nodiscard]] PreparedInputs PrepareInputs(
      const Sequences& seqs /*[in]*/,
      const SequenceMetadataVector& seq_metadata_list /*[in]*/
  ) const override;

  [[nodiscard]] SamplerOutputs Run(
      const Sequences& seqs /*[in]*/,
      const SequenceMetadataVector& seq_metadata_list /*[in]*/,
      std::vector<torch::Tensor>& gpu_caches /*[inout]*/
      ) override;

 private:
  const SamplerPtr sampler_;
  const bool is_pipeline_first_stage_;
  const bool is_pipeline_last_stage_;
  const c10::cuda::CUDAStream send_stream_;
  const c10::cuda::CUDAStream recv_stream_;

  // CPU Timers
  CpuTimer prepare_inputs_timer_;
  CpuTimer sampler_timer_;
  CpuTimer model_execution_timer_;
  CpuTimer attn_begin_forward_timer_;
};
//==============================================================================
using LLMModelRunnerPtr = std::shared_ptr<LLMModelRunner>;
//==============================================================================
}  // namespace vajra
//==============================================================================
