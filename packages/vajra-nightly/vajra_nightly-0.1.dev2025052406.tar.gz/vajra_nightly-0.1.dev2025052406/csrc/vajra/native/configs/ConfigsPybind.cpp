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
#include "native/configs/ConfigsPybind.h"

#include "commons/Logging.h"
#include "native/configs/CacheConfig.h"
#include "native/configs/MetricsConfig.h"
#include "native/configs/ModelConfig.h"
#include "native/configs/ParallelConfig.h"
#include "native/configs/ReplicaControllerConfig.h"
#include "native/configs/ReplicaResourceConfig.h"
#include "native/configs/ReplicaSchedulerConfig.h"
#include "native/configs/ReplicasetControllerConfig.h"
#include "native/configs/ReplicasetSchedulerConfig.h"
#include "native/configs/RequestPrioritizerConfig.h"
#include "native/configs/TransferEngineConfig.h"
#include "native/configs/WorkerConfig.h"
//==============================================================================
namespace vajra {
//==============================================================================
class PyReplicaSchedulerConfig : public BaseReplicaSchedulerConfig {
 public:
  std::size_t GetMaxChunkSize() const override {
    PYBIND11_OVERRIDE(std::size_t, BaseReplicaSchedulerConfig, GetMaxChunkSize);
  }
  std::size_t GetMinChunkSize() const override {
    PYBIND11_OVERRIDE(std::size_t, BaseReplicaSchedulerConfig, GetMinChunkSize);
  }
  float GetTargetBatchTime() const override {
    PYBIND11_OVERRIDE(float, BaseReplicaSchedulerConfig, GetTargetBatchTime);
  }
  ReplicaSchedulerType GetType() const override {
    PYBIND11_OVERRIDE(ReplicaSchedulerType, BaseReplicaSchedulerConfig,
                      GetType);
  }
};
//==============================================================================
class PyRequestPrioritizerConfig : public BaseRequestPrioritizerConfig {
 public:
  RequestPrioritizerType GetType() const override {
    PYBIND11_OVERRIDE(RequestPrioritizerType, BaseRequestPrioritizerConfig,
                      GetType);
  }
};
//==============================================================================
class PyReplicasetSchedulerConfig : public BaseReplicasetSchedulerConfig {
 public:
  ReplicasetSchedulerType GetType() const override {
    PYBIND11_OVERRIDE(ReplicasetSchedulerType, BaseReplicasetSchedulerConfig,
                      GetType);
  }
};
//==============================================================================
class PyReplicaControllerConfig : public BaseReplicaControllerConfig {
 public:
  PyReplicaControllerConfig(
      const ModelConfig& model_config_param,
      const WorkerConfig& worker_config_param,
      const CacheConfig& cache_config_param,
      const ParallelConfig& parallel_config_param,
      const std::shared_ptr<BaseReplicaSchedulerConfig>& scheduler_config_param)
      : BaseReplicaControllerConfig(model_config_param, worker_config_param,
                                    cache_config_param, parallel_config_param,
                                    scheduler_config_param) {}

  ReplicaControllerType GetType() const override {
    PYBIND11_OVERRIDE(ReplicaControllerType, BaseReplicaControllerConfig,
                      GetType);
  }
};
//==============================================================================
class PyReplicasetControllerConfig : public BaseReplicasetControllerConfig {
 public:
  PyReplicasetControllerConfig(
      const std::size_t num_replicas_param,
      const std::shared_ptr<BaseReplicaControllerConfig>&
          replica_controller_config_param,
      const std::shared_ptr<BaseRequestPrioritizerConfig>&
          request_prioritizer_config_param,
      const std::shared_ptr<BaseReplicasetSchedulerConfig>&
          replicaset_scheduler_config_param)
      : BaseReplicasetControllerConfig(num_replicas_param,
                                       replica_controller_config_param,
                                       request_prioritizer_config_param,
                                       replicaset_scheduler_config_param) {}

  ReplicasetControllerType GetType() const override {
    PYBIND11_OVERRIDE(ReplicasetControllerType, BaseReplicasetControllerConfig,
                      GetType);
  }
};
//==============================================================================
void InitModelConfigPybindClass(py::module_& m) {
  py::class_<ModelConfig>(m, "ModelConfig")
      .def(py::init<std::string, bool, std::optional<std::string>, std::string,
                    std::string, std::size_t, std::optional<std::string>,
                    std::size_t, std::size_t, std::size_t, std::size_t,
                    std::size_t>(),
           py::arg("model"), py::arg("trust_remote_code"),
           py::arg("download_dir"), py::arg("load_format"), py::arg("dtype"),
           py::arg("seed"), py::arg("revision"), py::arg("max_model_len"),
           py::arg("total_num_layers"), py::arg("total_num_q_heads"),
           py::arg("total_num_kv_heads"), py::arg("hidden_size"))
      .def("__str__", &ModelConfig::ToString)
      .def("__repr__", &ModelConfig::ToString)
      .def_readonly("model", &ModelConfig::model)
      .def_readonly("trust_remote_code", &ModelConfig::trust_remote_code)
      .def_readonly("download_dir", &ModelConfig::download_dir)
      .def_readonly("load_format", &ModelConfig::load_format)
      .def_readonly("dtype", &ModelConfig::dtype)
      .def_readonly("seed", &ModelConfig::seed)
      .def_readonly("revision", &ModelConfig::revision)
      .def_readonly("max_model_len", &ModelConfig::max_model_len)
      .def_readonly("total_num_layers", &ModelConfig::total_num_layers)
      .def_readonly("total_num_q_heads", &ModelConfig::total_num_q_heads)
      .def_readonly("total_num_kv_heads", &ModelConfig::total_num_kv_heads)
      .def_readonly("hidden_size", &ModelConfig::hidden_size)
      .def(py::pickle(
          [](const ModelConfig& p) {
            return py::make_tuple(p.model, p.trust_remote_code, p.download_dir,
                                  p.load_format, p.dtype, p.seed, p.revision,
                                  p.max_model_len, p.total_num_layers,
                                  p.total_num_q_heads, p.total_num_kv_heads,
                                  p.hidden_size);
          },
          [](py::tuple t) {
            ASSERT_VALID_RUNTIME(t.size() == 12,
                                 "Invalid pickled state for ModelConfig!");

            return ModelConfig(
                t[0].cast<std::string>(), t[1].cast<bool>(),
                t[2].cast<std::optional<std::string>>(),
                t[3].cast<std::string>(), t[4].cast<std::string>(),
                t[5].cast<std::size_t>(),
                t[6].cast<std::optional<std::string>>(),
                t[7].cast<std::size_t>(), t[8].cast<std::size_t>(),
                t[9].cast<std::size_t>(), t[10].cast<std::size_t>(),
                t[11].cast<std::size_t>());
          }));
}
//==============================================================================
void InitParallelConfigPybindClass(py::module_& m) {
  py::class_<ParallelConfig>(m, "ParallelConfig")
      .def(py::init<std::size_t, std::size_t, bool, bool, bool, std::size_t,
                    std::size_t>(),
           py::arg("pipeline_parallel_size"), py::arg("tensor_parallel_size"),
           py::arg("enable_expert_parallel"),
           py::arg("enable_sequence_pipeline_parallel"),
           py::arg("enable_chunked_pipeline_comm_opt"),
           py::arg("kv_parallel_size"), py::arg("max_num_tokens_per_kvp_group"))
      .def("__str__", &ParallelConfig::ToString)
      .def("__repr__", &ParallelConfig::ToString)
      .def_readonly("pipeline_parallel_size",
                    &ParallelConfig::pipeline_parallel_size)
      .def_readonly("tensor_parallel_size",
                    &ParallelConfig::tensor_parallel_size)
      .def_readonly("enable_expert_parallel",
                    &ParallelConfig::enable_expert_parallel)
      .def_readonly("enable_sequence_pipeline_parallel",
                    &ParallelConfig::enable_sequence_pipeline_parallel)
      .def_readonly("enable_chunked_pipeline_comm_opt",
                    &ParallelConfig::enable_chunked_pipeline_comm_opt)
      .def_readonly("kv_parallel_size", &ParallelConfig::kv_parallel_size)
      .def_readonly("max_num_tokens_per_kvp_group",
                    &ParallelConfig::max_num_tokens_per_kvp_group)
      .def_readonly("world_size", &ParallelConfig::world_size)
      .def(py::pickle(
          [](const ParallelConfig& p) {
            return py::make_tuple(
                p.pipeline_parallel_size, p.tensor_parallel_size,
                p.enable_expert_parallel, p.enable_sequence_pipeline_parallel,
                p.enable_chunked_pipeline_comm_opt, p.kv_parallel_size,
                p.max_num_tokens_per_kvp_group);
          },
          [](py::tuple t) {
            ASSERT_VALID_RUNTIME(t.size() == 7,
                                 "Invalid pickled state for ParallelConfig!");

            return ParallelConfig(
                t[0].cast<std::size_t>(), t[1].cast<std::size_t>(),
                t[2].cast<bool>(), t[3].cast<bool>(), t[4].cast<bool>(),
                t[5].cast<std::size_t>(), t[6].cast<std::size_t>());
          }));
}

//==============================================================================
void InitReplicaResourceConfigPybindClass(py::module_& m) {
  py::class_<ReplicaResourceConfig>(m, "ReplicaResourceConfig")
      .def(py::init<ParallelConfig&, ModelConfig&>(),
           py::arg("parallel_config"), py::arg("model_config"))
      .def("__str__", &ReplicaResourceConfig::ToString)
      .def("__repr__", &ReplicaResourceConfig::ToString)
      .def_readonly("tensor_parallel_size",
                    &ReplicaResourceConfig::tensor_parallel_size)
      .def_readonly("pipeline_parallel_size",
                    &ReplicaResourceConfig::pipeline_parallel_size)
      .def_readonly("kv_parallel_size",
                    &ReplicaResourceConfig::kv_parallel_size)
      .def_readonly("local_num_layers",
                    &ReplicaResourceConfig::local_num_layers)
      .def_readonly("total_num_layers",
                    &ReplicaResourceConfig::total_num_layers)
      .def_readonly("world_size", &ReplicaResourceConfig::world_size);
}

//==============================================================================
void InitTransferEngineConfigPybindClass(py::module_& m) {
  py::class_<TransferEngineConfig>(m, "TransferEngineConfig")
      .def(py::init<TransferBackendType, std::size_t,
                    const GlobalResourceConfig&,
                    c10::intrusive_ptr<c10d::ProcessGroup>>(),
           py::arg("transfer_backend_type"), py::arg("global_rank"),
           py::arg("global_resource_config"), py::arg("global_process_group"))
      .def("__str__", &TransferEngineConfig::ToString)
      .def("__repr__", &TransferEngineConfig::ToString)
      .def_readonly("transfer_backend_type",
                    &TransferEngineConfig::transfer_backend_type)
      .def_readonly("global_rank", &TransferEngineConfig::global_rank)
      .def_readonly("global_resource_config",
                    &TransferEngineConfig::global_resource_config)
      .def_readonly("global_process_group",
                    &TransferEngineConfig::global_process_group);
}

//==============================================================================
void InitCacheConfigPybindClass(py::module_& m) {
  py::class_<CacheConfig>(m, "CacheConfig")
      .def(py::init<std::size_t>(), py::arg("block_size"))
      .def("__str__", &CacheConfig::ToString)
      .def("__repr__", &CacheConfig::ToString)
      .def_readonly("block_size", &CacheConfig::block_size)
      .def(py::pickle(
          [](const CacheConfig& p) {  // __getstate__
            return py::make_tuple(p.block_size);
          },
          [](py::tuple t) {  // __setstate__
            ASSERT_VALID_RUNTIME(t.size() == 1,
                                 "Invalid pickled state for CacheConfig!");

            return CacheConfig(t[0].cast<std::size_t>());
          }));
}

//==============================================================================
void InitMetricsConfigPybindClass(py::module_& m) {
  py::class_<MetricsConfig>(m, "MetricsConfig")
      .def(py::init<bool, std::optional<std::string>,
                    std::optional<std::string>, std::optional<std::string>,
                    std::optional<std::string>, std::optional<std::string>,
                    bool, bool, bool, bool, bool, std::string>(),
           py::arg("write_metrics") = false,
           py::arg("wandb_project") = std::nullopt,
           py::arg("wandb_group") = std::nullopt,
           py::arg("wandb_run_name") = std::nullopt,
           py::arg("wandb_sweep_id") = std::nullopt,
           py::arg("wandb_run_id") = std::nullopt,
           py::arg("enable_gpu_op_level_metrics") = false,
           py::arg("enable_cpu_op_level_metrics") = false,
           py::arg("enable_chrome_trace") = false,
           py::arg("keep_individual_batch_metrics") = false,
           py::arg("store_png") = false, py::arg("output_dir") = ".")
      .def("__str__", &MetricsConfig::ToString)
      .def("__repr__", &MetricsConfig::ToString)
      .def_readonly("write_metrics", &MetricsConfig::write_metrics)
      .def_readonly("wandb_project", &MetricsConfig::wandb_project)
      .def_readonly("wandb_group", &MetricsConfig::wandb_group)
      .def_readonly("wandb_run_name", &MetricsConfig::wandb_run_name)
      .def_readonly("wandb_sweep_id", &MetricsConfig::wandb_sweep_id)
      .def_readonly("wandb_run_id", &MetricsConfig::wandb_run_id)
      .def_readonly("enable_gpu_op_level_metrics",
                    &MetricsConfig::enable_gpu_op_level_metrics)
      .def_readonly("enable_cpu_op_level_metrics",
                    &MetricsConfig::enable_cpu_op_level_metrics)
      .def_readonly("enable_chrome_trace", &MetricsConfig::enable_chrome_trace)
      .def_readonly("keep_individual_batch_metrics",
                    &MetricsConfig::keep_individual_batch_metrics)
      .def_readonly("store_png", &MetricsConfig::store_png)
      .def_readonly("output_dir", &MetricsConfig::output_dir)
      .def(py::pickle(
          [](const MetricsConfig& p) {
            return py::make_tuple(
                p.write_metrics, p.wandb_project, p.wandb_group,
                p.wandb_run_name, p.wandb_sweep_id, p.wandb_run_id,
                p.enable_gpu_op_level_metrics, p.enable_cpu_op_level_metrics,
                p.enable_chrome_trace, p.keep_individual_batch_metrics,
                p.store_png, p.output_dir);
          },
          [](py::tuple t) {
            ASSERT_VALID_RUNTIME(t.size() == 12,
                                 "Invalid pickled state for MetricsConfig!");
            return MetricsConfig(
                t[0].cast<bool>(), t[1].cast<std::optional<std::string>>(),
                t[2].cast<std::optional<std::string>>(),
                t[3].cast<std::optional<std::string>>(),
                t[4].cast<std::optional<std::string>>(),
                t[5].cast<std::optional<std::string>>(), t[6].cast<bool>(),
                t[7].cast<bool>(), t[8].cast<bool>(), t[9].cast<bool>(),
                t[10].cast<bool>(), t[11].cast<std::string>());
          }));
}

//==============================================================================
void InitWorkerConfigPybindClass(py::module_& m) {
  py::class_<WorkerConfig>(m, "WorkerConfig")
      .def(py::init<float, bool>())
      .def("__str__", &WorkerConfig::ToString)
      .def("__repr__", &WorkerConfig::ToString)
      .def_readonly("gpu_memory_utilization",
                    &WorkerConfig::gpu_memory_utilization)
      .def_readonly("use_native_execution_backend",
                    &WorkerConfig::use_native_execution_backend)
      .def(py::pickle(
          [](const WorkerConfig& self) {
            return py::make_tuple(self.gpu_memory_utilization,
                                  self.use_native_execution_backend);
          },
          [](py::tuple t) {
            ASSERT_VALID_RUNTIME(t.size() == 2,
                                 "Invalid pickled state for WorkerConfig!");

            return WorkerConfig(t[0].cast<float>(), t[1].cast<bool>());
          }));
}

//==============================================================================
void InitBaseReplicaSchedulerConfigPybindClass(py::module_& m) {
  py::class_<BaseReplicaSchedulerConfig, PyReplicaSchedulerConfig,
             std::shared_ptr<BaseReplicaSchedulerConfig>>(
      m, "BaseReplicaSchedulerConfig")
      .def("__str__", &BaseReplicaSchedulerConfig::ToString)
      .def("__repr__", &BaseReplicaSchedulerConfig::ToString)
      .def("get_type", &BaseReplicaSchedulerConfig::GetType)
      .def_property_readonly("max_chunk_size",
                             &BaseReplicaSchedulerConfig::GetMaxChunkSize)
      .def_property_readonly("min_chunk_size",
                             &BaseReplicaSchedulerConfig::GetMinChunkSize)
      .def_property_readonly("max_batch_size",
                             &BaseReplicaSchedulerConfig::GetMaxBatchSize)
      .def_property_readonly("target_batch_time",
                             &BaseReplicaSchedulerConfig::GetTargetBatchTime);
}
//==============================================================================
void InitFixedChunkReplicaSchedulerConfigPybindClass(py::module_& m) {
  py::class_<FixedChunkReplicaSchedulerConfig, BaseReplicaSchedulerConfig,
             std::shared_ptr<FixedChunkReplicaSchedulerConfig>>(
      m, "FixedChunkReplicaSchedulerConfig")
      .def(py::init<std::size_t, std::size_t>(),
           py::arg("max_batch_size") = 128, py::arg("chunk_size") = 2048)
      .def("__str__", &FixedChunkReplicaSchedulerConfig::ToString)
      .def("__repr__", &FixedChunkReplicaSchedulerConfig::ToString)
      .def(py::pickle(
          [](const FixedChunkReplicaSchedulerConfig& self) {
            return py::make_tuple(self.GetMaxBatchSize(),
                                  self.GetMinChunkSize());
          },
          [](py::tuple t) {
            ASSERT_VALID_RUNTIME(
                t.size() == 2,
                "Invalid state for FixedChunkReplicaSchedulerConfig!");

            return FixedChunkReplicaSchedulerConfig(
                t[0].cast<std::size_t>(),  // max_batch_size
                t[1].cast<std::size_t>()   // chunk_size
            );
          }));
}

//==============================================================================
void InitDynamicChunkReplicaSchedulerConfigPybindClass(py::module_& m) {
  py::class_<DynamicChunkReplicaSchedulerConfig, BaseReplicaSchedulerConfig,
             std::shared_ptr<DynamicChunkReplicaSchedulerConfig>>(
      m, "DynamicChunkReplicaSchedulerConfig")
      .def(py::init<std::size_t, std::size_t, std::size_t, float>(),
           py::arg("max_batch_size") = 128, py::arg("max_chunk_size") = 8192,
           py::arg("min_chunk_size") = 32, py::arg("target_batch_time") = 0.05)
      .def("__str__", &DynamicChunkReplicaSchedulerConfig::ToString)
      .def("__repr__", &DynamicChunkReplicaSchedulerConfig::ToString)
      .def(py::pickle(
          [](const DynamicChunkReplicaSchedulerConfig& self) {
            return py::make_tuple(
                self.GetMaxBatchSize(), self.GetMaxChunkSize(),
                self.GetMinChunkSize(), self.GetTargetBatchTime());
          },
          [](py::tuple t) {
            ASSERT_VALID_RUNTIME(
                t.size() == 4,
                "Invalid state for DynamicChunkReplicaSchedulerConfig!");

            return DynamicChunkReplicaSchedulerConfig(
                t[0].cast<std::size_t>(), t[1].cast<std::size_t>(),
                t[2].cast<std::size_t>(), t[3].cast<float>());
          }));
}

//==============================================================================
void InitSpaceSharingReplicaSchedulerConfigPybindClass(py::module_& m) {
  py::class_<SpaceSharingReplicaSchedulerConfig, BaseReplicaSchedulerConfig,
             std::shared_ptr<SpaceSharingReplicaSchedulerConfig>>(
      m, "SpaceSharingReplicaSchedulerConfig")
      .def(
          py::init<std::size_t, std::size_t, std::size_t, float, std::size_t>(),
          py::arg("max_batch_size") = 128, py::arg("max_chunk_size") = 8192,
          py::arg("min_chunk_size") = 32, py::arg("target_batch_time") = 0.05,
          py::arg("long_seq_kv_cache_len_threshold") = 256 * 1024)
      .def("__str__", &SpaceSharingReplicaSchedulerConfig::ToString)
      .def("__repr__", &SpaceSharingReplicaSchedulerConfig::ToString)
      .def_property_readonly(
          "long_seq_kv_cache_len_threshold",
          &SpaceSharingReplicaSchedulerConfig::GetLongSeqKvCacheLenThreshold)
      .def(py::pickle(
          [](const SpaceSharingReplicaSchedulerConfig& self) {
            return py::make_tuple(
                self.GetMaxBatchSize(), self.GetMaxChunkSize(),
                self.GetMinChunkSize(), self.GetTargetBatchTime(),
                self.GetLongSeqKvCacheLenThreshold());
          },
          [](py::tuple t) {
            ASSERT_VALID_RUNTIME(
                t.size() == 5,
                "Invalid state for SpaceSharingReplicaSchedulerConfig!");
            return SpaceSharingReplicaSchedulerConfig(
                t[0].cast<std::size_t>(), t[1].cast<std::size_t>(),
                t[2].cast<std::size_t>(), t[3].cast<float>(),
                t[4].cast<std::size_t>());
          }));
}

//==============================================================================
void InitBaseRequestPrioritizerConfigPybindClass(py::module_& m) {
  py::class_<BaseRequestPrioritizerConfig, PyRequestPrioritizerConfig,
             std::shared_ptr<BaseRequestPrioritizerConfig>>(
      m, "BaseRequestPrioritizerConfig")
      .def("__str__", &BaseRequestPrioritizerConfig::ToString)
      .def("__repr__", &BaseRequestPrioritizerConfig::ToString)
      .def("get_type", &BaseRequestPrioritizerConfig::GetType);
}
//==============================================================================
void InitFcfsRequestPrioritizerConfigPybindClass(py::module_& m) {
  py::class_<FcfsRequestPrioritizerConfig, BaseRequestPrioritizerConfig,
             std::shared_ptr<FcfsRequestPrioritizerConfig>>(
      m, "FcfsRequestPrioritizerConfig")
      .def(py::init<>())
      .def(py::pickle(
          [](const FcfsRequestPrioritizerConfig&) { return py::make_tuple(); },
          [](py::tuple t) {
            ASSERT_VALID_RUNTIME(
                t.size() == 0,
                "Invalid pickled state for FcfsRequestPrioritizerConfig!");
            return FcfsRequestPrioritizerConfig();
          }));
}
//==============================================================================
void InitEdfRequestPrioritizerConfigPybindClass(py::module_& m) {
  py::class_<EdfRequestPrioritizerConfig, BaseRequestPrioritizerConfig,
             std::shared_ptr<EdfRequestPrioritizerConfig>>(
      m, "EdfRequestPrioritizerConfig")
      .def(py::init<float, float>(), py::arg("deadline_multiplier") = 1.5,
           py::arg("min_deadline") = 0.5)
      .def_readonly("deadline_multiplier",
                    &EdfRequestPrioritizerConfig::deadline_multiplier)
      .def_readonly("min_deadline", &EdfRequestPrioritizerConfig::min_deadline)
      .def(py::pickle(
          [](const EdfRequestPrioritizerConfig& self) {
            return py::make_tuple(self.deadline_multiplier, self.min_deadline);
          },
          [](py::tuple t) {
            ASSERT_VALID_RUNTIME(
                t.size() == 2,
                "Invalid state for EdfRequestPrioritizerConfig!");
            return EdfRequestPrioritizerConfig(t[0].cast<float>(),
                                               t[1].cast<float>());
          }));
}
//==============================================================================
void InitLrsRequestPrioritizerConfigPybindClass(py::module_& m) {
  py::class_<LrsRequestPrioritizerConfig, BaseRequestPrioritizerConfig,
             std::shared_ptr<LrsRequestPrioritizerConfig>>(
      m, "LrsRequestPrioritizerConfig")
      .def(py::init<float, float>(), py::arg("deadline_multiplier") = 1.5,
           py::arg("min_deadline") = 0.5)
      .def_readonly("deadline_multiplier",
                    &LrsRequestPrioritizerConfig::deadline_multiplier)
      .def_readonly("min_deadline", &LrsRequestPrioritizerConfig::min_deadline)
      .def(py::pickle(
          [](const LrsRequestPrioritizerConfig& self) {
            return py::make_tuple(self.deadline_multiplier, self.min_deadline);
          },
          [](py::tuple t) {
            ASSERT_VALID_RUNTIME(
                t.size() == 2,
                "Invalid state for LrsRequestPrioritizerConfig!");
            return LrsRequestPrioritizerConfig(t[0].cast<float>(),
                                               t[1].cast<float>());
          }));
}
//==============================================================================
void InitBaseReplicasetSchedulerConfigPybindClass(py::module_& m) {
  py::class_<BaseReplicasetSchedulerConfig, PyReplicasetSchedulerConfig,
             std::shared_ptr<BaseReplicasetSchedulerConfig>>(
      m, "BaseReplicasetSchedulerConfig")
      .def("__str__", &BaseReplicasetSchedulerConfig::ToString)
      .def("__repr__", &BaseReplicasetSchedulerConfig::ToString)
      .def("get_type", &BaseReplicasetSchedulerConfig::GetType);
}
//==============================================================================
void InitPullReplicasetSchedulerConfigPybindClass(py::module_& m) {
  py::class_<PullReplicasetSchedulerConfig, BaseReplicasetSchedulerConfig,
             std::shared_ptr<PullReplicasetSchedulerConfig>>(
      m, "PullReplicasetSchedulerConfig")
      .def(py::init<>())
      .def(py::pickle(
          [](const PullReplicasetSchedulerConfig&) { return py::make_tuple(); },
          [](py::tuple t) {
            ASSERT_VALID_RUNTIME(
                t.size() == 0,
                "Invalid pickled state for PullReplicasetSchedulerConfig!");
            return PullReplicasetSchedulerConfig();
          }));
}
//==============================================================================
void InitRoundRobinReplicasetSchedulerConfigPybindClass(py::module_& m) {
  py::class_<RoundRobinReplicasetSchedulerConfig, BaseReplicasetSchedulerConfig,
             std::shared_ptr<RoundRobinReplicasetSchedulerConfig>>(
      m, "RoundRobinReplicasetSchedulerConfig")
      .def(py::init<>())
      .def(py::pickle(
          [](const RoundRobinReplicasetSchedulerConfig&) {
            return py::make_tuple();
          },
          [](py::tuple t) {
            ASSERT_VALID_RUNTIME(t.size() == 0,
                                 "Invalid pickled state for "
                                 "RoundRobinReplicasetSchedulerConfig!");

            return RoundRobinReplicasetSchedulerConfig();
          }));
}
//==============================================================================
void InitBaseReplicaControllerConfigPybindClass(py::module_& m) {
  py::class_<BaseReplicaControllerConfig, PyReplicaControllerConfig,
             std::shared_ptr<BaseReplicaControllerConfig>>(
      m, "BaseReplicaControllerConfig")
      .def("__str__", &BaseReplicaControllerConfig::ToString)
      .def("__repr__", &BaseReplicaControllerConfig::ToString)
      .def("get_type", &BaseReplicaControllerConfig::GetType)
      .def_readonly("model_config", &BaseReplicaControllerConfig::model_config)
      .def_readonly("worker_config",
                    &BaseReplicaControllerConfig::worker_config)
      .def_readonly("cache_config", &BaseReplicaControllerConfig::cache_config)
      .def_readonly("parallel_config",
                    &BaseReplicaControllerConfig::parallel_config)
      .def_readonly("scheduler_config",
                    &BaseReplicaControllerConfig::scheduler_config);
}
//==============================================================================
void InitLlmReplicaControllerConfigPybindClass(py::module_& m) {
  py::class_<LlmReplicaControllerConfig, BaseReplicaControllerConfig,
             std::shared_ptr<LlmReplicaControllerConfig>>(
      m, "LlmReplicaControllerConfig")
      .def(py::init<ModelConfig, WorkerConfig, CacheConfig, ParallelConfig,
                    std::shared_ptr<BaseReplicaSchedulerConfig>>(),
           py::arg("model_config"), py::arg("worker_config"),
           py::arg("cache_config"), py::arg("parallel_config"),
           py::arg("scheduler_config"))
      .def(py::pickle(
          [](const LlmReplicaControllerConfig& self) {
            return py::make_tuple(self.model_config, self.worker_config,
                                  self.cache_config, self.parallel_config,
                                  self.scheduler_config);
          },
          [](py::tuple t) {
            ASSERT_VALID_RUNTIME(
                t.size() == 5,
                "Invalid pickled state for LlmReplicaControllerConfig");

            return LlmReplicaControllerConfig(
                t[0].cast<ModelConfig>(), t[1].cast<WorkerConfig>(),
                t[2].cast<CacheConfig>(), t[3].cast<ParallelConfig>(),
                t[4].cast<std::shared_ptr<BaseReplicaSchedulerConfig>>());
          }));
}
//==============================================================================
void InitBaseReplicasetControllerConfigPybindClass(py::module_& m) {
  py::class_<BaseReplicasetControllerConfig, PyReplicasetControllerConfig,
             std::shared_ptr<BaseReplicasetControllerConfig>>(
      m, "BaseReplicasetControllerConfig")
      .def("__str__", &BaseReplicasetControllerConfig::ToString)
      .def("__repr__", &BaseReplicasetControllerConfig::ToString)
      .def("get_type", &BaseReplicasetControllerConfig::GetType)
      .def_readonly("num_replicas",
                    &BaseReplicasetControllerConfig::num_replicas)
      .def_readonly("replica_controller_config",
                    &BaseReplicasetControllerConfig::replica_controller_config)
      .def_readonly("request_prioritizer_config",
                    &BaseReplicasetControllerConfig::request_prioritizer_config)
      .def_readonly(
          "replicaset_scheduler_config",
          &BaseReplicasetControllerConfig::replicaset_scheduler_config);
}
//==============================================================================
void InitLlmReplicasetControllerConfigPybindClass(py::module_& m) {
  py::class_<LlmReplicasetControllerConfig, BaseReplicasetControllerConfig,
             std::shared_ptr<LlmReplicasetControllerConfig>>(
      m, "LlmReplicasetControllerConfig")
      .def(py::init<std::size_t, std::shared_ptr<LlmReplicaControllerConfig>,
                    std::shared_ptr<BaseRequestPrioritizerConfig>,
                    std::shared_ptr<BaseReplicasetSchedulerConfig>,
                    std::size_t>(),
           py::arg("num_replicas"), py::arg("replica_controller_config"),
           py::arg("request_prioritizer_config"),
           py::arg("replicaset_scheduler_config"),
           py::arg("num_tokenizer_workers"))
      .def_readonly("num_tokenizer_workers",
                    &LlmReplicasetControllerConfig::num_tokenizer_workers)
      .def(pybind11::pickle(
          [](const LlmReplicasetControllerConfig& self) {
            return py::make_tuple(
                self.num_replicas, self.replica_controller_config,
                self.request_prioritizer_config,
                self.replicaset_scheduler_config, self.num_tokenizer_workers);
          },
          [](py::tuple t) {
            ASSERT_VALID_RUNTIME(
                t.size() == 5,
                "Invalid pickled state for LlmReplicasetControllerConfig!");

            return LlmReplicasetControllerConfig(
                t[0].cast<std::size_t>(),
                t[1].cast<std::shared_ptr<LlmReplicaControllerConfig>>(),
                t[2].cast<std::shared_ptr<BaseRequestPrioritizerConfig>>(),
                t[3].cast<std::shared_ptr<BaseReplicasetSchedulerConfig>>(),
                t[4].cast<std::size_t>());
          }));
}
//==============================================================================
void InitConfigsPybindSubmodule(py::module_& pm) {
  auto m = pm.def_submodule("configs", "Configs submodule");

  // Call individual binding functions
  InitModelConfigPybindClass(m);
  InitParallelConfigPybindClass(m);
  InitReplicaResourceConfigPybindClass(m);
  InitTransferEngineConfigPybindClass(m);
  InitCacheConfigPybindClass(m);
  InitMetricsConfigPybindClass(m);
  InitWorkerConfigPybindClass(m);
  InitBaseReplicaSchedulerConfigPybindClass(m);
  InitFixedChunkReplicaSchedulerConfigPybindClass(m);
  InitDynamicChunkReplicaSchedulerConfigPybindClass(m);
  InitSpaceSharingReplicaSchedulerConfigPybindClass(m);
  InitBaseRequestPrioritizerConfigPybindClass(m);
  InitFcfsRequestPrioritizerConfigPybindClass(m);
  InitEdfRequestPrioritizerConfigPybindClass(m);
  InitLrsRequestPrioritizerConfigPybindClass(m);
  InitBaseReplicasetSchedulerConfigPybindClass(m);
  InitPullReplicasetSchedulerConfigPybindClass(m);
  InitRoundRobinReplicasetSchedulerConfigPybindClass(m);
  InitBaseReplicaControllerConfigPybindClass(m);
  InitLlmReplicaControllerConfigPybindClass(m);
  InitBaseReplicasetControllerConfigPybindClass(m);
  InitLlmReplicasetControllerConfigPybindClass(m);
}
//==============================================================================
}  // namespace vajra
//==============================================================================
