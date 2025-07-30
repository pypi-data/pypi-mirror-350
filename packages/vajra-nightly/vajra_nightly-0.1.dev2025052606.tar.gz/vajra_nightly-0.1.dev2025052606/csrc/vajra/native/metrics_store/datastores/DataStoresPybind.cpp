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
#include "native/metrics_store/datastores/DataStoresPybind.h"
//==============================================================================
#include "native/core/Types.h"
#include "native/metrics_store/datastores/BaseCdfDataStore.h"
#include "native/metrics_store/datastores/LabeledCdfDataStore.h"
#include "native/metrics_store/datastores/TimeSeriesDataStore.h"
#include "native/metrics_store/datastores/UnlabeledCdfDataStore.h"
//==============================================================================
namespace vajra {
//==============================================================================
// Define a_trampoline class for the abstract base class

class PyCdfDataStore : public BaseCdfDataStore {
 public:
  // Add a data point to the datastore (abstract)
  void Put(const std::string& label, float value) override {
    PYBIND11_OVERRIDE(void, BaseCdfDataStore, Put, label, value);
  }

  // Merge another datastore into this one (abstract)
  void Merge(const BaseCdfDataStore& other) override {
    PYBIND11_OVERRIDE(void, BaseCdfDataStore, Merge, other);
  }

  // Get the number of data points in the datastore (abstract)
  std::size_t Size() const override {
    PYBIND11_OVERRIDE(std::size_t, BaseCdfDataStore, Size);
  }

  // Get the sum of all values in the datastore (abstract)
  float Sum() const override {
    PYBIND11_OVERRIDE(float, BaseCdfDataStore, Sum);
  }

  void Reset() override { PYBIND11_OVERRIDE(void, BaseCdfDataStore, Reset); }
};
//==============================================================================
void InitBaseCdfDataStorePybindClass(py::module_& m) {
  // Bind the BaseCdfDataStore class as an abstract base class
  py::class_<BaseCdfDataStore, PyCdfDataStore,
             std::shared_ptr<BaseCdfDataStore>>(m, "BaseCdfDataStore")
      .def("put", &BaseCdfDataStore::Put, py::arg("label"), py::arg("value"))
      .def("merge", &BaseCdfDataStore::Merge, py::arg("other"))
      .def("size", &BaseCdfDataStore::Size)
      .def("sum", &BaseCdfDataStore::Sum)
      .def("reset", &BaseCdfDataStore::Reset);
}
//==============================================================================
void InitTimeSeriesDataStorePybindClass(py::module_& m) {
  py::class_<TimeSeriesDataStore, std::shared_ptr<TimeSeriesDataStore>>(
      m, "TimeSeriesDataStore")
      .def(py::init<>())
      .def(py::init<const std::vector<std::pair<TimeS, float>>&>())
      .def("put", &TimeSeriesDataStore::Put, py::arg("time"), py::arg("value"))
      .def("merge", &TimeSeriesDataStore::Merge, py::arg("other"))
      .def("get_start_time", &TimeSeriesDataStore::GetStartTime)
      .def("size", &TimeSeriesDataStore::Size)
      .def("sum", &TimeSeriesDataStore::Sum)
      .def("get_data_log", &TimeSeriesDataStore::GetDataLogCopy)
      .def("reset", &TimeSeriesDataStore::Reset)
      .def(py::pickle(
          [](const TimeSeriesDataStore& ts) {  // __getstate__
            // Pickle a copy of the data log
            return py::make_tuple(ts.GetDataLogCopy());
          },
          [](py::tuple t) {  // __setstate__
            ASSERT_VALID_RUNTIME(
                t.size() == 1,
                "Invalid pickled state for TimeSeriesDataStore!");

            // Get the data from the pickle
            auto data_log = t[0].cast<std::vector<std::pair<TimeS, float>>>();
            // Create a new TimeSeriesDataStore with the data using the custom
            // constructor
            return std::make_shared<TimeSeriesDataStore>(data_log);
          }));
}
//==============================================================================
void InitLabeledCdfDataStorePybindClass(py::module_& m) {
  py::class_<LabeledCdfDataStore, BaseCdfDataStore,
             std::shared_ptr<LabeledCdfDataStore>>(m, "LabeledCdfDataStore")
      .def(py::init<>())
      .def(py::init<const std::vector<std::pair<std::string, float>>&>())
      .def("get_data_log", &LabeledCdfDataStore::GetDataLogCopy)
      .def("dedupe_and_normalize", &LabeledCdfDataStore::DedupeAndNormalize)
      .def(py::pickle(
          [](const LabeledCdfDataStore& cdf) {  // __getstate__
            // Pickle a copy of the data log
            return py::make_tuple(cdf.GetDataLogCopy());
          },
          [](py::tuple t) {  // __setstate__
            ASSERT_VALID_RUNTIME(
                t.size() == 1,
                "Invalid pickled state for LabeledCdfDataStore!");

            // Get the data from the pickle
            auto data_log =
                t[0].cast<std::vector<std::pair<std::string, float>>>();
            // Create a new LabeledCdfDataStore with the data using the custom
            // constructor
            return std::make_shared<LabeledCdfDataStore>(data_log);
          }));
}
//==============================================================================
void InitUnlabeledCdfDataStorePybindClass(py::module_& m) {
  py::class_<UnlabeledCdfDataStore, BaseCdfDataStore,
             std::shared_ptr<UnlabeledCdfDataStore>>(m, "UnlabeledCdfDataStore")
      .def(py::init<double>(), py::arg("relative_accuracy") = 0.001)
      .def("min", &UnlabeledCdfDataStore::Min)
      .def("max", &UnlabeledCdfDataStore::Max)
      .def("count", &UnlabeledCdfDataStore::Count)
      .def("get_quantile_value", &UnlabeledCdfDataStore::GetQuantileValue,
           py::arg("quantile"))
      .def(py::pickle(
          [](const UnlabeledCdfDataStore& cdf) {  // __getstate__
            // Get serialized string state
            return py::make_tuple(cdf.GetSerializedState());
          },
          [](py::tuple t) {  // __setstate__
            ASSERT_VALID_RUNTIME(
                t.size() == 1,
                "Invalid pickled state for UnlabeledCdfDataStore!");

            // Extract components from the tuple
            std::string serialized_data = t[0].cast<std::string>();

            // Create a new sketch from the serialized string
            return UnlabeledCdfDataStore::FromSerializedString(serialized_data);
          }));
}
//==============================================================================
void InitDataStoresPybindSubmodule(py::module& pm) {
  auto m = pm.def_submodule("datastores", "DataStores submodule");

  InitBaseCdfDataStorePybindClass(m);
  InitTimeSeriesDataStorePybindClass(m);
  InitLabeledCdfDataStorePybindClass(m);
  InitUnlabeledCdfDataStorePybindClass(m);
}
//==============================================================================
}  // namespace vajra
//==============================================================================
