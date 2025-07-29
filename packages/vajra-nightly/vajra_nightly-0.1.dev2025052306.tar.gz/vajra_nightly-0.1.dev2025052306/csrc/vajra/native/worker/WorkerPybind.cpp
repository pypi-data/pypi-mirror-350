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
#include "native/worker/WorkerPybind.h"
//==============================================================================
#include "native/worker/BaseLLMWorker.h"
#include "native/worker/BaseWorker.h"
#include "native/worker/PipelineParallelLLMWorker.h"
//==============================================================================
namespace vajra {
//==============================================================================
// Trampoline class for BaseWorker to enable Python subclassing
class PyBaseWorker : public BaseWorker {
 public:
  using BaseWorker::BaseWorker;

  SamplerOutputs ExecuteModel(SchedulerOutputPtr scheduler_output /*[in]*/
                              ) override {
    PYBIND11_OVERRIDE_PURE_NAME(SamplerOutputs,    // Return type
                                BaseWorker,        // Parent class
                                "_execute_model",  // Python name
                                ExecuteModel,      // C++ name
                                scheduler_output   // Argument list
    );
  }

  void ExecutionLoop() override {
    PYBIND11_OVERRIDE_PURE_NAME(void,               // Return type
                                BaseWorker,         // Parent class
                                "_execution_loop",  // Python name
                                ExecutionLoop,      // C++ name
    );
  }
};

// Initialize BaseWorker pybind
void InitBaseWorkerPybind(py::module& m) {
  py::class_<BaseWorker, PyBaseWorker, BaseWorkerPtr>(m, "BaseWorker")
      .def(py::init<ReplicaId, std::size_t, ZmqSocketPtr, ZmqSocketPtr,
                    WorkerSequenceManagerPtr, WorkerMetricsStorePtr,
                    BaseModelRunnerPtr>())
      .def("execute_model", &BaseWorker::ExecuteModel)
      .def("_execution_loop", &BaseWorker::ExecutionLoop);
}

// Initialize BaseLLMWorker pybind
void InitBaseLLMWorkerPybind(py::module& m) {
  py::class_<BaseLLMWorker, BaseWorker, BaseLLMWorkerPtr>(m, "BaseLLMWorker")
      .def(py::init<ReplicaId, std::size_t, ZmqSocketPtr, ZmqSocketPtr,
                    WorkerSequenceManagerPtr, WorkerMetricsStorePtr,
                    BaseModelRunnerPtr, std::vector<torch::Tensor>,
                    ProcessGroupWrapperPtr>())
      .def("execute_model", &BaseLLMWorker::ExecuteModel)
      .def("_execution_loop", &BaseLLMWorker::ExecutionLoop,
           py::call_guard<py::gil_scoped_release>());
}

// Initialize PipelineParallelLLMWorker pybind
void InitPipelineParallelLLMWorkerPybind(py::module& m) {
  py::class_<PipelineParallelLLMWorker, BaseLLMWorker,
             PipelineParallelLLMWorkerPtr>(m, "PipelineParallelLLMWorker")
      .def(py::init<ReplicaId, std::size_t, ZmqSocketPtr, ZmqSocketPtr,
                    WorkerSequenceManagerPtr, WorkerMetricsStorePtr,
                    BaseModelRunnerPtr, std::vector<torch::Tensor>,
                    ProcessGroupWrapperPtr, ZmqSocketPtr>())
      .def("execute_model", &PipelineParallelLLMWorker::ExecuteModel)
      .def("_execution_loop", &PipelineParallelLLMWorker::ExecutionLoop,
           py::call_guard<py::gil_scoped_release>());
}

// Initialize Worker pybind submodule
void InitWorkerPybindSubmodule(py::module& m) {
  py::module worker_module =
      m.def_submodule("worker", "Worker module for Vajra");

  InitBaseWorkerPybind(worker_module);
  InitBaseLLMWorkerPybind(worker_module);
  InitPipelineParallelLLMWorkerPybind(worker_module);
}
//==============================================================================
}  // namespace vajra
//==============================================================================
