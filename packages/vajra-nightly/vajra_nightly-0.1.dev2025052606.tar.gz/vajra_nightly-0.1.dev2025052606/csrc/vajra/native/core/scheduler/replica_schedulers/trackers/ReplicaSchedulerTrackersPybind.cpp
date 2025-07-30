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
#include "native/core/scheduler/replica_schedulers/trackers/ReplicaSchedulerTrackersPybind.h"
//==============================================================================
// clang-format off
// Include vidur headers
#include "vidur/execution_time_predictor/execution_time_predictor.h"
// clang-format on
//==============================================================================
#include "commons/TorchCommon.h"
#include "native/configs/CacheConfig.h"
#include "native/configs/ModelConfig.h"
#include "native/configs/ParallelConfig.h"
#include "native/core/scheduler/replica_schedulers/trackers/BatchFormationTracker.h"
#include "native/core/scheduler/replica_schedulers/trackers/BatchFormationTrackerWithRuntimePrediction.h"
#include "native/core/scheduler/replica_schedulers/trackers/KvpBatchTracker.h"
#include "native/core/scheduler/replica_schedulers/trackers/KvpStateTracker.h"
//==============================================================================
namespace vajra {
//==============================================================================
void InitKvpBatchTrackerPybind(py::module& m) {
  py::class_<KvpBatchTracker>(m, "KvpBatchTracker")
      .def(py::init<std::size_t>())
      .def("add_sequence", &KvpBatchTracker::AddSequence, py::arg("seq"),
           py::arg("num_q_tokens"), py::arg("active_kvp_group_ids"),
           py::arg("kv_token_info"), py::arg("num_processed_tokens"))
      .def("_get_q_tokens_for_kvp_groups",
           &KvpBatchTracker::GetQTokensForKvpGroups,
           py::arg("active_kvp_group_ids"))
      .def("get_free_kvp_groups", &KvpBatchTracker::GetFreeKvpGroups,
           py::arg("token_threshold") = ALLOCATION_MAX_TOKEN_THRESHOLD)
      .def("get_per_group_sequences", &KvpBatchTracker::GetPerGroupSequences,
           py::arg("kvp_group_id"))
      .def("get_per_group_q_tokens", &KvpBatchTracker::GetPerGroupQTokens,
           py::arg("kvp_group_id"))
      .def("get_per_group_kv_tokens", &KvpBatchTracker::GetPerGroupKvTokens,
           py::arg("kvp_group_id"))
      .def("get_per_group_active_kvp_groups",
           &KvpBatchTracker::GetPerGroupActiveKvpGroups,
           py::arg("kvp_group_id"))
      .def("get_per_group_last_kvp_group_ids",
           &KvpBatchTracker::GetPerGroupLastKvpGroupIds,
           py::arg("kvp_group_id"));
}
//==============================================================================
void InitKvpStateTrackerPybind(py::module& m) {
  py::class_<KvpStateTracker, std::shared_ptr<KvpStateTracker>>(
      m, "KvpStateTracker")
      .def(py::init<const ModelConfig&, const CacheConfig&,
                    const ParallelConfig&, std::size_t>(),
           py::arg("model_config"), py::arg("cache_config"),
           py::arg("parallel_config"), py::arg("num_gpu_blocks"))
      .def("start_batch_formation", &KvpStateTracker::StartBatchFormation)
      .def("get_batch_tracker_q_tokens",
           &KvpStateTracker::GetBatchTrackerQTokens, py::arg("seq"))
      .def("get_batch_tracker_free_groups",
           &KvpStateTracker::GetBatchTrackerFreeGroups)
      .def("add_sequence_to_batch", &KvpStateTracker::AddSequenceToBatch,
           py::arg("seq"), py::arg("num_q_tokens"),
           py::arg("active_kvp_group_ids"))
      .def("get_batch_tracker_per_group_info",
           &KvpStateTracker::GetBatchTrackerPerGroupInfo,
           py::arg("kvp_group_id"))
      .def("get_max_seq_len", &KvpStateTracker::GetMaxSeqLen)
      .def("get_allocation_order", &KvpStateTracker::GetAllocationOrder,
           py::arg("kvp_group_ids"))
      .def("allocate", &KvpStateTracker::Allocate, py::arg("seq"))
      .def("free_seq", &KvpStateTracker::FreeSeq, py::arg("seq"))
      .def("get_last_kv_group_id", &KvpStateTracker::GetLastKvGroupId,
           py::arg("seq"))
      .def("can_append_slot", &KvpStateTracker::CanAppendSlot, py::arg("seq"))
      .def("append_slot", &KvpStateTracker::AppendSlot, py::arg("seq"),
           py::arg("num_total_blocks"))
      .def("get_active_kvp_group_ids", &KvpStateTracker::GetActiveKvpGroupIds,
           py::arg("seq"))
      .def("update_prefill_work", &KvpStateTracker::UpdatePrefillWork,
           py::arg("seq"), py::arg("current_tokens"), py::arg("new_tokens"))
      .def("get_kvp_group_block_counter",
           &KvpStateTracker::GetKvpGroupBlockCounter, py::arg("seq_id"))
      .def("get_sequence_kv_token_info",
           &KvpStateTracker::GetSequenceKvTokenInfo, py::arg("seq"),
           py::arg("active_kvp_group_ids"))
      .def("get_max_num_tokens_per_kvp_group",
           &KvpStateTracker::GetMaxNumTokensPerKvpGroup)
      .def("get_kvp_size", &KvpStateTracker::GetKvpSize);
}
//==============================================================================
void InitBatchFormationTrackerPybind(py::module& m) {
  py::class_<BatchFormationTracker, std::shared_ptr<BatchFormationTracker>>(
      m, "BatchFormationTracker")
      .def(py::init<const std::size_t, const std::size_t,
                    std::shared_ptr<KvpStateTracker>>(),
           py::arg("schedule_id"), py::arg("max_micro_batch_size"),
           py::arg("kvp_state_tracker"))
      .def("add_sequence", &BatchFormationTracker::AddSequence, py::arg("seq"),
           py::arg("num_q_tokens"))
      .def("add_ignored_sequence", &BatchFormationTracker::AddIgnoredSequence,
           py::arg("seq"))
      .def("add_preempted_sequence",
           &BatchFormationTracker::AddPreemptedSequence, py::arg("seq"))
      .def("can_add_sequences", &BatchFormationTracker::CanAddSequences)
      .def("get_batch", &BatchFormationTracker::GetBatch);
}
//==============================================================================
void InitBatchFormationTrackerWithRuntimePredictionPybind(py::module& m) {
  py::class_<BatchFormationTrackerWithRuntimePrediction, BatchFormationTracker,
             std::shared_ptr<BatchFormationTrackerWithRuntimePrediction>>(
      m, "BatchFormationTrackerWithRuntimePrediction")
      .def(
          py::init([](const std::size_t schedule_id,
                      const std::size_t max_micro_batch_size,
                      const std::size_t pipeline_parallel_size,
                      std::shared_ptr<KvpStateTracker> kvp_state_tracker,
                      const std::size_t max_chunk_size,
                      const std::size_t min_chunk_size,
                      py::capsule predictor_capsule) {
            ASSERT_VALID_RUNTIME(
                predictor_capsule,
                "Invalid or missing ExecutionTimePredictor capsule.");
            ASSERT_VALID_RUNTIME(std::string(predictor_capsule.name()) ==
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
            return std::make_shared<BatchFormationTrackerWithRuntimePrediction>(
                schedule_id, max_micro_batch_size, pipeline_parallel_size,
                kvp_state_tracker, max_chunk_size, min_chunk_size,
                predictor_shared);
          }),
          py::arg("schedule_id"), py::arg("max_micro_batch_size"),
          py::arg("pipeline_parallel_size"), py::arg("kvp_state_tracker"),
          py::arg("max_chunk_size"), py::arg("min_chunk_size"),
          py::arg("execution_time_predictor_capsule"))
      .def("add_sequence",
           &BatchFormationTrackerWithRuntimePrediction::AddSequence,
           py::arg("seq"), py::arg("num_q_tokens"))
      .def("get_batch_execution_time",
           &BatchFormationTrackerWithRuntimePrediction::GetBatchExecutionTime,
           py::arg("kvp_group_id"))
      .def("get_batch_execution_time_for_kvp_groups",
           &BatchFormationTrackerWithRuntimePrediction::
               GetBatchExecutionTimeForKvpGroups,
           py::arg("kvp_group_ids"))
      .def("get_max_chunk_size_for_seq",
           &BatchFormationTrackerWithRuntimePrediction::GetMaxChunkSizeForSeq,
           py::arg("seq"), py::arg("active_kvp_group_ids"),
           py::arg("target_batch_time"));
}
//==============================================================================
void InitReplicaSchedulerTrackersPybindSubmodule(py::module& pm) {
  auto m = pm.def_submodule("trackers", "ReplicaSchedulerTrackers submodule");

  InitKvpBatchTrackerPybind(m);
  InitKvpStateTrackerPybind(m);
  InitBatchFormationTrackerPybind(m);
  InitBatchFormationTrackerWithRuntimePredictionPybind(m);
}
//==============================================================================
}  // namespace vajra
//==============================================================================
