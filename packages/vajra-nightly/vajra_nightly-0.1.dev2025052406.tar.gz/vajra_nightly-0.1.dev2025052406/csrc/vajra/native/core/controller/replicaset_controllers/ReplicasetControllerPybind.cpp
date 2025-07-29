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
#include "native/core/controller/replicaset_controllers/ReplicasetControllerPybind.h"
//==============================================================================
#include "commons/TorchCommon.h"
#include "native/core/controller/replicaset_controllers/LlmReplicasetController.h"
#include "native/data_structures/Queues.h"
//==============================================================================
namespace vajra {
//==============================================================================
void InitReplicasetControllerPybindSubmodule(py::module& pm) {
  auto m = pm.def_submodule("replicaset_controllers");

  py::class_<
      LlmReplicasetController<UserSequenceParamQueue, RequestOutputQueue>,
      std::shared_ptr<
          LlmReplicasetController<UserSequenceParamQueue, RequestOutputQueue>>>(
      m, "LlmReplicasetController")
      .def(py::init<std::shared_ptr<LlmReplicasetControllerConfig>,
                    const std::string&, TokenId, UserSequenceParamQueuePtr,
                    RequestOutputQueuePtr,
                    std::shared_ptr<BaseRequestPrioritizer>,
                    std::shared_ptr<BaseReplicasetScheduler>>());
}
//==============================================================================
}  // namespace vajra
//==============================================================================
