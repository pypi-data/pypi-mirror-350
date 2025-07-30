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
#include "native/datatypes/StepInputs.h"
#include "native/datatypes/StepOutputs.h"
#include "native/metrics_store/CpuTimer.h"
#include "native/metrics_store/MetricType.h"
#include "native/worker/BaseWorker.h"
//==============================================================================
namespace vajra {
//==============================================================================
class BaseLLMWorker : public BaseWorker {
 public:
  BaseLLMWorker() = delete;

  BaseLLMWorker(ReplicaId replica_id /*[in]*/, std::size_t rank /*[in]*/,
                ZmqSocketPtr enqueue_socket /*[in]*/,
                ZmqSocketPtr output_socket /*[in]*/,
                WorkerSequenceManagerPtr worker_sequence_manager /*[in]*/,
                WorkerMetricsStorePtr worker_metrics_store /*[in]*/,
                BaseModelRunnerPtr model_runner /*[in]*/,
                std::vector<torch::Tensor> gpu_caches /*[in]*/,
                ProcessGroupWrapperPtr process_group_wrapper /*[in]*/
  );

  ~BaseLLMWorker() override = default;

  [[nodiscard]] SamplerOutputs ExecuteModel(
      SchedulerOutputPtr scheduler_output /*[in]*/
      ) override;

  void ExecutionLoop() override;

  virtual void OnStepCompleted(SchedulerOutputPtr scheduler_output /*[in]*/,
                               const SamplerOutputs& sampler_outputs /*[in]*/
  );

 protected:
  // GPU cache
  std::vector<torch::Tensor> gpu_caches_;

  // Parallel ranks
  const int tensor_model_parallel_rank_;
  const int pipeline_model_parallel_rank_;
  const int kv_parallel_rank_;

  // Flags for checking ranks
  const bool is_tensor_parallel_rank_zero_;
  const bool is_first_pipeline_stage_;
  const bool is_last_pipeline_stage_;

  // CPU Timers
  CpuTimer on_schedule_handling_timer_;
  CpuTimer on_step_completed_handling_timer_;
};
//==============================================================================
using BaseLLMWorkerPtr = std::shared_ptr<BaseLLMWorker>;
//==============================================================================
}  // namespace vajra
//==============================================================================
