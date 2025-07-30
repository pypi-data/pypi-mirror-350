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
#include "native/datatypes/StepMicrobatchOutputs.h"
#include "native/worker/BaseLLMWorker.h"
//==============================================================================
namespace vajra {
//==============================================================================
class PipelineParallelLLMWorker : public BaseLLMWorker {
 public:
  PipelineParallelLLMWorker() = delete;

  PipelineParallelLLMWorker(
      ReplicaId replica_id /*[in]*/, std::size_t rank /*[in]*/,
      ZmqSocketPtr enqueue_socket /*[in]*/, ZmqSocketPtr output_socket /*[in]*/,
      WorkerSequenceManagerPtr worker_sequence_manager /*[in]*/,
      WorkerMetricsStorePtr worker_metrics_store /*[in]*/,
      BaseModelRunnerPtr model_runner /*[in]*/,
      std::vector<torch::Tensor> gpu_caches /*[in]*/,
      ProcessGroupWrapperPtr process_group_wrapper /*[in]*/,
      ZmqSocketPtr microbatch_socket /*[in]*/
  );

  ~PipelineParallelLLMWorker() override = default;

  void ExecutionLoop() override;

  void OnStepCompleted(SchedulerOutputPtr scheduler_output /*[in]*/,
                       const SamplerOutputs& sampler_outputs /*[in]*/
                       ) override;

 private:
  ZmqSocketPtr microbatch_socket_;
};
//==============================================================================
using PipelineParallelLLMWorkerPtr = std::shared_ptr<PipelineParallelLLMWorker>;
//==============================================================================
}  // namespace vajra
//==============================================================================
