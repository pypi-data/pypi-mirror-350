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
#include <zmq.hpp>
//==============================================================================
#include "commons/BoostCommon.h"
#include "commons/Time.h"
#include "native/core/controller/replica_controllers/BaseReplicaController.h"
#include "native/core/scheduler/replica_schedulers/BaseReplicaScheduler.h"
#include "native/core/sequence_manager/EngineSequenceManager.h"
#include "native/datatypes/CommInfo.h"
#include "native/metrics_store/EngineMetricsStore.h"
//==============================================================================
namespace vajra {
//==============================================================================
constexpr std::size_t REPLICA_CONTROLLER_ZMQ_BIND_RETRIES = 5;
constexpr std::size_t REPLICA_CONTROLLER_ZMQ_BIND_BACKOFF_S = 5;
//==============================================================================
// Task type for the async processing queue
using RequestOutputTask = std::function<void()>;

class BaseLlmReplicaController : public BaseReplicaController {
 public:
  BaseLlmReplicaController(
      ReplicaId replica_id, std::shared_ptr<LlmReplicaControllerConfig> config,
      std::shared_ptr<BaseRequestPrioritizer> request_prioritizer,
      CommInfoPtr comm_info, SequencePriorityQueuePtr waiting_seq_queue,
      RequestOutputQueuePtr output_queue,
      std::shared_ptr<BaseReplicaScheduler> scheduler,
      std::shared_ptr<EngineSequenceManager> sequence_manager,
      std::shared_ptr<EngineMetricsStore> metrics_store);

  ~BaseLlmReplicaController() override;

  std::shared_ptr<LlmReplicaControllerConfig> GetConfig() const {
    return std::static_pointer_cast<LlmReplicaControllerConfig>(config_);
  }

 protected:
  void BindZmqSocket(zmq::socket_t& socket, std::size_t port);

  void OnStepCompleted(const SchedulerOutputPtr& scheduler_output,
                       const MutableSequences& seqs,
                       const ValidSamplerOutputs& sampler_outputs,
                       const TimeS start_time);

  // async function for pushing request outputs
  void PushRequestOutputs(
      const SequenceScheduleMetadataPtrList& seq_schedule_metadata_list,
      const MutableSequences& ignored_seqs, const MutableSequences& seqs);

  ValidSamplerOutputs CombineSamplerOutputs(
      const std::vector<SamplerOutputPtr>& all_workers_sampler_outputs,
      const SequenceScheduleMetadataPtrList& seq_schedule_metadata_list);

  virtual void Step();

  void SchedulerLoop();

  // Enqueue a task for async execution
  inline void EnqueueTask(RequestOutputTask task) {
    task_queue_.push(std::move(task));
  }

  std::shared_ptr<BaseReplicaScheduler> scheduler_;
  CommInfoPtr comm_info_;
  std::shared_ptr<EngineSequenceManager> sequence_manager_;
  std::shared_ptr<EngineMetricsStore> metrics_store_;
  std::atomic<bool> controller_running_{false};
  std::thread scheduler_thread_;
  zmq::socket_t output_socket_;
  zmq::socket_t enqueue_socket_;
  zmq::context_t zmq_context_;
  ReplicaId replica_id_;

 private:
  void InitializeThreads();

  void StopThreads();

  void InitZmqSockets();

  void CloseZmqSockets();

  // Worker thread and queue for asynchronous processing
  std::thread worker_thread_;
  Queue<RequestOutputTask> task_queue_;
  std::atomic<bool> stop_worker_{false};

  // Worker thread loop method
  void OutputWorkerLoop();
};
//==============================================================================
}  // namespace vajra
//==============================================================================
