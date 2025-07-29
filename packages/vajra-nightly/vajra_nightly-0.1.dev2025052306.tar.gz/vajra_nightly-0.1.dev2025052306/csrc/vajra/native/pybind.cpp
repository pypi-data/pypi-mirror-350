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
#include "native/configs/ConfigsPybind.h"
#include "native/core/CorePybind.h"
#include "native/core/scheduler/SchedulerPybind.h"
#include "native/data_structures/DataStructuresPybind.h"
#include "native/datatypes/DatatypesPybind.h"
#include "native/engine/EnginePybind.h"
#include "native/enums/EnumsPybind.h"
#include "native/metrics_store/MetricsStorePybind.h"
#include "native/model_executor/ModelExecutorPybind.h"
#include "native/transfer_engine/TransferEnginePybind.h"
#include "native/utils/UtilsPybind.h"
#include "native/worker/WorkerPybind.h"
//==============================================================================
namespace pybind11 {
namespace detail {
template <>
struct type_caster<std::set<int>> {
 public:
  PYBIND11_TYPE_CASTER(std::set<int>, _("Set[int]"));
  bool load(handle src, bool) {
    if (!py::isinstance<py::set>(src) && !py::isinstance<py::frozenset>(src))
      return false;
    for (auto item : src) {
      if (!py::isinstance<py::int_>(item)) return false;
      value.insert(item.cast<int>());
    }
    return true;
  }
  static handle cast(const std::set<int>& src, return_value_policy, handle) {
    py::set s;
    for (int v : src) s.add(py::cast(v));
    return s.release();
  }
};
}  // namespace detail
}  // namespace pybind11
namespace vajra {
//==============================================================================
PYBIND11_MODULE(TORCH_EXTENSION_NAME, m) {
  google::InitGoogleLogging("vajra-native");
  Logger::InitializeLogLevel();

  InitConfigsPybindSubmodule(m);
  InitCorePybindSubmodule(m);
  InitDataStructuresPybindSubmodule(m);
  InitEnumsPybindSubmodule(m);
  InitDatatypesPybindSubmodule(m);
  InitModelExecutorPybindSubmodule(m);
  InitMetricsStorePybindSubmodule(m);
  InitUtilsPybindSubmodule(m);
  InitTransferEnginePybindSubmodule(m);
  InitEnginePybindSubmodule(m);
  InitWorkerPybindSubmodule(m);
}
//==============================================================================
}  // namespace vajra
//==============================================================================
