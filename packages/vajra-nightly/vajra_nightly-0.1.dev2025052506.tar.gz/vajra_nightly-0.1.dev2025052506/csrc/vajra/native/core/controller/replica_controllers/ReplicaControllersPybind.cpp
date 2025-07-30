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
#include "native/core/controller/replica_controllers/BaseLlmReplicaController.h"
#include "native/core/controller/replica_controllers/PipelineParallelLlmReplicaController.h"
#include "native/data_structures/Queues.h"
#include "native/datatypes/CommInfo.h"
//==============================================================================
namespace vajra {
//==============================================================================
void InitBaseLlmReplicaControllerPybindClass(py::module& m) {
  py::class_<BaseLlmReplicaController,
             std::shared_ptr<BaseLlmReplicaController>>(
      m, "BaseLlmReplicaController")
      .def(py::init<ReplicaId, std::shared_ptr<LlmReplicaControllerConfig>,
                    std::shared_ptr<BaseRequestPrioritizer>, CommInfoPtr,
                    SequencePriorityQueuePtr, RequestOutputQueuePtr,
                    std::shared_ptr<BaseReplicaScheduler>,
                    std::shared_ptr<EngineSequenceManager>,
                    EngineMetricsStorePtr>());
}
//==============================================================================
void InitPipelineParallelLlmReplicaControllerPybindClass(py::module& m) {
  py::class_<PipelineParallelLlmReplicaController,
             std::shared_ptr<PipelineParallelLlmReplicaController>>(
      m, "PipelineParallelLlmReplicaController")
      .def(py::init<ReplicaId, std::shared_ptr<LlmReplicaControllerConfig>,
                    std::shared_ptr<BaseRequestPrioritizer>, CommInfoPtr,
                    SequencePriorityQueuePtr, RequestOutputQueuePtr,
                    std::shared_ptr<BaseReplicaScheduler>,
                    std::shared_ptr<EngineSequenceManager>,
                    EngineMetricsStorePtr>());
}
//==============================================================================
void InitReplicaControllersPybindSubmodule(py::module& pm) {
  auto m = pm.def_submodule("replica_controllers");

  InitBaseLlmReplicaControllerPybindClass(m);
  InitPipelineParallelLlmReplicaControllerPybindClass(m);
}
//==============================================================================
}  // namespace vajra
//==============================================================================
