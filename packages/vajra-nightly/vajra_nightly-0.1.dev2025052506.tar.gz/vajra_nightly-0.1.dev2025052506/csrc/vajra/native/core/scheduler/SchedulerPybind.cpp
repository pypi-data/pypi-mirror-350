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
#include "native/core/scheduler/SchedulerPybind.h"
//==============================================================================
#include "commons/TorchCommon.h"
#include "native/core/scheduler/replica_schedulers/ReplicaSchedulerPybind.h"
#include "native/core/scheduler/replicaset_schedulers/ReplicasetSchedulerPybind.h"
#include "native/core/scheduler/request_prioritizers/RequestPrioritizerPybind.h"
//==============================================================================
namespace vajra {
//==============================================================================
void InitSchedulerPybindSubmodule(py::module& m) {
  auto scheduler_module = m.def_submodule("scheduler");

  InitReplicaSchedulerPybindSubmodule(scheduler_module);
  InitReplicasetSchedulerPybindSubmodule(scheduler_module);
  InitRequestPrioritizerPybindSubmodule(scheduler_module);
}
//==============================================================================
}  // namespace vajra
//==============================================================================
