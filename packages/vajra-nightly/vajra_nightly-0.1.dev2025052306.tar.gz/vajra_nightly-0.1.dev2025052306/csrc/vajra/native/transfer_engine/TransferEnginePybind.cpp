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
#include "native/transfer_engine/TransferEnginePybind.h"
//==============================================================================
#include "commons/TorchCommon.h"
#include "native/configs/TransferEngineConfig.h"
#include "native/transfer_engine/backend/TransferEngineBackendPybind.h"
#include "native/transfer_engine/factory/TransferEngineFactory.h"
#include "native/transfer_engine/interface/TransferEngineInterfacePybind.h"
//==============================================================================
namespace vajra {
//==============================================================================
void InitTransferEnginePybindSubmodule(py::module_& pm) {
  auto m = pm.def_submodule("transfer_engine", "TransferEngine submodule");
  InitTransferEngineInterfacePybindSubmodule(m);
  InitTransferEngineBackendPybindSubmodule(m);
}
//==============================================================================
}  // namespace vajra
//==============================================================================
