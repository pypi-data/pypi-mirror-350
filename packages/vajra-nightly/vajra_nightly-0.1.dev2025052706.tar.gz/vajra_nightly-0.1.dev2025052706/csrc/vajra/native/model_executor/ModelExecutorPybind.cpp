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
#include "native/model_executor/ModelExecutorPybind.h"
//==============================================================================
#include "native/model_executor/LLMModelRunner.h"
#include "native/model_executor/layers/LayersPybind.h"
#include "native/model_executor/models/ModelsPybind.h"
#include "native/model_executor/parallel_utils/ParallelUtilsPybind.h"
//==============================================================================
namespace vajra {
//==============================================================================
// Trampoline class for BaseModelRunner
class PyBaseModelRunner : public BaseModelRunner {
 public:
  // Inherit constructors from BaseModelRunner so that Python can call them.
  using BaseModelRunner::BaseModelRunner;

  PreparedInputs PrepareInputs(
      const Sequences& seqs,
      const SequenceMetadataVector& seq_metadata_list) const override {
    PYBIND11_OVERRIDE_PURE_NAME(
        PreparedInputs,          // Return type
        BaseModelRunner,         // Parent class
        "_prepare_inputs",       // Name of function in Python
        PrepareInputs,           // Name of function in C++
        seqs, seq_metadata_list  // Arguments
    );
  }

  SamplerOutputs Run(const Sequences& seqs,
                     const SequenceMetadataVector& seq_metadata_list,
                     std::vector<torch::Tensor>& gpu_caches) override {
    PYBIND11_OVERRIDE_PURE_NAME(SamplerOutputs,   // Return type
                                BaseModelRunner,  // Parent class
                                "run",            // Name of function in Python
                                Run,              // Name of function in C++
                                seqs, seq_metadata_list,
                                gpu_caches  // Arguments
    );
  }
};
//==============================================================================
void InitBaseModelRunnerPybindClass(py::module_& m) {
  py::class_<BaseModelRunner, PyBaseModelRunner,
             std::shared_ptr<BaseModelRunner>>(m, "BaseModelRunner")
      .def(py::init<std::shared_ptr<BaseReplicaControllerConfig>, torch::Device,
                    std::size_t, BaseModelPtr, ProcessGroupWrapperPtr,
                    WorkerMetricsStorePtr>(),
           py::arg("config"), py::arg("device"), py::arg("rank"),
           py::arg("model"), py::arg("process_group_wrapper"),
           py::arg("worker_metrics_store"))
      .def("_prepare_inputs", &BaseModelRunner::PrepareInputs)
      .def("run", &BaseModelRunner::Run);
}
//==============================================================================
void InitLLMModelRunnerPybindClass(py::module& pm) {
  py::class_<LLMModelRunner, BaseModelRunner, std::shared_ptr<LLMModelRunner>>(
      pm, "LLMModelRunner")
      .def(py::init<std::shared_ptr<BaseReplicaControllerConfig>, torch::Device,
                    std::size_t, BaseModelPtr, ProcessGroupWrapperPtr,
                    WorkerMetricsStorePtr, SamplerPtr>(),
           py::arg("config"), py::arg("device"), py::arg("rank"),
           py::arg("model"), py::arg("process_group_wrapper"),
           py::arg("worker_metrics_store"), py::arg("sampler"))
      .def("_prepare_inputs", &LLMModelRunner::PrepareInputs)
      .def("run", &LLMModelRunner::Run);
}
//==============================================================================
void InitModelExecutorPybindSubmodule(py::module_& pm) {
  auto m = pm.def_submodule("model_executor", "Model executor submodule");

  InitBaseModelRunnerPybindClass(m);
  InitLLMModelRunnerPybindClass(m);
  InitLayersPybindSubmodule(m);
  InitModelsPybindSubmodule(m);
  InitParallelUtilsPybindSubmodule(m);
}
//==============================================================================
}  // namespace vajra
//==============================================================================
