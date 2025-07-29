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
#include "native/worker/BaseLLMWorker.h"
//==============================================================================
using vajra::BaseLLMWorker;
using vajra::SamplerOutputs;
//==============================================================================
BaseLLMWorker::BaseLLMWorker(
    ReplicaId replica_id /*[in]*/, std::size_t rank /*[in]*/,
    ZmqSocketPtr enqueue_socket /*[in]*/, ZmqSocketPtr output_socket /*[in]*/,
    WorkerSequenceManagerPtr worker_sequence_manager /*[in]*/,
    WorkerMetricsStorePtr worker_metrics_store /*[in]*/,
    BaseModelRunnerPtr model_runner /*[in]*/,
    std::vector<torch::Tensor> gpu_caches /*[in]*/,
    ProcessGroupWrapperPtr process_group_wrapper /*[in]*/
    )
    : BaseWorker(replica_id, rank, enqueue_socket, output_socket,
                 worker_sequence_manager, worker_metrics_store, model_runner),
      gpu_caches_(gpu_caches),
      tensor_model_parallel_rank_(
          process_group_wrapper->GetTensorModelParallelGroup()->getRank()),
      pipeline_model_parallel_rank_(
          process_group_wrapper->GetPipelineModelParallelGroup()->getRank()),
      kv_parallel_rank_(process_group_wrapper->GetKvParallelGroup()->getRank()),
      is_tensor_parallel_rank_zero_(tensor_model_parallel_rank_ == 0),
      is_first_pipeline_stage_(process_group_wrapper->IsPipelineFirstStage()),
      is_last_pipeline_stage_(process_group_wrapper->IsPipelineLastStage()),
      on_schedule_handling_timer_(MetricType::WORKER_ON_SCHEDULE_HANDLING,
                                  worker_metrics_store),
      on_step_completed_handling_timer_(
          MetricType::WORKER_ON_STEP_COMPLETE_HANDLING, worker_metrics_store) {
  ASSERT_VALID_POINTER_ARGUMENT(process_group_wrapper);
  ASSERT_VALID_POINTER_ARGUMENT(worker_sequence_manager);
  ASSERT_VALID_POINTER_ARGUMENT(worker_metrics_store);
  ASSERT_VALID_POINTER_ARGUMENT(model_runner);
  ASSERT_VALID_POINTER_ARGUMENT(enqueue_socket);
  ASSERT_VALID_POINTER_ARGUMENT(output_socket);
}

SamplerOutputs BaseLLMWorker::ExecuteModel(
    SchedulerOutputPtr scheduler_output /*[in]*/
) {
  ASSERT_VALID_POINTER_ARGUMENT(scheduler_output);

  auto batch_stage_start_time = time_utils::now_s();

  // Notify metrics store about batch stage start
  worker_metrics_store_->OnBatchStageStart(scheduler_output);

  // Handle scheduling
  std::tuple<Sequences, Sequences, SequenceMetadataVector> scheduled_outputs;
  {
    auto timer_guard = on_schedule_handling_timer_.TimeOperation();
    scheduled_outputs =
        worker_sequence_manager_->OnScheduleWorker(scheduler_output);
  }

  // Unpack scheduled outputs
  auto& [_, seqs, seq_metadata_list] = scheduled_outputs;

  // Run the model
  auto sampler_outputs =
      model_runner_->Run(seqs, seq_metadata_list, gpu_caches_);

  // Handle step completion
  {
    auto timer_guard = on_step_completed_handling_timer_.TimeOperation();
    OnStepCompleted(scheduler_output, sampler_outputs);
  }

  auto batch_stage_end_time = time_utils::now_s();

  // Notify metrics store about batch stage end
  worker_metrics_store_->OnBatchStageEnd(
      replica_id_, seq_metadata_list, tensor_model_parallel_rank_,
      pipeline_model_parallel_rank_, kv_parallel_rank_, batch_stage_start_time,
      batch_stage_end_time);

  return sampler_outputs;
}

void BaseLLMWorker::OnStepCompleted(
    SchedulerOutputPtr scheduler_output /*[in]*/,
    const SamplerOutputs& sampler_outputs /*[in]*/
) {
  ValidSamplerOutputs valid_sampler_outputs;

  // Filter out invalid sampler outputs
  for (const auto& sampler_output : sampler_outputs) {
    if (sampler_output.has_value()) {
      valid_sampler_outputs.push_back(sampler_output.value());
    }
  }

  worker_sequence_manager_->OnStepCompleted(
      scheduler_output->seq_schedule_metadata_list, valid_sampler_outputs);
}

void BaseLLMWorker::ExecutionLoop() {
  while (true) {
    auto step_inputs = ZmqHelper::Recv<StepInputs>(*enqueue_socket_);

    // Add new sequences
    for (const auto& params : step_inputs.new_seq_params) {
      MutableSequencePtr new_seq = std::make_shared<Sequence>(Sequence(params));
      worker_sequence_manager_->AddSequence(new_seq);
    }

    // Execute model
    auto output = ExecuteModel(step_inputs.scheduler_output);

    // Skip sending output if not tensor parallel rank zero
    if (!is_tensor_parallel_rank_zero_) {
      continue;
    }

    // Create step outputs and send
    StepOutputs step_outputs(step_inputs.scheduler_output->id, output);
    ZmqHelper::Send<StepOutputs>(*output_socket_, step_outputs);
  }
}
//==============================================================================
