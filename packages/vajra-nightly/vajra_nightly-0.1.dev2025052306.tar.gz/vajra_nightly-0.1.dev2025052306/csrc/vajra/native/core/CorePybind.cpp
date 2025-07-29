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
#include "native/core/CorePybind.h"
//==============================================================================
#include "native/core/block_space_manager/BlockSpaceManagerPybind.h"
#include "native/core/controller/ControllerPybind.h"
#include "native/core/scheduler/SchedulerPybind.h"
#include "native/core/sequence_manager/SequenceManagerPybind.h"
#include "native/core/tokenizer/TokenizerPybind.h"
//==============================================================================
namespace vajra {
//==============================================================================
void InitCorePybindSubmodule(py::module& pm) {
  auto m = pm.def_submodule("core", "Core submodule");

  InitBlockSpaceManagerPybindSubmodule(m);
  InitSequenceManagerPybindSubmodule(m);
  InitSchedulerPybindSubmodule(m);
  InitTokenizerPybindSubmodule(m);
  InitControllerPybindSubmodule(m);
}
//==============================================================================
}  // namespace vajra
//==============================================================================
