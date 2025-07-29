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
#include "native/configs/ReplicasetSchedulerConfig.h"
#include "native/core/scheduler/replicaset_schedulers/BaseReplicasetScheduler.h"
#include "native/data_structures/Queues.h"
#include "native/datatypes/BaseSequenceWithPriority.h"
//==============================================================================
namespace vajra {
//==============================================================================
class PullReplicasetScheduler : public BaseReplicasetScheduler {
 public:
  PullReplicasetScheduler(std::shared_ptr<PullReplicasetSchedulerConfig> config,
                          std::size_t num_replicas)
      : BaseReplicasetScheduler(config, num_replicas),
        request_queue_(std::make_shared<SequencePriorityQueue>()) {
    ASSERT_VALID_POINTER_ARGUMENT(config);
  }

  [[nodiscard]] SequencePriorityQueuePtr GetReplicaQueue(
      ReplicaId) const override {
    return request_queue_;
  }

  void Schedule(const MutableBaseSequenceWithPriorityPtr& seq) override {
    request_queue_->push(seq);
  }

 private:
  SequencePriorityQueuePtr request_queue_;
};
//==============================================================================
}  // namespace vajra
//==============================================================================
