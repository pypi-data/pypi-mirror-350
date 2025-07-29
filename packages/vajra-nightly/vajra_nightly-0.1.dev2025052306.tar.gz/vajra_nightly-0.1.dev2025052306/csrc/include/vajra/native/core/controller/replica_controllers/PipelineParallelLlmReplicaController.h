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
#include "native/core/controller/replica_controllers/BaseLlmReplicaController.h"
#include "native/datatypes/PendingStepOutput.h"
#include "native/datatypes/ScheduleStageOutputs.h"
#include "native/datatypes/StepMicrobatchOutputs.h"
#include "native/datatypes/StepOutputs.h"
//==============================================================================
namespace vajra {
//==============================================================================
// Constants already defined in BaseLlmReplicaController.h
// constexpr std::size_t REPLICA_CONTROLLER_ZMQ_BIND_RETRIES = 10;
constexpr std::size_t REPLICA_CONTROLLER_ZMQ_BIND_BACKOFF_MS = 100;
//==============================================================================
class PipelineParallelLlmReplicaController : public BaseLlmReplicaController {
 public:
  PipelineParallelLlmReplicaController(
      ReplicaId replica_id, std::shared_ptr<LlmReplicaControllerConfig> config,
      std::shared_ptr<BaseRequestPrioritizer> request_prioritizer,
      CommInfoPtr comm_info, SequencePriorityQueuePtr waiting_seq_queue,
      RequestOutputQueuePtr output_queue,
      std::shared_ptr<BaseReplicaScheduler> scheduler,
      std::shared_ptr<EngineSequenceManager> sequence_manager,
      std::shared_ptr<EngineMetricsStore> metrics_store);

  ~PipelineParallelLlmReplicaController();

 private:
  void InitializeThreads();

  void StopThreads();

  void InitZmqSockets();

  void CloseZmqSockets();

  void Step() override;

  void MicrobatchWatchStep();

  void MicrobatchWatcherLoop();

  void OutputStep();

  void OutputLoop();

  std::thread microbatch_watcher_thread_;
  std::thread output_thread_;
  std::thread scheduler_thread_;

  zmq::socket_t microbatch_socket_;

  std::vector<PendingStepOutput> pending_step_outputs_;
  std::mutex pending_step_outputs_mutex_;

  // Map of schedule ID to vector of StepOutputs
  std::unordered_map<std::size_t, SamplerOutputs> pending_sampler_outputs_map_;

  // Map of schedule ID to number of microbatches received for stage completion
  // which are pending processing
  std::unordered_map<std::size_t, std::size_t>
      pending_microbatch_outputs_stage_complete_;

  Queue<ScheduleStageOutputsPtr> scheduler_output_queue_;
  Queue<SchedulerOutputPtr> microbatch_watch_queue_;
  Queue<bool> microbatch_output_processing_sync_queue_;
};
//==============================================================================
}  // namespace vajra
//==============================================================================
