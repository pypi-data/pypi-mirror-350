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
#include "commons/ClassTraits.h"
#include "native/configs/ReplicasetSchedulerConfig.h"
#include "native/core/Types.h"
#include "native/data_structures/Queues.h"
#include "native/datatypes/BaseSequenceWithPriority.h"
//==============================================================================
namespace vajra {
//==============================================================================
class BaseReplicasetScheduler : public NonCopyableNonMovable {
 public:
  BaseReplicasetScheduler(std::shared_ptr<BaseReplicasetSchedulerConfig> config,
                          std::size_t num_replicas)
      : config_(config), num_replicas_(num_replicas) {}

  virtual ~BaseReplicasetScheduler() = default;

  [[nodiscard]] virtual SequencePriorityQueuePtr GetReplicaQueue(
      ReplicaId replica_id) const = 0;

  virtual void Schedule(const MutableBaseSequenceWithPriorityPtr& seq) = 0;

 protected:
  std::shared_ptr<BaseReplicasetSchedulerConfig> config_;
  std::size_t num_replicas_;
};
//==============================================================================
}  // namespace vajra
//==============================================================================
