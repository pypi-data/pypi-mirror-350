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
#include "commons/Time.h"
#include "commons/TorchCommon.h"
#include "native/configs/ParallelConfig.h"
#include "native/core/Types.h"
#include "native/core/sequence_manager/WorkerSequenceManager.h"
#include "native/metrics_store/WorkerMetricsStore.h"
#include "native/model_executor/BaseModelRunner.h"
#include "native/model_executor/parallel_utils/ProcessGroupWrapper.h"
#include "native/utils/ZmqHelper.h"
//==============================================================================
namespace vajra {
//==============================================================================
class BaseWorker : public NonCopyableNonMovable {
 public:
  BaseWorker() = delete;

  BaseWorker(ReplicaId replica_id /*[in]*/, std::size_t rank /*[in]*/,
             ZmqSocketPtr enqueue_socket /*[in]*/,
             ZmqSocketPtr output_socket /*[in]*/,
             WorkerSequenceManagerPtr worker_sequence_manager /*[in]*/,
             WorkerMetricsStorePtr worker_metrics_store /*[in]*/,
             BaseModelRunnerPtr model_runner /*[in]*/
             )
      : replica_id_(replica_id),
        rank_(rank),
        enqueue_socket_(enqueue_socket),
        output_socket_(output_socket),
        worker_sequence_manager_(worker_sequence_manager),
        worker_metrics_store_(worker_metrics_store),
        model_runner_(model_runner) {
    ASSERT_VALID_POINTER_ARGUMENT(enqueue_socket);
    ASSERT_VALID_POINTER_ARGUMENT(output_socket);
    ASSERT_VALID_POINTER_ARGUMENT(worker_sequence_manager);
    ASSERT_VALID_POINTER_ARGUMENT(worker_metrics_store);
    ASSERT_VALID_POINTER_ARGUMENT(model_runner);
  }

  virtual ~BaseWorker() = default;

  virtual SamplerOutputs ExecuteModel(
      SchedulerOutputPtr scheduler_output /*[in]*/
      ) = 0;

  virtual void ExecutionLoop() = 0;

 protected:
  // Worker info
  const ReplicaId replica_id_;
  const std::size_t rank_;

  // Zmq sockets
  const ZmqSocketPtr enqueue_socket_;
  const ZmqSocketPtr output_socket_;

  // Worker components
  const WorkerSequenceManagerPtr worker_sequence_manager_;
  const WorkerMetricsStorePtr worker_metrics_store_;
  const BaseModelRunnerPtr model_runner_;
};
//==============================================================================
using BaseWorkerPtr = std::shared_ptr<BaseWorker>;
//==============================================================================
}  // namespace vajra
//==============================================================================
