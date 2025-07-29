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
#include "commons/StdCommon.h"
#include "native/datatypes/BaseSequenceWithPriority.h"
#include "native/datatypes/RequestOutput.h"
#include "native/datatypes/Sequence.h"
//==============================================================================
namespace vajra {
//==============================================================================
using UserSequenceParamQueue = Queue<UserSequenceParamsPtr>;
using UserSequenceParamQueuePtr = std::shared_ptr<UserSequenceParamQueue>;

using SequencePriorityQueue =
    PriorityQueue<MutableBaseSequenceWithPriorityPtr,
                  MutableBaseSequenceWithPriorityPtrList,
                  BaseSequenceWithPriorityComparator>;
using SequencePriorityQueuePtr = std::shared_ptr<SequencePriorityQueue>;

using RequestOutputQueue = Queue<RequestOutputPtr>;
using RequestOutputQueuePtr = std::shared_ptr<RequestOutputQueue>;
//==============================================================================
}  // namespace vajra
//==============================================================================
