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
#include "native/transfer_engine/backend/TransferEngineBackendPybind.h"

#include "native/transfer_engine/backend/TorchTransferEngine.h"
#include "native/transfer_engine/backend/TorchTransferWork.h"
#include "native/transfer_engine/backend/TransferEngineUtils.h"
//==============================================================================
namespace vajra {
//==============================================================================
void InitTorchTransferEnginePybindClass(py::module_& m) {
  // Bind the TorchTransferEngine class
  py::class_<TorchTransferEngine, BaseTransferEngine,
             std::shared_ptr<TorchTransferEngine>>(m, "TorchTransferEngine")
      .def(py::init<std::size_t, GlobalResourceConfig,
                    const c10::intrusive_ptr<c10d::ProcessGroup>>(),
           py::arg("global_rank"), py::arg("global_resource_config"),
           py::arg("global_process_group"));
}
//==============================================================================
void InitTransferEngineUtilsPybindClass(py::module_& m) {
  py::class_<vajra::TransferEngineUtils>(m, "TransferEngineUtils")
      .def_static("copy_merge_pages_cache",
                  &vajra::TransferEngineUtils::CopyMergePagesCache);
}
//==============================================================================
void InitTransferEngineBackendPybindSubmodule(py::module& m) {
  auto transfer_engine_module =
      m.def_submodule("backend", "Transfer engine backend module");

  InitTorchTransferEnginePybindClass(transfer_engine_module);
  InitTransferEngineUtilsPybindClass(transfer_engine_module);
}
//==============================================================================
}  // namespace vajra
//==============================================================================
