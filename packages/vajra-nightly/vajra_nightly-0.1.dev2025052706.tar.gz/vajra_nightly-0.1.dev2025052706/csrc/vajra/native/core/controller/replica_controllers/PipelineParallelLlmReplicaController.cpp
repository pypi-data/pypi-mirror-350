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
#include "native/core/controller/replica_controllers/PipelineParallelLlmReplicaController.h"
//==============================================================================
#include "commons/Time.h"
#include "native/configs/ParallelConfig.h"
#include "native/utils/ZmqHelper.h"
//==============================================================================
namespace vajra {
//==============================================================================
PipelineParallelLlmReplicaController::PipelineParallelLlmReplicaController(
    ReplicaId replica_id, std::shared_ptr<LlmReplicaControllerConfig> config,
    std::shared_ptr<BaseRequestPrioritizer> request_prioritizer,
    CommInfoPtr comm_info, SequencePriorityQueuePtr waiting_seq_queue,
    RequestOutputQueuePtr output_queue,
    std::shared_ptr<BaseReplicaScheduler> scheduler,
    std::shared_ptr<EngineSequenceManager> sequence_manager,
    std::shared_ptr<EngineMetricsStore> metrics_store)
    : BaseLlmReplicaController(replica_id, config, request_prioritizer,
                               comm_info, waiting_seq_queue, output_queue,
                               scheduler, sequence_manager, metrics_store) {
  ASSERT_VALID_POINTER_ARGUMENT(config);
  ASSERT_VALID_POINTER_ARGUMENT(request_prioritizer);
  ASSERT_VALID_POINTER_ARGUMENT(comm_info);
  ASSERT_VALID_POINTER_ARGUMENT(waiting_seq_queue);
  ASSERT_VALID_POINTER_ARGUMENT(output_queue);
  ASSERT_VALID_POINTER_ARGUMENT(scheduler);
  ASSERT_VALID_POINTER_ARGUMENT(sequence_manager);
  ASSERT_VALID_POINTER_ARGUMENT(metrics_store);

  InitZmqSockets();
  InitializeThreads();
}
//==============================================================================
PipelineParallelLlmReplicaController::~PipelineParallelLlmReplicaController() {
  CloseZmqSockets();
  StopThreads();
}
//==============================================================================
void PipelineParallelLlmReplicaController::InitializeThreads() {
  microbatch_watcher_thread_ = std::thread(
      &PipelineParallelLlmReplicaController::MicrobatchWatcherLoop, this);

  output_thread_ =
      std::thread(&PipelineParallelLlmReplicaController::OutputLoop, this);

  scheduler_thread_ =
      std::thread(&PipelineParallelLlmReplicaController::SchedulerLoop, this);
}
//==============================================================================
void PipelineParallelLlmReplicaController::StopThreads() {
  controller_running_ = false;
  scheduler_output_queue_.close();
  microbatch_watch_queue_.close();
  microbatch_output_processing_sync_queue_.close();

  if (microbatch_watcher_thread_.joinable()) {
    microbatch_watcher_thread_.join();
  }
  if (output_thread_.joinable()) {
    output_thread_.join();
  }
  if (scheduler_thread_.joinable()) {
    scheduler_thread_.join();
  }
}
//==============================================================================
void PipelineParallelLlmReplicaController::InitZmqSockets() {
  microbatch_socket_ = zmq::socket_t(zmq_context_, zmq::socket_type::pull);

  LOG_INFO("Initializing microbatch socket, binding to port {}",
           comm_info_->microbatch_socket_port);
  BindZmqSocket(microbatch_socket_, comm_info_->microbatch_socket_port);
}
//==============================================================================
void PipelineParallelLlmReplicaController::CloseZmqSockets() {
  microbatch_socket_.close();
}
//==============================================================================
void PipelineParallelLlmReplicaController::Step() {
  auto start_time = time_utils::now_s();

  auto [scheduler_output, new_seqs] = scheduler_->Schedule();

  if (scheduler_output->has_no_output) {
    return;
  }

  for (const auto& seq : new_seqs) {
    sequence_manager_->AddSequence(seq);
  }

  auto [ignored_seqs, seqs] = sequence_manager_->OnSchedule(scheduler_output);

  auto schedule_stage_outputs = std::make_shared<ScheduleStageOutputs>(
      ignored_seqs, seqs, scheduler_output, start_time);

  scheduler_output_queue_.push(schedule_stage_outputs);

  auto end_time = time_utils::now_s();

  if (!scheduler_output->is_empty) {
    microbatch_watch_queue_.push(scheduler_output);

    std::vector<PendingStepOutput> pending_step_outputs;
    {
      std::lock_guard<std::mutex> lock(pending_step_outputs_mutex_);
      pending_step_outputs = std::move(pending_step_outputs_);
    }

    std::vector<SequenceParams> new_seq_params;
    for (const auto& seq : new_seqs) {
      new_seq_params.emplace_back(seq->GetParams());
    }

    StepInputs step_inputs(scheduler_output, new_seq_params,
                           pending_step_outputs);

    ZmqHelper::Send<StepInputs>(enqueue_socket_, step_inputs);
  }

  metrics_store_->OnSchedule(replica_id_, scheduler_output, start_time,
                             end_time);
}
//==============================================================================
void PipelineParallelLlmReplicaController::MicrobatchWatchStep() {
  SchedulerOutputPtr scheduler_output;
  try {
    scheduler_output = microbatch_watch_queue_.pull();
  } catch (const boost::sync_queue_is_closed& e) {
    return;
  }

  std::size_t num_microbatches_received = 0;
  // Check if we have a scheduler output for this schedule ID
  auto scheduler_output_it =
      pending_microbatch_outputs_stage_complete_.find(scheduler_output->id);

  if (scheduler_output_it != pending_microbatch_outputs_stage_complete_.end()) {
    num_microbatches_received = scheduler_output_it->second;
    scheduler_output_it->second = 0;
  }

  while (num_microbatches_received <
         GetConfig()->parallel_config.kv_parallel_size) {
    StepMicrobatchOutputs step_microbatch_outputs =
        ZmqHelper::Recv<StepMicrobatchOutputs>(microbatch_socket_);

    if (step_microbatch_outputs.schedule_id != scheduler_output->id) {
      pending_microbatch_outputs_stage_complete_[step_microbatch_outputs
                                                     .schedule_id]++;
      continue;
    }

    num_microbatches_received++;
  }

  // Notify sequence manager that a stage is completed
  sequence_manager_->OnStageCompleted(scheduler_output);

  MutableSequences seqs;
  for (const auto& seq_schedule_metadata :
       scheduler_output->seq_schedule_metadata_list) {
    seqs.push_back(
        sequence_manager_->GetMutableSequence(seq_schedule_metadata->seq_id));
  }

  scheduler_->OnStageCompleted(seqs);

  microbatch_output_processing_sync_queue_.push(true);
}
//==============================================================================
void PipelineParallelLlmReplicaController::OutputStep() {
  // Use the public pull method instead of trying to access the mutex directly
  ScheduleStageOutputsPtr schedule_stage_outputs;
  try {
    schedule_stage_outputs = scheduler_output_queue_.pull();
  } catch (const boost::sync_queue_is_closed& e) {
    return;
  }

  // Use a vector of pointers to StepOutputs instead of StepOutputs directly
  SamplerOutputs all_sampler_outputs =
      std::move(pending_sampler_outputs_map_[schedule_stage_outputs
                                                 ->scheduler_output->id]);

  std::size_t num_sampler_outputs_received = all_sampler_outputs.size();

  while (num_sampler_outputs_received <
         GetConfig()->parallel_config.kv_parallel_size) {
    StepOutputs step_output = ZmqHelper::Recv<StepOutputs>(output_socket_);
    if (step_output.schedule_id !=
        schedule_stage_outputs->scheduler_output->id) {
      // extend the pending_sampler_outputs_map_ with the new sampler outputs
      auto& pending_sampler_outputs =
          pending_sampler_outputs_map_[step_output.schedule_id];
      pending_sampler_outputs.reserve(pending_sampler_outputs.size() +
                                      step_output.sampler_outputs.size());
      pending_sampler_outputs.insert(pending_sampler_outputs.end(),
                                     step_output.sampler_outputs.begin(),
                                     step_output.sampler_outputs.end());
    } else {
      all_sampler_outputs.reserve(all_sampler_outputs.size() +
                                  step_output.sampler_outputs.size());
      all_sampler_outputs.insert(all_sampler_outputs.end(),
                                 step_output.sampler_outputs.begin(),
                                 step_output.sampler_outputs.end());
      num_sampler_outputs_received++;
    }
  }

  ValidSamplerOutputs sampler_outputs;
  for (const auto& sampler_output : all_sampler_outputs) {
    if (sampler_output && sampler_output.value()) {
      sampler_outputs.push_back(sampler_output.value());
    }
  }

  auto combined_sampler_outputs = CombineSamplerOutputs(
      sampler_outputs,
      schedule_stage_outputs->scheduler_output->seq_schedule_metadata_list);

  {
    std::lock_guard<std::mutex> lock(pending_step_outputs_mutex_);
    pending_step_outputs_.emplace_back(schedule_stage_outputs->scheduler_output,
                                       combined_sampler_outputs);
  }

  // Use the public pull method instead of trying to access the mutex directly
  try {
    microbatch_output_processing_sync_queue_.pull();
  } catch (const boost::sync_queue_is_closed& e) {
    return;
  }

  OnStepCompleted(schedule_stage_outputs->scheduler_output,
                  schedule_stage_outputs->seqs, combined_sampler_outputs,
                  schedule_stage_outputs->start_time);

  // async request output processing
  PushRequestOutputs(
      schedule_stage_outputs->scheduler_output->seq_schedule_metadata_list,
      schedule_stage_outputs->ignored_seqs, schedule_stage_outputs->seqs);
}
//==============================================================================
void PipelineParallelLlmReplicaController::MicrobatchWatcherLoop() {
  while (controller_running_) {
    MicrobatchWatchStep();
  }
}
//==============================================================================
void PipelineParallelLlmReplicaController::OutputLoop() {
  while (controller_running_) {
    OutputStep();
  }
}
//==============================================================================
}  // namespace vajra
//==============================================================================
