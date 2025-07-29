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
#include "native/model_executor/parallel_utils/ParallelUtilsPybind.h"
//==============================================================================
#include "commons/TorchCommon.h"
#include "native/model_executor/parallel_utils/ProcessGroupWrapper.h"
//==============================================================================
namespace vajra {
//==============================================================================
void InitProcessGroupWrapperPybindClass(py::module_& m) {
  py::class_<ProcessGroupWrapper, std::shared_ptr<ProcessGroupWrapper>>(
      m, "ProcessGroupWrapper")
      .def(py::init<c10::intrusive_ptr<c10d::ProcessGroup>,
                    c10::intrusive_ptr<c10d::ProcessGroup>,
                    c10::intrusive_ptr<c10d::ProcessGroup>>(),
           py::arg("tensor_model_parallel_group"),
           py::arg("pipeline_model_parallel_group"),
           py::arg("kv_parallel_group"))
      .def("get_tensor_model_parallel_group",
           &ProcessGroupWrapper::GetTensorModelParallelGroup)
      .def("get_pipeline_model_parallel_group",
           &ProcessGroupWrapper::GetPipelineModelParallelGroup)
      .def("get_kv_parallel_group", &ProcessGroupWrapper::GetKvParallelGroup)
      .def("is_pipeline_first_stage",
           &ProcessGroupWrapper::IsPipelineFirstStage)
      .def("is_pipeline_last_stage", &ProcessGroupWrapper::IsPipelineLastStage)
      .def("get_pipeline_model_parallel_prev_rank",
           &ProcessGroupWrapper::GetPipelineModelParallelPrevRank)
      .def("get_pipeline_model_parallel_next_rank",
           &ProcessGroupWrapper::GetPipelineModelParallelNextRank);
}
//==============================================================================
void InitParallelUtilsPybindSubmodule(py::module& pm) {
  auto m = pm.def_submodule("parallel_utils", "Parallel Utils submodule");

  InitProcessGroupWrapperPybindClass(m);
}
//==============================================================================
}  // namespace vajra
//==============================================================================
