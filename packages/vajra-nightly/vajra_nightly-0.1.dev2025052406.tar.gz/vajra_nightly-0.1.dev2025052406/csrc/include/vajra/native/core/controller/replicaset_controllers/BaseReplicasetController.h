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
#include "native/configs/ReplicasetControllerConfig.h"
#include "native/core/controller/AbstractController.h"
#include "native/core/scheduler/replicaset_schedulers/BaseReplicasetScheduler.h"
#include "native/core/scheduler/request_prioritizers/BaseRequestPrioritizer.h"
//==============================================================================
namespace vajra {
//==============================================================================
template <typename WaitingQueueType, typename OutputQueueType>
class BaseReplicasetController
    : public AbstractController<WaitingQueueType, OutputQueueType> {
 public:
  BaseReplicasetController(
      std::shared_ptr<BaseReplicasetControllerConfig> config,
      std::shared_ptr<WaitingQueueType> waiting_seq_queue,
      std::shared_ptr<OutputQueueType> output_queue,
      std::shared_ptr<BaseRequestPrioritizer> request_prioritizer,
      std::shared_ptr<BaseReplicasetScheduler> replica_scheduler)
      : AbstractController<WaitingQueueType, OutputQueueType>(waiting_seq_queue,
                                                              output_queue),
        config_(config),
        request_prioritizer_(request_prioritizer),
        replica_scheduler_(replica_scheduler) {}

  virtual ~BaseReplicasetController() = default;

 protected:
  std::shared_ptr<BaseReplicasetControllerConfig> config_;
  std::shared_ptr<BaseRequestPrioritizer> request_prioritizer_;
  std::shared_ptr<BaseReplicasetScheduler> replica_scheduler_;
};
//==============================================================================
}  // namespace vajra
//==============================================================================
