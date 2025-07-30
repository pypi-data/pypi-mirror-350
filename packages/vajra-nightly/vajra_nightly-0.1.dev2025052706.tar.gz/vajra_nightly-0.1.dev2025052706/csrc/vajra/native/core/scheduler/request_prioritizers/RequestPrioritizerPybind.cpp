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

#include "vidur/execution_time_predictor/execution_time_predictor.h"
//==============================================================================
#include "native/core/scheduler/request_prioritizers/RequestPrioritizerPybind.h"
//==============================================================================
#include "native/configs/ParallelConfig.h"
#include "native/configs/ReplicaSchedulerConfig.h"
#include "native/configs/RequestPrioritizerConfig.h"
#include "native/core/scheduler/request_prioritizers/BaseRequestPrioritizer.h"
#include "native/core/scheduler/request_prioritizers/EdfRequestPrioritizer.h"
#include "native/core/scheduler/request_prioritizers/FcfsRequestPrioritizer.h"
#include "native/core/scheduler/request_prioritizers/LrsRequestPrioritizer.h"
//==============================================================================
namespace vajra {
//==============================================================================
using ExecutionTimePredictor =
    vidur::execution_time_predictor::ExecutionTimePredictor;
//==============================================================================
class PyRequestPrioritizer : public BaseRequestPrioritizer {
 public:
  [[nodiscard]] MutableBaseSequenceWithPriorityPtr GetSeqWithPriority(
      MutableSequencePtr seq) override {
    PYBIND11_OVERRIDE(MutableBaseSequenceWithPriorityPtr,
                      BaseRequestPrioritizer, GetSeqWithPriority, seq);
  }
};
//==============================================================================
void InitBaseRequestPrioritizerPybindClass(py::module_& m) {
  py::class_<BaseRequestPrioritizer, PyRequestPrioritizer,
             std::shared_ptr<BaseRequestPrioritizer>>(m,
                                                      "BaseRequestPrioritizer")
      .def("get_seq_with_priority",
           &BaseRequestPrioritizer::GetSeqWithPriority);
}
//==============================================================================
void InitFcfsRequestPrioritizerPybindClass(py::module_& m) {
  py::class_<FcfsRequestPrioritizer, BaseRequestPrioritizer,
             std::shared_ptr<FcfsRequestPrioritizer>>(m,
                                                      "FcfsRequestPrioritizer")
      .def(py::init<>());
}
//==============================================================================
void InitEdfRequestPrioritizerPybindClass(py::module_& m) {
  py::class_<EdfRequestPrioritizer, BaseRequestPrioritizer,
             std::shared_ptr<EdfRequestPrioritizer>>(m, "EdfRequestPrioritizer")
      .def(py::init<const EdfRequestPrioritizerConfig&, const ParallelConfig&,
                    const std::shared_ptr<BaseReplicaSchedulerConfig>&,
                    const std::shared_ptr<ExecutionTimePredictor>&>(),
           py::arg("config"), py::arg("parallel_config"),
           py::arg("replica_scheduler_config"),
           py::arg("execution_time_predictor"));
}
//==============================================================================
void InitLrsRequestPrioritizerPybindClass(py::module_& m) {
  py::class_<LrsRequestPrioritizer, EdfRequestPrioritizer,
             std::shared_ptr<LrsRequestPrioritizer>>(m, "LrsRequestPrioritizer")
      .def(py::init<const LrsRequestPrioritizerConfig&, const ParallelConfig&,
                    const std::shared_ptr<BaseReplicaSchedulerConfig>&,
                    const std::shared_ptr<ExecutionTimePredictor>&>(),
           py::arg("config"), py::arg("parallel_config"),
           py::arg("replica_scheduler_config"),
           py::arg("execution_time_predictor"));
}
//==============================================================================
void InitRequestPrioritizerPybindSubmodule(py::module_& pm) {
  auto m =
      pm.def_submodule("request_prioritizers", "Request prioritizer submodule");

  InitBaseRequestPrioritizerPybindClass(m);
  InitFcfsRequestPrioritizerPybindClass(m);
  InitEdfRequestPrioritizerPybindClass(m);
  InitLrsRequestPrioritizerPybindClass(m);
}
//==============================================================================
}  // namespace vajra
//==============================================================================
