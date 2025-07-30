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
#include "native/core/block_space_manager/BlockSpaceManager.h"
//==============================================================================
namespace vajra {
//==============================================================================
void InitBlockSpaceManagerPybindClass(py::module_& m) {
  py::class_<BlockSpaceManager, std::shared_ptr<BlockSpaceManager>>(
      m, "BlockSpaceManager")
      .def(py::init<int, int, int, float>(), py::arg("block_size"),
           py::arg("num_gpu_blocks"), py::arg("max_model_len"),
           py::arg("watermark") = 0.01f)
      .def("can_allocate_blocks", &BlockSpaceManager::CanAllocateBlocks)
      .def("allocate", &BlockSpaceManager::Allocate)
      .def("allocate_delta", &BlockSpaceManager::AllocateDelta)
      .def("can_append_slot", &BlockSpaceManager::CanAppendSlot)
      .def("append_slot", &BlockSpaceManager::AppendSlot)
      .def("free", &BlockSpaceManager::Free)
      .def("get_block_table", &BlockSpaceManager::GetBlockTableCopy)
      .def("is_allocated", &BlockSpaceManager::IsAllocated);
}
//==============================================================================
void InitBlockSpaceManagerPybindSubmodule(py::module& pm) {
  auto m =
      pm.def_submodule("block_space_manger", "BlockSpaceManager submodule");
  InitBlockSpaceManagerPybindClass(m);
}
//==============================================================================
}  // namespace vajra
//==============================================================================
