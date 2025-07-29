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
#include "commons/Logging.h"
//==============================================================================
namespace vajra {
//==============================================================================
template <typename WaitingQueueType, typename OutputQueueType>
class AbstractController : public NonCopyableNonMovable {
  static_assert(is_boost_queue<WaitingQueueType>::value,
                "WaitingQueueType must be either boost::sync_queue or "
                "boost::sync_priority_queue");
  static_assert(is_boost_queue<OutputQueueType>::value,
                "OutputQueueType must be either boost::sync_queue or "
                "boost::sync_priority_queue");

 public:
  AbstractController(std::shared_ptr<WaitingQueueType> waiting_seq_queue,
                     std::shared_ptr<OutputQueueType> output_queue)
      : waiting_seq_queue_(waiting_seq_queue), output_queue_(output_queue) {
    ASSERT_VALID_POINTER_ARGUMENT(waiting_seq_queue);
    ASSERT_VALID_POINTER_ARGUMENT(output_queue);
  }

  virtual ~AbstractController() = default;

 protected:
  std::shared_ptr<WaitingQueueType> waiting_seq_queue_;
  std::shared_ptr<OutputQueueType> output_queue_;
};
//==============================================================================
}  // namespace vajra
//==============================================================================
