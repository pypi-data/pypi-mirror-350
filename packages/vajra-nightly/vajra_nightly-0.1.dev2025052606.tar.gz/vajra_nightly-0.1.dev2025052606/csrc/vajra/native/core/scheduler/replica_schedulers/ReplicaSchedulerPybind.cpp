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
#include "native/core/scheduler/replica_schedulers/ReplicaSchedulerPybind.h"
//==============================================================================
#include "commons/TorchCommon.h"
#include "native/configs/ReplicaSchedulerConfig.h"
#include "native/core/scheduler/replica_schedulers/DynamicChunkReplicaScheduler.h"
#include "native/core/scheduler/replica_schedulers/FixedChunkReplicaScheduler.h"
#include "native/core/scheduler/replica_schedulers/SpaceSharingReplicaScheduler.h"
#include "native/core/scheduler/replica_schedulers/trackers/ReplicaSchedulerTrackersPybind.h"
#include "native/core/scheduler/request_prioritizers/BaseRequestPrioritizer.h"
#include "native/core/scheduler/request_prioritizers/LrsRequestPrioritizer.h"
#include "native/data_structures/Queues.h"
// clang-format off
// Include vidur headers
#include "vidur/execution_time_predictor/execution_time_predictor.h"
// clang-format on
//==============================================================================
namespace vajra {
//==============================================================================
// Trampoline class for BaseReplicaScheduler
class PyBaseReplicaScheduler : public BaseReplicaScheduler {
 public:
  // Inherit constructors from BaseReplicaScheduler so that Python can call
  // them.
  using BaseReplicaScheduler::BaseReplicaScheduler;

  std::size_t GetSeqNextNumQTokens(
      const MutableSequencePtr& seq,
      const BatchFormationTracker& batch_formation_tracker) const override {
    PYBIND11_OVERRIDE(std::size_t,                  // Return type
                      BaseReplicaScheduler,         // Parent class
                      GetSeqNextNumQTokens,         // Name of function in C++
                      seq, batch_formation_tracker  // Arguments
    );
  }
};
//==============================================================================
void InitFixedChunkReplicaSchedulerPybind(py::module_& m) {
  py::class_<FixedChunkReplicaScheduler, BaseReplicaScheduler,
             std::shared_ptr<FixedChunkReplicaScheduler>>(
      m, "FixedChunkReplicaScheduler")
      .def(py::init(
               [](const ModelConfig& model_config,
                  const std::shared_ptr<FixedChunkReplicaSchedulerConfig>&
                      scheduler_config,
                  const CacheConfig& cache_config,
                  const ParallelConfig& parallel_config,
                  std::size_t num_gpu_blocks,
                  SequencePriorityQueuePtr waiting_queue,
                  std::shared_ptr<BaseRequestPrioritizer> request_prioritizer) {
                 return std::make_shared<FixedChunkReplicaScheduler>(
                     model_config, scheduler_config, cache_config,
                     parallel_config, num_gpu_blocks, waiting_queue,
                     request_prioritizer);
               }),
           py::arg("model_config"), py::arg("scheduler_config"),
           py::arg("cache_config"), py::arg("parallel_config"),
           py::arg("num_gpu_blocks"), py::arg("waiting_queue"),
           py::arg("request_prioritizer"));
}
//==============================================================================

void InitDynamicChunkReplicaSchedulerPybind(py::module_& m) {
  py::class_<DynamicChunkReplicaScheduler, BaseReplicaScheduler,
             std::shared_ptr<DynamicChunkReplicaScheduler>>(
      m, "DynamicChunkReplicaScheduler")
      .def(py::init(
               [](const ModelConfig& model_config,
                  const std::shared_ptr<DynamicChunkReplicaSchedulerConfig>&
                      scheduler_config,
                  const CacheConfig& cache_config,
                  const ParallelConfig& parallel_config,
                  std::size_t num_gpu_blocks,
                  SequencePriorityQueuePtr waiting_queue,
                  std::shared_ptr<BaseRequestPrioritizer> request_prioritizer,
                  py::capsule predictor_capsule) {
                 ASSERT_VALID_RUNTIME(
                     predictor_capsule,
                     "Invalid or missing ExecutionTimePredictor capsule.");
                 ASSERT_VALID_RUNTIME(
                     std::string(predictor_capsule.name()) ==
                         "ExecutionTimePredictorPtr",
                     "Invalid ExecutionTimePredictor capsule.");

                 // Retrieve pointer to the std::shared_ptr
                 auto* sp_predictor_ptr = static_cast<std::shared_ptr<
                     vidur::execution_time_predictor::ExecutionTimePredictor>*>(
                     predictor_capsule.get_pointer());

                 ASSERT_VALID_RUNTIME(
                     sp_predictor_ptr,
                     "Invalid or missing ExecutionTimePredictor capsule.");

                 // Copy the shared_ptr so we have local ownership
                 auto predictor_shared = *sp_predictor_ptr;
                 ASSERT_VALID_RUNTIME(
                     predictor_shared,
                     "Invalid or missing ExecutionTimePredictor capsule.");

                 // Create the object with the C++ predictor reference
                 return std::make_shared<DynamicChunkReplicaScheduler>(
                     model_config, scheduler_config, cache_config,
                     parallel_config, num_gpu_blocks, waiting_queue,
                     request_prioritizer, predictor_shared);
               }),
           py::arg("model_config"), py::arg("scheduler_config"),
           py::arg("cache_config"), py::arg("parallel_config"),
           py::arg("num_gpu_blocks"), py::arg("waiting_queue"),
           py::arg("request_prioritizer"),
           py::arg("execution_time_predictor_capsule"));
}
//==============================================================================

void InitSpaceSharingReplicaSchedulerPybind(py::module_& m) {
  py::class_<SpaceSharingReplicaScheduler, DynamicChunkReplicaScheduler,
             std::shared_ptr<SpaceSharingReplicaScheduler>>(
      m, "SpaceSharingReplicaScheduler")
      .def(py::init(
               [](const ModelConfig& model_config,
                  const std::shared_ptr<SpaceSharingReplicaSchedulerConfig>&
                      scheduler_config,
                  const CacheConfig& cache_config,
                  const ParallelConfig& parallel_config,
                  std::size_t num_gpu_blocks,
                  SequencePriorityQueuePtr waiting_queue,
                  std::shared_ptr<BaseRequestPrioritizer> request_prioritizer,
                  py::capsule predictor_capsule) {
                 ASSERT_VALID_RUNTIME(
                     predictor_capsule,
                     "Invalid or missing ExecutionTimePredictor capsule.");
                 ASSERT_VALID_RUNTIME(
                     std::string(predictor_capsule.name()) ==
                         "ExecutionTimePredictorPtr",
                     "Invalid ExecutionTimePredictor capsule.");

                 // Retrieve pointer to the std::shared_ptr
                 auto* sp_predictor_ptr = static_cast<std::shared_ptr<
                     vidur::execution_time_predictor::ExecutionTimePredictor>*>(
                     predictor_capsule.get_pointer());

                 ASSERT_VALID_RUNTIME(
                     sp_predictor_ptr,
                     "Invalid or missing ExecutionTimePredictor capsule.");

                 // Copy the shared_ptr so we have local ownership
                 auto predictor_shared = *sp_predictor_ptr;
                 ASSERT_VALID_RUNTIME(
                     predictor_shared,
                     "Invalid or missing ExecutionTimePredictor capsule.");

                 // Create the object with the C++ predictor reference
                 return std::make_shared<SpaceSharingReplicaScheduler>(
                     model_config, scheduler_config, cache_config,
                     parallel_config, num_gpu_blocks, waiting_queue,
                     request_prioritizer, predictor_shared);
               }),
           py::arg("model_config"), py::arg("scheduler_config"),
           py::arg("cache_config"), py::arg("parallel_config"),
           py::arg("num_gpu_blocks"), py::arg("waiting_queue"),
           py::arg("request_prioritizer"),
           py::arg("execution_time_predictor_capsule"));
}
//==============================================================================

void InitBaseReplicaSchedulerPybind(py::module_& m) {
  py::class_<BaseReplicaScheduler, PyBaseReplicaScheduler,
             std::shared_ptr<BaseReplicaScheduler>>(m, "BaseReplicaScheduler")
      .def(py::init<const ModelConfig&,
                    const std::shared_ptr<const BaseReplicaSchedulerConfig>&,
                    const CacheConfig&, const ParallelConfig&, std::size_t,
                    SequencePriorityQueuePtr,
                    std::shared_ptr<BaseRequestPrioritizer>>(),
           py::arg("model_config"), py::arg("scheduler_config"),
           py::arg("cache_config"), py::arg("parallel_config"),
           py::arg("num_gpu_blocks"), py::arg("waiting_queue"),
           py::arg("request_prioritizer"))
      .def("reset_state", &BaseReplicaScheduler::ResetState)
      .def("add_partial_prefill", &BaseReplicaScheduler::AddPartialPrefill)
      .def("on_stage_completed", &BaseReplicaScheduler::OnStageCompleted)
      .def("on_step_completed", &BaseReplicaScheduler::OnStepCompleted)
      .def("schedule", &BaseReplicaScheduler::Schedule)
      .def("free_finished_seqs", &BaseReplicaScheduler::FreeFinishedSeqs)
      .def("is_seq_allocated", &BaseReplicaScheduler::IsSeqAllocated);
}
//==============================================================================

void InitReplicaSchedulerPybindSubmodule(py::module_& pm) {
  auto m = pm.def_submodule("replica_schedulers", "ReplicaScheduler submodule");

  // Initialize trackers submodule
  InitReplicaSchedulerTrackersPybindSubmodule(m);

  // Initialize BaseReplicaSchedulerConfig binding
  InitBaseReplicaSchedulerPybind(m);

  // Initialize replica scheduler classes
  InitFixedChunkReplicaSchedulerPybind(m);
  InitDynamicChunkReplicaSchedulerPybind(m);
  InitSpaceSharingReplicaSchedulerPybind(m);
}
//==============================================================================
}  // namespace vajra
//==============================================================================
