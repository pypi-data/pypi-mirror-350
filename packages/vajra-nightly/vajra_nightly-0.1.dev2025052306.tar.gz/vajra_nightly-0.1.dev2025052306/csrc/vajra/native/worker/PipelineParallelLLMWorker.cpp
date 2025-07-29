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
#include "native/worker/PipelineParallelLLMWorker.h"
//==============================================================================
using vajra::PipelineParallelLLMWorker;
using vajra::SamplerOutputs;
//==============================================================================
PipelineParallelLLMWorker::PipelineParallelLLMWorker(
    ReplicaId replica_id /*[in]*/, std::size_t rank /*[in]*/,
    ZmqSocketPtr enqueue_socket /*[in]*/, ZmqSocketPtr output_socket /*[in]*/,
    WorkerSequenceManagerPtr worker_sequence_manager /*[in]*/,
    WorkerMetricsStorePtr worker_metrics_store /*[in]*/,
    BaseModelRunnerPtr model_runner /*[in]*/,
    std::vector<torch::Tensor> gpu_caches /*[in]*/,
    ProcessGroupWrapperPtr process_group_wrapper /*[in]*/,
    ZmqSocketPtr microbatch_socket /*[in]*/
    )
    : BaseLLMWorker(replica_id, rank, enqueue_socket, output_socket,
                    worker_sequence_manager, worker_metrics_store, model_runner,
                    gpu_caches, process_group_wrapper),
      microbatch_socket_(microbatch_socket) {
  ASSERT_VALID_POINTER_ARGUMENT(enqueue_socket);
  ASSERT_VALID_POINTER_ARGUMENT(output_socket);
  ASSERT_VALID_POINTER_ARGUMENT(microbatch_socket);
  ASSERT_VALID_POINTER_ARGUMENT(worker_sequence_manager);
  ASSERT_VALID_POINTER_ARGUMENT(worker_metrics_store);
  ASSERT_VALID_POINTER_ARGUMENT(model_runner);
  ASSERT_VALID_POINTER_ARGUMENT(process_group_wrapper);
}

void PipelineParallelLLMWorker::OnStepCompleted(
    SchedulerOutputPtr scheduler_output /*[in]*/, const SamplerOutputs& /*[in]*/
) {
  ASSERT_VALID_POINTER_ARGUMENT(scheduler_output);
  // In pipeline parallel case, just update for this stage completion
  worker_sequence_manager_->OnStageCompleted(scheduler_output);
}

void PipelineParallelLLMWorker::ExecutionLoop() {
  while (true) {
    auto step_inputs = ZmqHelper::Recv<StepInputs>(*enqueue_socket_);

    // Add new sequences
    for (const auto& params : step_inputs.new_seq_params) {
      MutableSequencePtr new_seq = std::make_shared<Sequence>(Sequence(params));
      worker_sequence_manager_->AddSequence(new_seq);
    }

    // Process pending step outputs
    for (const auto& pending_step_output : step_inputs.pending_step_outputs) {
      ASSERT_VALID_POINTER_ARGUMENT(pending_step_output.scheduler_output);
      worker_sequence_manager_->OnStepCompleted(
          pending_step_output.scheduler_output->seq_schedule_metadata_list,
          pending_step_output.sampler_outputs);
    }

    // Execute model
    auto output = ExecuteModel(step_inputs.scheduler_output);

    // Skip sending output if not tensor parallel rank zero
    if (!is_tensor_parallel_rank_zero_) {
      continue;
    }

    // Send appropriate output based on pipeline stage
    if (is_last_pipeline_stage_) {
      // Send final output to engine
      LOG_DEBUG("Worker {} sending output to engine", rank_);
      StepOutputs step_outputs(step_inputs.scheduler_output->id, output);
      ZmqHelper::Send<StepOutputs>(*output_socket_, step_outputs);
    } else if (is_first_pipeline_stage_) {
      // Send microbatch signal
      LOG_DEBUG("Worker {} sending microbatch signal", rank_);
      StepMicrobatchOutputs step_microbatch_outputs(
          step_inputs.scheduler_output->id);
      ZmqHelper::Send<StepMicrobatchOutputs>(*microbatch_socket_,
                                             step_microbatch_outputs);
    }
  }
}
//==============================================================================
