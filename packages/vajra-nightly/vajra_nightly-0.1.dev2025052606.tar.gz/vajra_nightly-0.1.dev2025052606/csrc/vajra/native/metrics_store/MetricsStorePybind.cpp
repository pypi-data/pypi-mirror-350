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
#include "native/metrics_store/MetricsStorePybind.h"
//==============================================================================
#include "native/metrics_store/ChromeTracer.h"
#include "native/metrics_store/CpuTimer.h"
#include "native/metrics_store/CudaTimer.h"
#include "native/metrics_store/MetricGroups.h"
#include "native/metrics_store/MetricType.h"
#include "native/metrics_store/Types.h"
#include "native/metrics_store/datastores/DataStoresPybind.h"
//==============================================================================
namespace vajra {
//==============================================================================
class PyMetricStore : public BaseMetricsStore {
 public:
  // Check if an operation is enabled for the given metric type
  [[nodiscard]] bool IsOperationEnabled(MetricType metric_type) override {
    PYBIND11_OVERRIDE(bool, BaseMetricsStore, IsOperationEnabled, metric_type);
  }
};
//==============================================================================
void InitMetricsStorePybindFunctions(py::module_& m) {
  m.def("get_gpu_operation_metrics_types", &GetGpuOperationMetricsTypes);
  m.def("get_gpu_operation_metrics", &GetGpuOperationMetrics,
        py::arg("requires_label") = false);

  m.def("get_cpu_operation_metrics_types", &GetCpuOperationMetricsTypes);
  m.def("get_cpu_operation_metrics", &GetCpuOperationMetrics,
        py::arg("requires_label") = false);

  m.def("get_sequence_time_distribution_metrics_types",
        &GetSequenceTimeDistributionMetricsTypes);
  m.def("get_sequence_time_distribution_metrics",
        &GetSequenceTimeDistributionMetrics);

  m.def("get_sequence_histogram_metrics_types",
        &GetSequenceHistogramMetricsTypes);
  m.def("get_sequence_histogram_metrics", &GetSequenceHistogramMetrics);

  m.def("get_batch_count_distribution_metrics_types",
        &GetBatchCountDistributionMetricsTypes);
  m.def("get_batch_count_distribution_metrics",
        &GetBatchCountDistributionMetrics, py::arg("requires_label") = false);

  m.def("get_batch_time_distribution_metrics_types",
        &GetBatchTimeDistributionMetricsTypes);
  m.def("get_batch_time_distribution_metrics", &GetBatchTimeDistributionMetrics,
        py::arg("requires_label") = false);

  m.def("get_token_time_distribution_metrics_types",
        &GetTokenTimeDistributionMetricsTypes);
  m.def("get_token_time_distribution_metrics",
        &GetTokenTimeDistributionMetrics);

  m.def("get_completion_time_series_metrics_types",
        &GetCompletionTimeSeriesMetricsTypes);
  m.def("get_completion_time_series_metrics", &GetCompletionTimeSeriesMetrics);

  m.def("get_all_metrics", &GetAllMetrics, py::arg("write_metrics") = true,
        py::arg("keep_individual_batch_metrics") = false,
        py::arg("enable_gpu_op_level_metrics") = false,
        py::arg("enable_cpu_op_level_metrics") = false);
}
//==============================================================================
void InitChromeTracerPybindClass(py::module_& m) {
  // Bind the ChromeTracer class
  py::class_<ChromeTracer, std::shared_ptr<ChromeTracer>>(m, "ChromeTracer")
      .def(py::init<std::string>(), py::arg("output_dir"))
      .def("put", &ChromeTracer::Put, py::arg("seq_metadata_list"),
           py::arg("replica_id"), py::arg("tensor_parallel_rank"),
           py::arg("pipeline_parallel_rank"), py::arg("kv_parallel_rank"),
           py::arg("start_time"), py::arg("end_time"))
      .def("put_scheduler_event", &ChromeTracer::PutSchedulerEvent,
           py::arg("replica_id"), py::arg("scheduler_id"),
           py::arg("seq_schedule_metadata_list"), py::arg("start_time"),
           py::arg("end_time"))
      .def("merge", &ChromeTracer::Merge, py::arg("other"))
      .def("store", &ChromeTracer::Store)
      .def("reset", &ChromeTracer::Reset)
      .def("get_output_dir", &ChromeTracer::GetOutputDir)
      .def("get_state", &ChromeTracer::GetState)
      .def(py::pickle(
          [](const ChromeTracer& tracer) {  // __getstate__
            return py::make_tuple(tracer.GetOutputDir(), tracer.GetState());
          },
          [](py::tuple t) {  // __setstate__
            ASSERT_VALID_RUNTIME(t.size() == 2,
                                 "Invalid pickled state for ChromeTracer!");

            return std::make_shared<ChromeTracer>(t[0].cast<std::string>(),
                                                  t[1].cast<std::string>());
          }));
}
//==============================================================================
void InitCudaTimerPybindClass(py::module_& m) {
  // Bind the CudaTimer class
  py::class_<CudaTimer, std::shared_ptr<CudaTimer>>(m, "CudaTimer")
      .def(py::init<std::optional<MetricType>, WorkerMetricsStorePtr,
                    std::optional<int>>(),
           py::arg("metric_type"), py::arg("metrics_store"),
           py::arg("layer_id") = std::nullopt)
      .def("start", &CudaTimer::Start)
      .def("stop", &CudaTimer::Stop);
}
//==============================================================================
void InitCpuTimerPybindClass(py::module_& m) {
  // Bind the CpuTimer class
  py::class_<CpuTimer, std::shared_ptr<CpuTimer>>(m, "CpuTimer")
      .def(py::init<std::optional<MetricType>,
                    std::shared_ptr<BaseMetricsStore>>(),
           py::arg("metric_type"), py::arg("metrics_store"))
      .def("start", &CpuTimer::Start)
      .def("stop", &CpuTimer::Stop);
}
//==============================================================================
void InitBaseMetricsStorePybindClass(py::module_& m) {
  // Bind the BaseMetricsStore class (as an abstract class)
  py::class_<BaseMetricsStore, PyMetricStore,
             std::shared_ptr<BaseMetricsStore>>(m, "BaseMetricsStore")
      .def("reset", &BaseMetricsStore::Reset)
      .def("push_cpu_operation_metric",
           &BaseMetricsStore::PushCpuOperationMetric, py::arg("metric_type"),
           py::arg("time"))
      .def("is_operation_enabled", &BaseMetricsStore::IsOperationEnabled,
           py::arg("metric_type"))
      .def("get_chrome_tracer", &BaseMetricsStore::GetChromeTracer);
}
//==============================================================================
void InitEngineMetricsStorePybindClass(py::module_& m) {
  // Bind the EngineMetricsStore class
  py::class_<EngineMetricsStore, BaseMetricsStore, EngineMetricsStorePtr>(
      m, "EngineMetricsStore")
      .def(py::init<const MetricsConfig&, const CdfDataStores&,
                    const TimeSeriesDataStores&,
                    const std::shared_ptr<ChromeTracer>&>(),
           py::arg("config"), py::arg("cdf_datastores"),
           py::arg("time_series_datastores"), py::arg("chrome_tracer"))
      .def("on_request_arrival", &EngineMetricsStore::OnRequestArrival,
           py::arg("seq_id"), py::arg("arrival_time"))
      .def("on_request_end", &EngineMetricsStore::OnRequestEnd, py::arg("seq"))
      .def("on_schedule", &EngineMetricsStore::OnSchedule,
           py::arg("replica_id"), py::arg("scheduler_output"),
           py::arg("start_time"), py::arg("end_time"))
      .def("on_batch_end", &EngineMetricsStore::OnBatchEnd, py::arg("seqs"),
           py::arg("scheduler_output"), py::arg("batch_start_time"),
           py::arg("batch_end_time"));
}
//==============================================================================
void InitWorkerMetricsStorePybindClass(py::module_& m) {
  // Bind the WorkerMetricsStore class
  py::class_<WorkerMetricsStore, BaseMetricsStore, WorkerMetricsStorePtr>(
      m, "WorkerMetricsStore")
      .def(py::init<const MetricsConfig&, const CdfDataStores&,
                    const TimeSeriesDataStores&,
                    const std::shared_ptr<ChromeTracer>&, const std::size_t>(),
           py::arg("config"), py::arg("cdf_datastores"),
           py::arg("time_series_datastores"), py::arg("chrome_tracer"),
           py::arg("rank"))
      .def("is_operation_enabled",
           (bool (WorkerMetricsStore::*)(
               MetricType,
               std::optional<int>))&WorkerMetricsStore::IsOperationEnabled,
           py::arg("metric_type"), py::arg("layer_id") = std::nullopt)
      .def("on_batch_stage_start", &WorkerMetricsStore::OnBatchStageStart,
           py::arg("scheduler_output"))
      .def("on_batch_stage_end", &WorkerMetricsStore::OnBatchStageEnd,
           py::arg("replica_id"), py::arg("seq_metadata_list"),
           py::arg("tensor_parallel_rank"), py::arg("pipeline_parallel_rank"),
           py::arg("kv_parallel_rank"), py::arg("start_time"),
           py::arg("end_time"))
      .def("push_operation_metric_cuda_events",
           &WorkerMetricsStore::PushGpuOperationMetricCudaEvents,
           py::arg("metric_type"), py::arg("start_event"), py::arg("end_event"))
      .def("push_gpu_operation_metric",
           &WorkerMetricsStore::PushGpuOperationMetric, py::arg("metric_type"),
           py::arg("time"));
}
//==============================================================================
void InitPlotTypePybindEnum(py::module_& m) {
  py::enum_<PlotType>(m, "PlotType")
      .value("CDF", PlotType::CDF)
      .value("HISTOGRAM", PlotType::HISTOGRAM)
      .value("TIME_SERIES", PlotType::TIME_SERIES);
}
//==============================================================================
void InitUnitTypePybindEnum(py::module_& m) {
  py::enum_<UnitType>(m, "UnitType")
      .value("MS", UnitType::MS)
      .value("SECONDS", UnitType::SECONDS)
      .value("PERCENT", UnitType::PERCENT)
      .value("COUNT", UnitType::COUNT);
}
//==============================================================================
void InitLabelTypePybindEnum(py::module_& m) {
  py::enum_<LabelType>(m, "LabelType")
      .value("BATCH", LabelType::BATCH)
      .value("REQUEST", LabelType::REQUEST);
}
//==============================================================================
void InitEntityAssociationTypePybindEnum(py::module_& m) {
  py::enum_<EntityAssociationType>(m, "EntityAssociationType")
      .value("REQUEST", EntityAssociationType::REQUEST)
      .value("BATCH", EntityAssociationType::BATCH);
}
//==============================================================================
void InitComparisonGroupTypePybindEnum(py::module_& m) {
  py::enum_<ComparisonGroupType>(m, "ComparisonGroupType")
      .value("GPU_OPERATION_RUNTIME",
             ComparisonGroupType::GPU_OPERATION_RUNTIME)
      .value("BATCH_RUNTIME", ComparisonGroupType::BATCH_RUNTIME)
      .value("BATCH_COMPOSITION", ComparisonGroupType::BATCH_COMPOSITION)
      .value("REQUEST_RUNTIME", ComparisonGroupType::REQUEST_RUNTIME);
}
//==============================================================================
void InitMetricPybindClass(py::module_& m) {
  py::class_<Metric>(m, "Metric")
      .def(py::init<MetricType, UnitType, bool, PlotType,
                    std::optional<ComparisonGroupType>,
                    std::optional<EntityAssociationType>,
                    std::optional<LabelType>, bool>(),
           py::arg("type"), py::arg("unit"), py::arg("requires_label"),
           py::arg("plot_type"), py::arg("comparison_group") = std::nullopt,
           py::arg("entity_association_group") = std::nullopt,
           py::arg("label_type") = std::nullopt,
           py::arg("aggregate_time_series") = true)
      .def_readonly("type", &Metric::type)
      .def_readonly("name", &Metric::name)
      .def_readonly("unit", &Metric::unit)
      .def_readonly("requires_label", &Metric::requires_label)
      .def_readonly("plot_type", &Metric::plot_type)
      .def_readonly("comparison_group", &Metric::comparison_group)
      .def_readonly("entity_association_group",
                    &Metric::entity_association_group)
      .def_readonly("label_type", &Metric::label_type)
      .def_readonly("aggregate_time_series", &Metric::aggregate_time_series)
      .def("__str__", &Metric::ToString)
      .def("__repr__", &Metric::ToString)
      .def("__eq__", &Metric::operator==)
      .def("__ne__", &Metric::operator!=)
      .def(py::pickle(
          // __getstate__: Convert the C++ object to a Python tuple that can be
          // pickled
          [](const Metric& m) {
            return py::make_tuple(m.type, m.unit, m.requires_label, m.plot_type,
                                  m.comparison_group,
                                  m.entity_association_group, m.label_type,
                                  m.aggregate_time_series);
          },
          // __setstate__: Convert the Python tuple back to a C++ object
          [](py::tuple t) {
            ASSERT_VALID_RUNTIME(t.size() == 8,
                                 "Invalid state for Metric pickle!");

            // Create a new Metric object with the unpickled data
            return Metric(t[0].cast<MetricType>(), t[1].cast<UnitType>(),
                          t[2].cast<bool>(), t[3].cast<PlotType>(),
                          t[4].cast<std::optional<ComparisonGroupType>>(),
                          t[5].cast<std::optional<EntityAssociationType>>(),
                          t[6].cast<std::optional<LabelType>>(),
                          t[7].cast<bool>());
          }));
}
//==============================================================================
void InitMetricTypePybindEnum(py::module_& m) {
  py::enum_<MetricType>(m, "MetricType")
      // GPU Operations
      .value("MLP_UP_PROJ", MetricType::MLP_UP_PROJ)
      .value("MLP_UP_PROJ_ALL_GATHER", MetricType::MLP_UP_PROJ_ALL_GATHER)
      .value("MLP_ACTIVATION", MetricType::MLP_ACTIVATION)
      .value("MLP_DOWN_PROJ", MetricType::MLP_DOWN_PROJ)
      .value("MLP_DOWN_PROJ_ALL_REDUCE", MetricType::MLP_DOWN_PROJ_ALL_REDUCE)
      .value("ATTN_PRE_PROJ", MetricType::ATTN_PRE_PROJ)
      .value("ATTN_PRE_PROJ_ALL_GATHER", MetricType::ATTN_PRE_PROJ_ALL_GATHER)
      .value("ATTN_POST_PROJ", MetricType::ATTN_POST_PROJ)
      .value("ATTN_POST_PROJ_ALL_REDUCE", MetricType::ATTN_POST_PROJ_ALL_REDUCE)
      .value("ATTN_KV_CACHE_SAVE", MetricType::ATTN_KV_CACHE_SAVE)
      .value("ATTN", MetricType::ATTN)
      .value("ATTN_ROPE", MetricType::ATTN_ROPE)
      .value("ATTN_INPUT_RESHAPE", MetricType::ATTN_INPUT_RESHAPE)
      .value("ATTN_OUTPUT_RESHAPE", MetricType::ATTN_OUTPUT_RESHAPE)
      .value("EMBED_LINEAR", MetricType::EMBED_LINEAR)
      .value("EMBED_ALL_REDUCE", MetricType::EMBED_ALL_REDUCE)
      .value("LM_HEAD_LINEAR", MetricType::LM_HEAD_LINEAR)
      .value("LM_HEAD_ALL_GATHER", MetricType::LM_HEAD_ALL_GATHER)
      .value("INPUT_LAYERNORM", MetricType::INPUT_LAYERNORM)
      .value("POST_ATTENTION_LAYERNORM", MetricType::POST_ATTENTION_LAYERNORM)
      .value("NORM", MetricType::NORM)
      .value("ADD", MetricType::ADD)
      .value("NCCL_SEND", MetricType::NCCL_SEND)
      .value("NCCL_RECV", MetricType::NCCL_RECV)
      .value("MOE_GATING", MetricType::MOE_GATING)
      .value("MOE_LINEAR", MetricType::MOE_LINEAR)
      // CPU Operations
      .value("SAMPLER", MetricType::SAMPLER)
      .value("PREPARE_INPUTS", MetricType::PREPARE_INPUTS)
      .value("MODEL_EXECUTION", MetricType::MODEL_EXECUTION)
      .value("WORKER_ON_SCHEDULE_HANDLING",
             MetricType::WORKER_ON_SCHEDULE_HANDLING)
      .value("WORKER_ON_STEP_COMPLETE_HANDLING",
             MetricType::WORKER_ON_STEP_COMPLETE_HANDLING)
      .value("ATTN_BEGIN_FORWARD", MetricType::ATTN_BEGIN_FORWARD)
      // Sequence Metrics Time Distributions
      .value("REQUEST_E2E_TIME", MetricType::REQUEST_E2E_TIME)
      .value("REQUEST_INTER_ARRIVAL_DELAY",
             MetricType::REQUEST_INTER_ARRIVAL_DELAY)
      .value("REQUEST_E2E_TIME_NORMALIZED",
             MetricType::REQUEST_E2E_TIME_NORMALIZED)
      .value("REQUEST_E2E_TIME_PIECEWISE_NORMALIZED",
             MetricType::REQUEST_E2E_TIME_PIECEWISE_NORMALIZED)
      .value("REQUEST_EXECUTION_TIME", MetricType::REQUEST_EXECUTION_TIME)
      .value("REQUEST_EXECUTION_TIME_NORMALIZED",
             MetricType::REQUEST_EXECUTION_TIME_NORMALIZED)
      .value("REQUEST_PREEMPTION_TIME", MetricType::REQUEST_PREEMPTION_TIME)
      .value("REQUEST_SCHEDULING_DELAY", MetricType::REQUEST_SCHEDULING_DELAY)
      .value("REQUEST_EXECUTION_PLUS_PREEMPTION_TIME",
             MetricType::REQUEST_EXECUTION_PLUS_PREEMPTION_TIME)
      .value("REQUEST_EXECUTION_PLUS_PREEMPTION_TIME_NORMALIZED",
             MetricType::REQUEST_EXECUTION_PLUS_PREEMPTION_TIME_NORMALIZED)
      .value("PREFILL_TIME_E2E", MetricType::PREFILL_TIME_E2E)
      .value("PREFILL_TIME_E2E_NORMALIZED",
             MetricType::PREFILL_TIME_E2E_NORMALIZED)
      .value("PREFILL_TIME_E2E_PIECEWISE_NORMALIZED",
             MetricType::PREFILL_TIME_E2E_PIECEWISE_NORMALIZED)
      .value("PREFILL_TIME_EXECUTION_PLUS_PREEMPTION",
             MetricType::PREFILL_TIME_EXECUTION_PLUS_PREEMPTION)
      .value("PREFILL_TIME_EXECUTION_PLUS_PREEMPTION_NORMALIZED",
             MetricType::PREFILL_TIME_EXECUTION_PLUS_PREEMPTION_NORMALIZED)
      .value("DECODE_TIME_EXECUTION_PLUS_PREEMPTION_NORMALIZED",
             MetricType::DECODE_TIME_EXECUTION_PLUS_PREEMPTION_NORMALIZED)
      // Sequence Metrics Histograms
      .value("REQUEST_NUM_TOKENS", MetricType::REQUEST_NUM_TOKENS)
      .value("REQUEST_PREFILL_TOKENS", MetricType::REQUEST_PREFILL_TOKENS)
      .value("REQUEST_DECODE_TOKENS", MetricType::REQUEST_DECODE_TOKENS)
      .value("REQUEST_PD_RATIO", MetricType::REQUEST_PD_RATIO)
      .value("REQUEST_NUM_RESTARTS", MetricType::REQUEST_NUM_RESTARTS)
      .value("REQUEST_NUM_PAUSES", MetricType::REQUEST_NUM_PAUSES)
      .value("REQUEST_NUM_IGNORED", MetricType::REQUEST_NUM_IGNORED)
      // Batch Metrics Count Distributions
      .value("BATCH_NUM_TOKENS", MetricType::BATCH_NUM_TOKENS)
      .value("BATCH_NUM_PREFILL_TOKENS", MetricType::BATCH_NUM_PREFILL_TOKENS)
      .value("BATCH_NUM_DECODE_TOKENS", MetricType::BATCH_NUM_DECODE_TOKENS)
      .value("BATCH_SIZE", MetricType::BATCH_SIZE)
      // Batch Metrics Time Distributions
      .value("BATCH_EXECUTION_TIME", MetricType::BATCH_EXECUTION_TIME)
      .value("INTER_BATCH_DELAY", MetricType::INTER_BATCH_DELAY)
      // Token Metrics Time Distributions
      .value("DECODE_TOKEN_EXECUTION_PLUS_PREEMPTION_TIME",
             MetricType::DECODE_TOKEN_EXECUTION_PLUS_PREEMPTION_TIME)
      // Completion Metrics Time Series
      .value("REQUEST_ARRIVED", MetricType::REQUEST_ARRIVED)
      .value("REQUEST_COMPLETED", MetricType::REQUEST_COMPLETED)
      .value("PREFILL_COMPLETED", MetricType::PREFILL_COMPLETED)
      .value("DECODE_COMPLETED", MetricType::DECODE_COMPLETED);
}
//==============================================================================
void InitMetricsStorePybindSubmodule(py::module& m) {
  auto metrics_store_module =
      m.def_submodule("metrics_store", "Metrics store module");

  // Initialize each class and enum using the individual functions
  InitChromeTracerPybindClass(metrics_store_module);
  InitCudaTimerPybindClass(metrics_store_module);
  InitCpuTimerPybindClass(metrics_store_module);
  InitBaseMetricsStorePybindClass(metrics_store_module);
  InitEngineMetricsStorePybindClass(metrics_store_module);
  InitWorkerMetricsStorePybindClass(metrics_store_module);
  InitPlotTypePybindEnum(metrics_store_module);
  InitUnitTypePybindEnum(metrics_store_module);
  InitLabelTypePybindEnum(metrics_store_module);
  InitEntityAssociationTypePybindEnum(metrics_store_module);
  InitComparisonGroupTypePybindEnum(metrics_store_module);
  InitMetricPybindClass(metrics_store_module);
  InitMetricTypePybindEnum(metrics_store_module);
  InitMetricsStorePybindFunctions(metrics_store_module);

  // Initialize the datastores submodule
  InitDataStoresPybindSubmodule(metrics_store_module);
}
//==============================================================================
}  // namespace vajra
//==============================================================================
