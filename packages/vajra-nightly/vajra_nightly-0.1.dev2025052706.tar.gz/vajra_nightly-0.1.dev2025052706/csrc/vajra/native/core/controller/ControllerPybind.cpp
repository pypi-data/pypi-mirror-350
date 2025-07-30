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
#include "commons/TorchCommon.h"
#include "native/core/controller/replica_controllers/ReplicaControllersPybind.h"
#include "native/core/controller/replicaset_controllers/ReplicasetControllerPybind.h"
//==============================================================================
namespace vajra {
//==============================================================================
void InitControllerPybindSubmodule(py::module& m) {
  auto controller_module = m.def_submodule("controller");

  InitReplicasetControllerPybindSubmodule(controller_module);
  InitReplicaControllersPybindSubmodule(controller_module);
}
//==============================================================================
}  // namespace vajra
//==============================================================================
