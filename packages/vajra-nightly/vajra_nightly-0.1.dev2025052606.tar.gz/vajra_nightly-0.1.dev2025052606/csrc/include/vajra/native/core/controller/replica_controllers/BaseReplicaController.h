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
#include "commons/BoostCommon.h"
#include "native/configs/ReplicaControllerConfig.h"
#include "native/core/controller/AbstractController.h"
#include "native/core/scheduler/request_prioritizers/BaseRequestPrioritizer.h"
#include "native/data_structures/Queues.h"
//==============================================================================
namespace vajra {
//==============================================================================
class BaseReplicaController
    : public AbstractController<
          boost::concurrent::sync_priority_queue<
              std::shared_ptr<BaseSequenceWithPriority>,
              std::vector<std::shared_ptr<BaseSequenceWithPriority>>,
              BaseSequenceWithPriorityComparator>,
          boost::concurrent::sync_queue<std::shared_ptr<RequestOutput>>> {
 public:
  BaseReplicaController(
      ReplicaId replica_id, std::shared_ptr<BaseReplicaControllerConfig> config,
      std::shared_ptr<BaseRequestPrioritizer> request_prioritizer,
      SequencePriorityQueuePtr waiting_seq_queue,
      RequestOutputQueuePtr output_queue)
      : AbstractController<
            boost::concurrent::sync_priority_queue<
                std::shared_ptr<BaseSequenceWithPriority>,
                std::vector<std::shared_ptr<BaseSequenceWithPriority>>,
                BaseSequenceWithPriorityComparator>,
            boost::concurrent::sync_queue<std::shared_ptr<RequestOutput>>>(
            waiting_seq_queue, output_queue),
        replica_id_(replica_id),
        config_(config),
        request_prioritizer_(request_prioritizer) {
    ASSERT_VALID_POINTER_ARGUMENT(config);
    ASSERT_VALID_POINTER_ARGUMENT(request_prioritizer);
    ASSERT_VALID_POINTER_ARGUMENT(waiting_seq_queue);
    ASSERT_VALID_POINTER_ARGUMENT(output_queue);
  }

  virtual ~BaseReplicaController() = default;

  std::shared_ptr<BaseReplicaControllerConfig> GetConfig() const {
    return config_;
  }

 protected:
  ReplicaId replica_id_;
  std::shared_ptr<BaseReplicaControllerConfig> config_;
  std::shared_ptr<BaseRequestPrioritizer> request_prioritizer_;
};
//==============================================================================
}  // namespace vajra
//==============================================================================
