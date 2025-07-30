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
#include "native/enums/EnumsPybind.h"
//==============================================================================
#include "native/enums/Enums.h"
//==============================================================================
namespace vajra {
//==============================================================================
void InitReplicasetSchedulerTypePybindEnum(py::module_& m) {
  py::enum_<ReplicasetSchedulerType>(m, "ReplicasetSchedulerType")
      .value("PULL", ReplicasetSchedulerType::PULL)
      .value("ROUND_ROBIN", ReplicasetSchedulerType::ROUND_ROBIN);
}
//==============================================================================
void InitReplicasetControllerTypePybindEnum(py::module_& m) {
  py::enum_<ReplicasetControllerType>(m, "ReplicasetControllerType")
      .value("LLM", ReplicasetControllerType::LLM);
}
//==============================================================================
void InitReplicaControllerTypePybindEnum(py::module_& m) {
  py::enum_<ReplicaControllerType>(m, "ReplicaControllerType")
      .value("LLM_BASE", ReplicaControllerType::LLM_BASE)
      .value("LLM_PIPELINE_PARALLEL",
             ReplicaControllerType::LLM_PIPELINE_PARALLEL);
}
//==============================================================================
void InitReplicaSchedulerTypePybindEnum(py::module_& m) {
  py::enum_<ReplicaSchedulerType>(m, "ReplicaSchedulerType")
      .value("FIXED_CHUNK", ReplicaSchedulerType::FIXED_CHUNK)
      .value("DYNAMIC_CHUNK", ReplicaSchedulerType::DYNAMIC_CHUNK)
      .value("SPACE_SHARING", ReplicaSchedulerType::SPACE_SHARING);
}
//==============================================================================
void InitRequestPrioritizerTypePybindEnum(py::module_& m) {
  py::enum_<RequestPrioritizerType>(m, "RequestPrioritizerType")
      .value("FCFS", RequestPrioritizerType::FCFS)
      .value("EDF", RequestPrioritizerType::EDF)
      .value("LRS", RequestPrioritizerType::LRS);
}
//==============================================================================
void InitTransferBackendTypePybindEnum(py::module_& m) {
  py::enum_<TransferBackendType>(m, "TransferBackendType")
      .value("TORCH", TransferBackendType::TORCH);
  py::enum_<TransferOperationRanksType>(m, "TransferOperationRanksType")
      .value("MATCHING", TransferOperationRanksType::MATCHING)
      .value("ALL", TransferOperationRanksType::ALL)
      .value("SINGLE", TransferOperationRanksType::SINGLE);
}
//==============================================================================
void InitMetricsStoreTypePybindEnum(py::module_& m) {
  py::enum_<MetricsStoreType>(m, "MetricsStoreType")
      .value("ENGINE", MetricsStoreType::ENGINE)
      .value("WORKER", MetricsStoreType::WORKER);
}
//==============================================================================
void InitZmqConstantsPybindEnum(py::module_& m) {
  py::enum_<ZmqConstants>(m, "ZmqConstants")
      .value("PUB", ZmqConstants::PUB)
      .value("SUB", ZmqConstants::SUB)
      .value("PUSH", ZmqConstants::PUSH)
      .value("PULL", ZmqConstants::PULL)
      .value("SUBSCRIBE", ZmqConstants::SUBSCRIBE);
}
//==============================================================================
void InitEnumsPybindSubmodule(py::module_& pm) {
  auto m = pm.def_submodule("enums", "Enums submodule");

  InitReplicasetSchedulerTypePybindEnum(m);
  InitReplicasetControllerTypePybindEnum(m);
  InitReplicaControllerTypePybindEnum(m);
  InitReplicaSchedulerTypePybindEnum(m);
  InitRequestPrioritizerTypePybindEnum(m);
  InitMetricsStoreTypePybindEnum(m);
  InitTransferBackendTypePybindEnum(m);
  InitZmqConstantsPybindEnum(m);
}
//==============================================================================
}  // namespace vajra
//==============================================================================
