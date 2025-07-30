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
class RoundRobinReplicasetScheduler : public BaseReplicasetScheduler {
 public:
  RoundRobinReplicasetScheduler(
      std::shared_ptr<RoundRobinReplicasetSchedulerConfig> config,
      std::size_t num_replicas)
      : BaseReplicasetScheduler(config, num_replicas), current_replica_id_(0) {
    ASSERT_VALID_POINTER_ARGUMENT(config);

    replica_queue_mapping_.reserve(num_replicas);
    for (std::size_t i = 0; i < num_replicas; ++i) {
      replica_queue_mapping_[i] = std::make_shared<SequencePriorityQueue>();
    }
  }

  [[nodiscard]] SequencePriorityQueuePtr GetReplicaQueue(
      ReplicaId replica_id) const override {
    return replica_queue_mapping_.at(replica_id);
  }

  void Schedule(const MutableBaseSequenceWithPriorityPtr& seq) override {
    replica_queue_mapping_.at(current_replica_id_)->push(seq);
    current_replica_id_ = (current_replica_id_ + 1) % num_replicas_;
  }

 private:
  std::size_t current_replica_id_;
  std::unordered_map<std::size_t, SequencePriorityQueuePtr>
      replica_queue_mapping_;
};
//==============================================================================
}  // namespace vajra
//==============================================================================
