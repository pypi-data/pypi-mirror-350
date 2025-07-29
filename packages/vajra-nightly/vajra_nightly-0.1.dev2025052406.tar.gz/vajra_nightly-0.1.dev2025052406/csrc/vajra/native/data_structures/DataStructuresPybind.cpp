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
#include "native/data_structures/DataStructuresPybind.h"
//==============================================================================
#include "native/data_structures/Queues.h"
#include "native/datatypes/BaseSequenceWithPriority.h"
#include "native/datatypes/RequestOutput.h"
#include "native/datatypes/Sequence.h"
//==============================================================================
namespace vajra {
//==============================================================================
template <typename T>
void InitQueuePybindClass(py::module_& m, const std::string& name) {
  py::class_<Queue<T>, std::shared_ptr<Queue<T>>>(m, name.c_str())
      .def(py::init<>())
      .def("empty", [](Queue<T>& queue) { return queue.empty(); })
      .def(
          "put", [](Queue<T>& queue, const T& item) { queue.push(item); },
          py::arg("item"))
      .def(
          "get",
          [](Queue<T>& queue, bool block) {
            if (block) {
              // Release GIL for blocking operations
              py::gil_scoped_release release;
              return queue.pull();
            } else {
              // Try to get without blocking
              T result;
              boost::concurrent::queue_op_status status =
                  queue.try_pull(result);
              if (status == boost::concurrent::queue_op_status::success) {
                return result;
              }
              throw py::index_error("Queue is empty");
            }
          },
          py::arg("block") = true);
}
//==============================================================================
template <typename T, typename Container, typename Comparator>
void InitPriorityQueuePybindClass(py::module_& m, const std::string& name) {
  py::class_<PriorityQueue<T, Container, Comparator>,
             std::shared_ptr<PriorityQueue<T, Container, Comparator>>>(
      m, name.c_str())
      .def(py::init<>())
      .def("empty",
           [](PriorityQueue<T, Container, Comparator>& queue) {
             return queue.empty();
           })
      .def(
          "put",
          [](PriorityQueue<T, Container, Comparator>& queue, const T& item) {
            queue.push(item);
          },
          py::arg("item"))
      .def(
          "get",
          [](PriorityQueue<T, Container, Comparator>& queue, bool block) {
            if (block) {
              // Release GIL for blocking operations
              py::gil_scoped_release release;
              return queue.pull();
            } else {
              // Try to get without blocking
              T result;
              boost::concurrent::queue_op_status status =
                  queue.try_pull(result);
              if (status == boost::concurrent::queue_op_status::success) {
                return result;
              }
              throw py::index_error("Queue is empty");
            }
          },
          py::arg("block") = true);
}
//==============================================================================
void InitQueuesPybindClass(py::module_& m) {
  // Regular queues
  InitQueuePybindClass<UserSequenceParamsPtr>(m, "UserSequenceParamQueue");
  InitQueuePybindClass<RequestOutputPtr>(m, "RequestOutputQueue");

  // Priority queue
  InitPriorityQueuePybindClass<MutableBaseSequenceWithPriorityPtr,
                               MutableBaseSequenceWithPriorityPtrList,
                               BaseSequenceWithPriorityComparator>(
      m, "SequencePriorityQueue");
}
//==============================================================================
void InitDataStructuresPybindSubmodule(py::module_& pm) {
  auto m = pm.def_submodule("data_structures", "Data Structures submodule");

  // Call individual binding functions
  InitQueuesPybindClass(m);
}
//==============================================================================
}  // namespace vajra
//==============================================================================
