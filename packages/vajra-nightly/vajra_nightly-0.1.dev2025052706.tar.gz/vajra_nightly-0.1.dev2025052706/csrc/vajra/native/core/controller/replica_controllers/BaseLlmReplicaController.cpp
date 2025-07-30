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
#include "native/core/controller/replica_controllers/BaseLlmReplicaController.h"
//==============================================================================
#include "commons/Time.h"
#include "native/utils/ZmqHelper.h"
//==============================================================================
namespace vajra {
//==============================================================================
BaseLlmReplicaController::BaseLlmReplicaController(
    ReplicaId replica_id, std::shared_ptr<LlmReplicaControllerConfig> config,
    std::shared_ptr<BaseRequestPrioritizer> request_prioritizer,
    CommInfoPtr comm_info, SequencePriorityQueuePtr waiting_seq_queue,
    RequestOutputQueuePtr output_queue,
    std::shared_ptr<BaseReplicaScheduler> scheduler,
    std::shared_ptr<EngineSequenceManager> sequence_manager,
    std::shared_ptr<EngineMetricsStore> metrics_store)
    : BaseReplicaController(replica_id, config, request_prioritizer,
                            waiting_seq_queue, output_queue),
      scheduler_(scheduler),
      comm_info_(comm_info),
      sequence_manager_(sequence_manager),
      metrics_store_(metrics_store),
      replica_id_(replica_id) {
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
void BaseLlmReplicaController::InitializeThreads() {
  controller_running_ = true;
  stop_worker_ = false;

  // Start the worker thread for async processing
  worker_thread_ =
      std::thread(&BaseLlmReplicaController::OutputWorkerLoop, this);

  // Start the scheduler thread
  scheduler_thread_ =
      std::thread(&BaseLlmReplicaController::SchedulerLoop, this);
}
//==============================================================================
void BaseLlmReplicaController::StopThreads() {
  controller_running_ = false;

  // Stop the worker thread
  stop_worker_ = true;
  // Push empty task to wake up worker thread
  task_queue_.push({});

  if (worker_thread_.joinable()) {
    worker_thread_.join();
  }

  if (scheduler_thread_.joinable()) {
    scheduler_thread_.join();
  }
}
//==============================================================================
BaseLlmReplicaController::~BaseLlmReplicaController() {
  StopThreads();
  CloseZmqSockets();
}
//==============================================================================
void BaseLlmReplicaController::BindZmqSocket(zmq::socket_t& socket,
                                             std::size_t port) {
  std::string endpoint = std::format("tcp://*:{}", port);

  for (std::size_t num_retries = 0;
       num_retries < REPLICA_CONTROLLER_ZMQ_BIND_RETRIES; ++num_retries) {
    try {
      socket.bind(endpoint);
      return;
    } catch (const zmq::error_t& e) {
      LOG_WARNING("Failed to bind socket to {}: {}", endpoint, e.what());
      LOG_WARNING("Retrying in {} seconds...",
                  REPLICA_CONTROLLER_ZMQ_BIND_BACKOFF_S);
      std::this_thread::sleep_for(
          std::chrono::seconds(REPLICA_CONTROLLER_ZMQ_BIND_BACKOFF_S));
    }
  }

  THROW_RUNTIME_ERROR("Failed to bind socket to {} after {} retries", endpoint,
                      REPLICA_CONTROLLER_ZMQ_BIND_RETRIES);
}
//==============================================================================
void BaseLlmReplicaController::InitZmqSockets() {
  zmq_context_ = zmq::context_t();
  enqueue_socket_ = zmq::socket_t(zmq_context_, zmq::socket_type::pub);
  output_socket_ = zmq::socket_t(zmq_context_, zmq::socket_type::pull);

  LOG_INFO("Initializing ZMQ sockets for replica controller {}", replica_id_);
  LOG_INFO("Initializing enqueue socket, binding to port {}",
           comm_info_->enqueue_socket_port);
  BindZmqSocket(enqueue_socket_, comm_info_->enqueue_socket_port);
  LOG_INFO("Initializing output socket, binding to port {}",
           comm_info_->output_socket_port);
  BindZmqSocket(output_socket_, comm_info_->output_socket_port);
}
//==============================================================================
void BaseLlmReplicaController::CloseZmqSockets() {
  enqueue_socket_.close();
  output_socket_.close();
  zmq_context_.close();
}
//==============================================================================
void BaseLlmReplicaController::OnStepCompleted(
    const SchedulerOutputPtr& scheduler_output, const MutableSequences& seqs,
    const ValidSamplerOutputs& sampler_outputs, const TimeS start_time) {
  // Process sequence manager updates
  sequence_manager_->OnStepCompleted(
      scheduler_output->seq_schedule_metadata_list, sampler_outputs);

  scheduler_->OnStepCompleted(
      seqs, static_cast<float>(time_utils::now_s() - start_time));
  // Update metrics
  metrics_store_->OnBatchEnd(AsConstSequences(seqs), scheduler_output,
                             start_time, time_utils::now_s());
}
//==============================================================================
void BaseLlmReplicaController::PushRequestOutputs(
    const SequenceScheduleMetadataPtrList& seq_schedule_metadata_list,
    const MutableSequences& ignored_seqs, const MutableSequences& seqs) {
  // Create shared_ptrs to protect the data during async execution
  auto ignored_seqs_copy = std::make_shared<MutableSequences>(ignored_seqs);
  auto seqs_copy = std::make_shared<MutableSequences>(seqs);
  auto seq_schedule_metadata_list_copy =
      std::make_shared<SequenceScheduleMetadataPtrList>(
          seq_schedule_metadata_list);

  // Create and enqueue the task
  EnqueueTask(
      [this, ignored_seqs_copy, seqs_copy, seq_schedule_metadata_list_copy]() {
        try {
          // The second parameter is not used in the engine append token
          for (std::size_t i = 0; i < seq_schedule_metadata_list_copy->size();
               i++) {
            auto seq = (*seqs_copy)[i];
            sequence_manager_->OnAppendTokenImpl(seq);
          }
          std::vector<RequestOutputPtr> request_outputs =
              sequence_manager_->GenerateRequestOutputs(
                  AsConstSequences(*ignored_seqs_copy),
                  AsConstSequences(*seqs_copy));

          // Push each request output to the output queue
          for (const auto& request_output : request_outputs) {
            output_queue_->push(request_output);
          }
        } catch (const std::exception& e) {
          LOG_ERROR("Exception processing request outputs for replica {}: {}",
                    replica_id_, e.what());
        }
      });
}
//==============================================================================
void BaseLlmReplicaController::OutputWorkerLoop() {
  LOG_INFO("Request output worker thread started for replica {}", replica_id_);

  while (!stop_worker_.load()) {
    RequestOutputTask task;
    // Wait for a task to become available
    task_queue_.wait_pull(task);

    // Check for stop signal after potentially being woken up by an empty task
    if (stop_worker_.load()) {
      break;
    }

    // Execute the task
    if (task) {
      try {
        task();
      } catch (const std::exception& e) {
        LOG_ERROR(
            "Exception in request output worker thread for replica {}: {}",
            replica_id_, e.what());
      } catch (...) {
        LOG_ERROR(
            "Unknown exception in request output worker thread for replica {}",
            replica_id_);
      }
    }
  }

  LOG_INFO("Request output worker thread stopped for replica {}", replica_id_);
}
//==============================================================================
ValidSamplerOutputs BaseLlmReplicaController::CombineSamplerOutputs(
    const std::vector<SamplerOutputPtr>& all_workers_sampler_outputs,
    const SequenceScheduleMetadataPtrList& seq_schedule_metadata_list) {
  std::unordered_map<std::string, SamplerOutputPtr> sampler_outputs_map;
  sampler_outputs_map.reserve(all_workers_sampler_outputs.size());

  for (const auto& output : all_workers_sampler_outputs) {
    if (output) {
      sampler_outputs_map[output->GetSeqId()] = output;
    }
  }

  ValidSamplerOutputs result;
  result.reserve(sampler_outputs_map.size());

  // Sort sampler outputs based on sequence schedule metadata
  for (const auto& metadata : seq_schedule_metadata_list) {
    if (sampler_outputs_map.find(metadata->seq_id) !=
        sampler_outputs_map.end()) {
      result.push_back(sampler_outputs_map[metadata->seq_id]);
    } else {
      ASSERT_VALID_RUNTIME(false, "sampler output not found for sequence {}",
                           metadata->seq_id);
    }
  }

  return result;
}
//==============================================================================
void BaseLlmReplicaController::Step() {
  auto start_time = time_utils::now_s();

  auto [scheduler_output, new_seqs] = scheduler_->Schedule();

  if (scheduler_output->is_empty) {
    return;
  }

  for (const auto& seq : new_seqs) {
    sequence_manager_->AddSequence(seq);
  }

  auto [ignored_seqs, seqs] = sequence_manager_->OnSchedule(scheduler_output);

  auto end_time = time_utils::now_s();

  std::vector<SequenceParams> new_seq_params;
  for (const auto& seq : new_seqs) {
    new_seq_params.emplace_back(seq->GetParams());
  }

  auto step_inputs = StepInputs(scheduler_output, new_seq_params);

  ZmqHelper::Send<StepInputs>(enqueue_socket_, step_inputs);

  metrics_store_->OnSchedule(replica_id_, scheduler_output, start_time,
                             end_time);
  std::vector<SamplerOutputPtr> all_workers_sampler_outputs;

  std::size_t kv_parallel_size = GetConfig()->parallel_config.kv_parallel_size;

  for (std::size_t i = 0; i < kv_parallel_size; ++i) {
    StepOutputs step_outputs = ZmqHelper::Recv<StepOutputs>(output_socket_);
    ASSERT_VALID_RUNTIME(step_outputs.schedule_id == scheduler_output->id,
                         "Schedule ID Mismatch");

    for (const auto& sampler_output : step_outputs.sampler_outputs) {
      if (sampler_output) {
        all_workers_sampler_outputs.push_back(sampler_output.value());
      }
    }
  }

  ValidSamplerOutputs sampler_outputs =
      CombineSamplerOutputs(all_workers_sampler_outputs,
                            scheduler_output->seq_schedule_metadata_list);

  OnStepCompleted(scheduler_output, seqs, sampler_outputs, start_time);

  // async request output processing
  PushRequestOutputs(scheduler_output->seq_schedule_metadata_list, ignored_seqs,
                     seqs);
}
//==============================================================================
void BaseLlmReplicaController::SchedulerLoop() {
  while (controller_running_) {
    Step();
  }
}
//==============================================================================
}  // namespace vajra
//==============================================================================
