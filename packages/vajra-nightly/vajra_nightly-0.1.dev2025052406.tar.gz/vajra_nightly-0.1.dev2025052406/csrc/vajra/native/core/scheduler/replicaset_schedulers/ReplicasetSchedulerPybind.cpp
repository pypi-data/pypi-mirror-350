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
#include "native/core/scheduler/replicaset_schedulers/ReplicasetSchedulerPybind.h"
//==============================================================================
#include "commons/TorchCommon.h"
#include "native/core/scheduler/replicaset_schedulers/BaseReplicasetScheduler.h"
#include "native/core/scheduler/replicaset_schedulers/PullReplicasetScheduler.h"
#include "native/core/scheduler/replicaset_schedulers/RoundRobinReplicasetScheduler.h"
//==============================================================================
namespace vajra {
//==============================================================================
class PyReplicasetScheduler : public BaseReplicasetScheduler {
 public:
  [[nodiscard]] SequencePriorityQueuePtr GetReplicaQueue(
      ReplicaId replica_id) const override {
    PYBIND11_OVERRIDE(SequencePriorityQueuePtr, BaseReplicasetScheduler,
                      GetReplicaQueue, replica_id);
  }

  void Schedule(const MutableBaseSequenceWithPriorityPtr& seq) override {
    PYBIND11_OVERRIDE(void, BaseReplicasetScheduler, Schedule, seq);
  }
};
//==============================================================================
void InitBaseReplicasetSchedulerPybindClass(py::module& pm) {
  py::class_<BaseReplicasetScheduler, PyReplicasetScheduler,
             std::shared_ptr<BaseReplicasetScheduler>>(
      pm, "BaseReplicasetScheduler")
      .def("get_replica_queue", &BaseReplicasetScheduler::GetReplicaQueue)
      .def("schedule", &BaseReplicasetScheduler::Schedule);
}
//==============================================================================
void InitPullReplicasetSchedulerPybindClass(py::module& pm) {
  py::class_<PullReplicasetScheduler, BaseReplicasetScheduler,
             std::shared_ptr<PullReplicasetScheduler>>(
      pm, "PullReplicasetScheduler")
      .def(py::init<std::shared_ptr<PullReplicasetSchedulerConfig>,
                    std::size_t>(),
           py::arg("config"), py::arg("num_replicas"));
}
//==============================================================================
void InitRoundRobinReplicasetSchedulerPybindClass(py::module& pm) {
  py::class_<RoundRobinReplicasetScheduler, BaseReplicasetScheduler,
             std::shared_ptr<RoundRobinReplicasetScheduler>>(
      pm, "RoundRobinReplicasetScheduler")
      .def(py::init<std::shared_ptr<RoundRobinReplicasetSchedulerConfig>,
                    std::size_t>(),
           py::arg("config"), py::arg("num_replicas"));
}
//==============================================================================
void InitReplicasetSchedulerPybindSubmodule(py::module& pm) {
  auto m = pm.def_submodule("replicaset_schedulers",
                            "ReplicasetScheduler submodule");

  InitBaseReplicasetSchedulerPybindClass(m);
  InitPullReplicasetSchedulerPybindClass(m);
  InitRoundRobinReplicasetSchedulerPybindClass(m);
}
//==============================================================================
}  // namespace vajra
//==============================================================================
