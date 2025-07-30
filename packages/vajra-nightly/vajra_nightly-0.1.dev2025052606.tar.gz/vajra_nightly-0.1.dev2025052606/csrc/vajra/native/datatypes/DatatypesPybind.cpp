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
#include "native/datatypes/DatatypesPybind.h"
//==============================================================================
#include "commons/Logging.h"
#include "native/data_structures/Queues.h"
#include "native/datatypes/BaseSequenceWithPriority.h"
#include "native/datatypes/CommInfo.h"
#include "native/datatypes/RequestOutput.h"
#include "native/datatypes/SamplerOutput.h"
#include "native/datatypes/SamplingParams.h"
#include "native/datatypes/SchedulerOutput.h"
#include "native/datatypes/Sequence.h"
#include "native/datatypes/SequenceMetadata.h"
#include "native/datatypes/SequenceScheduleMetadata.h"
#include "native/datatypes/SequenceState.h"
#include "native/datatypes/SequenceStatus.h"
#include "native/datatypes/StepInputs.h"
#include "native/datatypes/StepMicrobatchOutputs.h"
#include "native/datatypes/StepOutputs.h"
//==============================================================================
namespace vajra {
//==============================================================================
class PySequenceWithPriority : public BaseSequenceWithPriority {
 public:
  [[nodiscard]] float GetPriority() const override {
    PYBIND11_OVERRIDE(float, BaseSequenceWithPriority, GetPriority);
  }
};
//==============================================================================
void InitCommInfoPybindClass(py::module_& m) {
  py::class_<CommInfo, std::shared_ptr<CommInfo>>(m, "CommInfo")
      .def(py::init<std::string>(), py::arg("driver_ip"))
      .def("__str__", &CommInfo::ToString)
      .def("__repr__", &CommInfo::ToString)
      .def_readonly("distributed_init_method",
                    &CommInfo::distributed_init_method)
      .def_readonly("engine_ip_address", &CommInfo::engine_ip_address)
      .def_readonly("enqueue_socket_port", &CommInfo::enqueue_socket_port)
      .def_readonly("output_socket_port", &CommInfo::output_socket_port)
      .def_readonly("microbatch_socket_port",
                    &CommInfo::microbatch_socket_port)
      .def(py::pickle(
          [](const CommInfo& p) {  // __getstate__
            return py::make_tuple(p.distributed_init_method,
                                  p.engine_ip_address, p.enqueue_socket_port,
                                  p.output_socket_port,
                                  p.microbatch_socket_port);
          },
          [](py::tuple t) {  // __setstate__
            ASSERT_VALID_RUNTIME(t.size() == 5,
                                 "Invalid pickled state for CommInfo!");

            return CommInfo(t[0].cast<std::string>(), t[1].cast<std::string>(),
                            t[2].cast<std::size_t>(), t[3].cast<std::size_t>(),
                            t[4].cast<std::size_t>());
          }));
}
//==============================================================================
void InitSequenceMetadataPybindClass(py::module_& m) {
  py::class_<SequenceMetadata, std::shared_ptr<SequenceMetadata>>(
      m, "SequenceMetadata")
      .def(py::init<std::size_t, std::string, std::size_t, std::size_t,
                    std::vector<int>, std::vector<std::size_t>, bool>(),
           py::arg("schedule_id"), py::arg("seq_id"), py::arg("num_q_tokens"),
           py::arg("num_kv_tokens"), py::arg("block_table"),
           py::arg("kvp_group_ids"), py::arg("save_kv_cache"))
      .def("__str__", &SequenceMetadata::ToString)
      .def("__repr__", &SequenceMetadata::ToString)
      .def_readonly("schedule_id", &SequenceMetadata::schedule_id)
      .def_readonly("seq_id", &SequenceMetadata::seq_id)
      .def_readonly("num_q_tokens", &SequenceMetadata::num_q_tokens)
      .def_readonly("num_kv_tokens", &SequenceMetadata::num_kv_tokens)
      .def_readonly("block_table", &SequenceMetadata::block_table)
      .def_readonly("kvp_group_ids", &SequenceMetadata::kvp_group_ids)
      .def_readonly("save_kv_cache", &SequenceMetadata::save_kv_cache)
      .def_readonly("is_kvp_request", &SequenceMetadata::is_kvp_request);
}
//==============================================================================
void InitLogicalTokenBlockPybindClass(py::module_& m) {
  py::class_<LogicalTokenBlock, std::shared_ptr<LogicalTokenBlock>>(
      m, "LogicalTokenBlock")
      .def(py::init<std::size_t, std::size_t>(), py::arg("block_number"),
           py::arg("block_size"))
      .def("__str__", &LogicalTokenBlock::ToString)
      .def("__repr__", &LogicalTokenBlock::ToString)
      .def("append_tokens", &LogicalTokenBlock::AppendTokens)
      .def("get_last_token_id", &LogicalTokenBlock::GetLastTokenId)
      .def_readonly("block_number", &LogicalTokenBlock::block_number)
      .def_readonly("block_size", &LogicalTokenBlock::block_size)
      .def_property_readonly("token_ids", &LogicalTokenBlock::GetTokenIds)
      .def_property_readonly("num_tokens", &LogicalTokenBlock::GetNumTokens)
      .def_property_readonly("is_empty", &LogicalTokenBlock::IsEmpty)
      .def_property_readonly("num_empty_slots",
                             &LogicalTokenBlock::NumEmptySlots)
      .def_property_readonly("is_full", &LogicalTokenBlock::IsFull)
      .def(py::pickle(
          [](const LogicalTokenBlock& p) {  // __getstate__
            return py::make_tuple(p.block_number, p.block_size,
                                  p.GetTokenIdsCopy(), p.GetNumTokens());
          },
          [](py::tuple t) {  // __setstate__
            ASSERT_VALID_RUNTIME(
                t.size() == 4, "Invalid pickled state for LogicalTokenBlock!");

            return LogicalTokenBlock(t[0].cast<std::size_t>(),
                                     t[1].cast<std::size_t>(),
                                     t[2].cast<std::vector<std::size_t>>(),
                                     t[3].cast<std::size_t>());
          }));
}
//==============================================================================
void InitSamplerOutputPybindClass(py::module_& m) {
  py::class_<SamplerOutput, SamplerOutputPtr>(m, "SamplerOutput")
      .def(py::init<std::size_t, std::string, std::vector<TokenId>>(),
           py::arg("schedule_id"), py::arg("seq_id"), py::arg("output_tokens"))
      .def("__str__", &SamplerOutput::ToString)
      .def("__repr__", &SamplerOutput::ToString)
      .def_property_readonly("schedule_id", &SamplerOutput::GetScheduleId)
      .def_property_readonly("seq_id", &SamplerOutput::GetSeqId)
      .def_property_readonly("output_tokens",
                             &SamplerOutput::GetOutputTokens)
      .def(py::pickle(
          [](const SamplerOutput& p) {  // __getstate__
            return py::make_tuple(p.GetScheduleId(), p.GetSeqIdCopy(),
                                  p.GetOutputTokensCopy());
          },
          [](py::tuple t) {  // __setstate__
            ASSERT_VALID_RUNTIME(t.size() == 3,
                                 "Invalid pickled state for SamplerOutput!");

            return SamplerOutput(t[0].cast<std::size_t>(),
                                 t[1].cast<std::string>(),
                                 t[2].cast<std::vector<TokenId>>());
          }));
}
//==============================================================================
void InitSequenceStatusPybindEnum(py::module_& m) {
  py::enum_<SequenceStatus>(m, "SequenceStatus")
      .value("WAITING", SequenceStatus::Waiting)
      .value("WAITING_PREEMPTED", SequenceStatus::WaitingPreempted)
      .value("RUNNING", SequenceStatus::Running)
      .value("PAUSED", SequenceStatus::Paused)
      .value("FINISHED_STOPPED", SequenceStatus::FinishedStopped)
      .value("FINISHED_LENGTH_CAPPED", SequenceStatus::FinishedLengthCapped)
      .value("FINISHED_IGNORED", SequenceStatus::FinishedIgnored)
      .def_static("is_finished", &sequence_status::IsFinished)
      .def_static("is_executing", &sequence_status::IsExecuting)
      .def_static("is_waiting", &sequence_status::IsWaiting)
      .def_static("is_waiting_preempted", &sequence_status::IsWaitingPreempted)
      .def_static("is_paused", &sequence_status::IsPaused)
      .def_static("is_running", &sequence_status::IsRunning)
      .def_static("get_finished_reason", &sequence_status::GetFinishedReason);
}
//==============================================================================
void InitSamplingTypePybindEnum(py::module_& m) {
  py::enum_<SamplingType>(m, "SamplingType")
      .value("GREEDY", SamplingType::Greedy)
      .value("RANDOM", SamplingType::Random);
}
//==============================================================================
void InitSamplingParamsPybindClass(py::module_& m) {
  py::class_<SamplingParams>(m, "SamplingParams")
      .def(py::init<float, float, int, bool, std::size_t>(),
           py::arg("temperature") = 1.0f, py::arg("top_p") = 1.0f,
           py::arg("top_k") = -1, py::arg("ignore_eos") = false,
           py::arg("max_tokens") = 2048)
      .def("__str__", &SamplingParams::ToString)
      .def("__repr__", &SamplingParams::ToString)
      .def_readonly("temperature", &SamplingParams::temperature)
      .def_readonly("top_p", &SamplingParams::top_p)
      .def_readonly("top_k", &SamplingParams::top_k)
      .def_readonly("ignore_eos", &SamplingParams::ignore_eos)
      .def_readonly("max_tokens", &SamplingParams::max_tokens)
      .def_property_readonly("sampling_type",
                             &SamplingParams::GetSamplingType)
      .def(py::pickle(
          [](const SamplingParams& p) {  // __getstate__
            return py::make_tuple(p.temperature, p.top_p, p.top_k, p.ignore_eos,
                                  p.max_tokens);
          },
          [](py::tuple t) {  // __setstate__
            ASSERT_VALID_RUNTIME(t.size() == 5,
                                 "Invalid pickled state for SamplingParams!");

            return SamplingParams(t[0].cast<double>(), t[1].cast<double>(),
                                  t[2].cast<int>(), t[3].cast<bool>(),
                                  t[4].cast<std::size_t>());
          }));
}
//==============================================================================
void InitSequenceStatePybindClass(py::module_& m) {
  py::class_<SequenceState>(m, "SequenceState")
      .def(py::init<std::string, double, std::size_t>(), py::arg("id"),
           py::arg("arrived_at"), py::arg("num_prompt_tokens"))
      .def("__str__", &SequenceState::ToString)
      .def("__repr__", &SequenceState::ToString)
      .def_property_readonly("id", &SequenceState::GetId)
      .def_property_readonly("arrived_at", &SequenceState::GetArrivedAt)
      .def_property_readonly("num_prompt_tokens",
                             &SequenceState::GetNumPromptTokens)
      .def_property_readonly("num_output_tokens",
                             &SequenceState::GetNumOutputTokens)
      .def_property_readonly("num_total_tokens",
                             &SequenceState::GetNumTotalTokens)
      .def_property("status", &SequenceState::GetStatus,
                    &SequenceState::SetStatus)
      .def_property_readonly("is_scheduled", &SequenceState::GetIsScheduled)
      .def_property_readonly("is_completed", &SequenceState::GetIsCompleted)
      .def_property_readonly("scheduled_at", &SequenceState::GetScheduledAt)
      .def_property_readonly("completed_at", &SequenceState::GetCompletedAt)
      .def_property_readonly("prompt_processing_completed_at",
                             &SequenceState::GetPromptProcessingCompletedAt)
      .def_property_readonly("e2e_time", &SequenceState::GetE2ETime)
      .def_property_readonly("e2e_time_piecewise_normalized",
                             &SequenceState::GetE2ETimePiecewiseNormalized)
      .def_property_readonly("e2e_time_normalized",
                             &SequenceState::GetE2ETimeNormalized)
      .def_property_readonly("e2e_prefill_time",
                             &SequenceState::GetE2EPrefillTime)
      .def_property_readonly("e2e_prefill_time_normalized",
                             &SequenceState::GetE2EPrefillTimeNormalized)
      .def_property_readonly(
          "e2e_prefill_time_piecewise_normalized",
          &SequenceState::GetE2EPrefillTimePiecewiseNormalized)
      .def_property_readonly(
          "prefill_execution_plus_preemption_time",
          &SequenceState::GetPrefillExecutionPlusPreemptionTime)
      .def_property_readonly(
          "decode_execution_plus_preemption_time",
          &SequenceState::GetDecodeExecutionPlusPreemptionTime)
      .def_property_readonly(
          "prefill_execution_plus_preemption_time_normalized",
          &SequenceState::GetPrefillExecutionPlusPreemptionTimeNormalized)
      .def_property_readonly(
          "decode_execution_plus_preemption_time_normalized",
          &SequenceState::GetDecodeExecutionPlusPreemptionTimeNormalized)
      .def_property_readonly("scheduling_delay",
                             &SequenceState::GetSchedulingDelay)
      .def_property_readonly("execution_time", &SequenceState::GetExecutionTime)
      .def_property_readonly("execution_time_normalized",
                             &SequenceState::GetExecutionTimeNormalized)
      .def_property_readonly("preempted_time", &SequenceState::GetPreemptedTime)
      .def_property_readonly("execution_plus_preemption_time",
                             &SequenceState::GetExecutionPlusPreemptionTime)
      .def_property_readonly(
          "execution_plus_preemption_time_normalized",
          &SequenceState::GetExecutionPlusPreemptionTimeNormalized)
      .def_property_readonly("last_token_generation_time",
                             &SequenceState::GetLastTokenGenerationTime)
      .def_property_readonly("num_restarts", &SequenceState::GetNumRestarts)
      .def_property_readonly("num_pauses", &SequenceState::GetNumPauses)
      .def_property_readonly("is_ignore_finished",
                             &SequenceState::GetIsIgnoreFinished)
      .def("on_prompt_processing_completed",
           &SequenceState::OnPromptProcessingCompleted)
      .def("on_token_generated", &SequenceState::OnTokenGenerated);
}
//==============================================================================
void InitUserSequenceParamsPybindClass(py::module_& m) {
  py::class_<UserSequenceParams, MutableUserSequenceParamsPtr>(
      m, "UserSequenceParams")
      .def(py::init([](std::string seq_id, std::string prompt,
                       TokenIds prompt_token_ids, TimeS arrival_time,
                       SamplingParams sampling_params) {
             return vajra::UserSequenceParams(
                 seq_id, prompt, std::make_shared<TokenIds>(prompt_token_ids),
                 arrival_time, sampling_params);
           }),
           py::arg("seq_id"), py::arg("prompt"), py::arg("prompt_token_ids"),
           py::arg("arrival_time"), py::arg("sampling_params"))
      .def("__str__", &UserSequenceParams::ToString)
      .def("__repr__", &UserSequenceParams::ToString)
      .def_readonly("seq_id", &UserSequenceParams::seq_id)
      .def_readonly("prompt", &UserSequenceParams::prompt)
      .def_property_readonly("prompt_token_ids",
                             [](const vajra::UserSequenceParams& self) {
                               return self.prompt_token_ids
                                          ? *(self.prompt_token_ids)
                                          : std::vector<TokenId>();
                             })
      .def_readonly("arrival_time", &UserSequenceParams::arrival_time)
      .def_readonly("sampling_params", &UserSequenceParams::sampling_params);
}
//==============================================================================
void InitSequenceParamsPybindClass(py::module_& m) {
  py::class_<SequenceParams>(m, "SequenceParams")
      .def(py::init([](std::string seq_id, std::string prompt,
                       TokenIds prompt_token_ids, std::size_t block_size,
                       TokenId eos_token_id, TimeS arrival_time,
                       SamplingParams sampling_params) {
             return vajra::SequenceParams(
                 seq_id, prompt, std::make_shared<TokenIds>(prompt_token_ids),
                 block_size, eos_token_id, arrival_time, sampling_params);
           }),
           py::arg("seq_id"), py::arg("prompt"), py::arg("prompt_token_ids"),
           py::arg("block_size"), py::arg("eos_token_id"),
           py::arg("arrival_time"), py::arg("sampling_params"))
      .def("__str__", &SequenceParams::ToString)
      .def("__repr__", &SequenceParams::ToString)
      .def_readonly("seq_id", &SequenceParams::seq_id)
      .def_readonly("prompt", &SequenceParams::prompt)
      .def_property_readonly("prompt_token_ids",
                             [](const vajra::SequenceParams& self) {
                               return self.prompt_token_ids
                                          ? *(self.prompt_token_ids)
                                          : std::vector<TokenId>();
                             })
      .def_readonly("block_size", &SequenceParams::block_size)
      .def_readonly("eos_token_id", &SequenceParams::eos_token_id)
      .def_readonly("arrival_time", &SequenceParams::arrival_time)
      .def_readonly("sampling_params", &SequenceParams::sampling_params)
      .def(py::pickle(
          [](const SequenceParams& p) {  // __getstate__
            return py::make_tuple(p.seq_id, p.prompt, *p.prompt_token_ids,
                                  p.block_size, p.eos_token_id, p.arrival_time,
                                  p.sampling_params);
          },
          [](py::tuple t) {  // __setstate__
            ASSERT_VALID_RUNTIME(t.size() == 7,
                                 "Invalid pickled state for SequenceParams!");
            auto token_ids = t[2].cast<TokenIds>();
            return SequenceParams(
                t[0].cast<std::string>(), t[1].cast<std::string>(),
                std::make_shared<TokenIds>(token_ids), t[3].cast<std::size_t>(),
                t[4].cast<TokenId>(), t[5].cast<double>(),
                t[6].cast<SamplingParams>());
          }));
}
//==============================================================================
void InitSequencePybindClass(py::module_& m) {
  py::class_<Sequence, MutableSequencePtr>(m, "Sequence")
      .def(py::init([](std::string seq_id, std::string prompt,
                       TokenIds prompt_token_ids, std::size_t block_size,
                       TokenId eos_token_id, TimeS arrival_time,
                       SamplingParams sampling_params) {
             return vajra::Sequence(
                 seq_id, prompt, std::make_shared<TokenIds>(prompt_token_ids),
                 block_size, eos_token_id, arrival_time, sampling_params);
           }),
           py::arg("seq_id"), py::arg("prompt"), py::arg("prompt_token_ids"),
           py::arg("block_size"), py::arg("eos_token_id"),
           py::arg("arrival_time"), py::arg("sampling_params"))
      .def(py::init<SequenceParams&>(), py::arg("params"))
      .def("__str__", &Sequence::ToString)
      .def("__repr__", &Sequence::ToString)
      .def_readonly("seq_id", &Sequence::seq_id)
      .def_readonly("prompt", &Sequence::prompt)
      .def_readonly("block_size", &Sequence::block_size)
      .def_readonly("eos_token_id", &Sequence::eos_token_id)
      .def_readonly("arrival_time", &Sequence::arrival_time)
      .def_readonly("sampling_params", &Sequence::sampling_params)
      .def_readwrite("output_text", &Sequence::output_text)
      .def_property("tokens", &Sequence::GetTokens, &Sequence::SetTokens)
      .def("append_tokens", &Sequence::ExtendTokens)
      .def_readwrite("prefix_offset", &Sequence::prefix_offset)
      .def_readwrite("read_offset", &Sequence::read_offset)
      .def_property_readonly("prompt_token_ids",
                             [](const vajra::Sequence& self) {
                               auto prompt_token_ids = self.GetPromptTokenIds();
                               return prompt_token_ids ? *(prompt_token_ids)
                                                       : std::vector<TokenId>();
                             })
      .def_property_readonly("output_token_ids",
                             [](const vajra::Sequence& self) {
                               auto output_token_ids = self.GetOutputTokenIds();
                               return output_token_ids ? *(output_token_ids)
                                                       : std::vector<TokenId>();
                             })
      .def_property_readonly("prompt_processing_finished",
                             &Sequence::GetPromptProcessingFinished)
      .def_property_readonly("prompt_stage_processing_finished",
                             &Sequence::GetPromptStageProcessingFinished)
      .def_property_readonly("logical_token_blocks",
                             &Sequence::GetLogicalTokenBlocks)
      .def_property_readonly("state", &Sequence::GetState)
      .def_property("status", &Sequence::GetStatus, &Sequence::SetStatus)
      .def("append_token_id", &Sequence::AppendTokenId)
      .def("__len__", &Sequence::Length)
      .def_property_readonly("prompt_len", &Sequence::GetPromptLength)
      .def_property_readonly("output_len", &Sequence::GetOutputLength)
      .def("update_tokens_processed", &Sequence::UpdateTokensProcessed)
      .def("update_prompt_tokens_processed",
           &Sequence::UpdatePromptTokensProcessed)
      .def("update_prompt_tokens_stage_processed",
           &Sequence::UpdatePromptTokensStageProcessed)
      .def("get_num_processable_tokens", &Sequence::GetNumProcessableTokens)
      .def("get_num_prompt_tokens_processed",
           &Sequence::GetNumPromptTokensProcessed)
      .def("get_num_prompt_tokens_stage_processed",
           &Sequence::GetNumPromptTokensStageProcessed)
      .def("get_num_tokens_stage_processed",
           &Sequence::GetNumTokensStageProcessed)
      .def("get_num_tokens_processed", &Sequence::GetNumTokensProcessed)
      .def("get_last_token_id", &Sequence::GetLastTokenId)
      .def("get_last_n_token_ids", &Sequence::GetLastNTokenIds, py::arg("n"),
           py::arg("truncate") = false)
      .def("is_finished", &Sequence::IsFinished)
      .def("is_waiting", &Sequence::IsWaiting)
      .def("is_paused", &Sequence::IsPaused)
      .def("is_running", &Sequence::IsRunning)
      .def("is_waiting_preempted", &Sequence::IsWaitingPreempted)
      .def("reset", &Sequence::Reset)
      .def("check_stop", &Sequence::CheckStop)
      .def("__str__", &Sequence::ToString)
      .def("__repr__", &Sequence::ToString)
      .def("get_params", &Sequence::GetParams);
}
//==============================================================================
void InitSequenceScheduleMetadataPybindClass(py::module_& m) {
  py::class_<SequenceScheduleMetadata,
             std::shared_ptr<SequenceScheduleMetadata>>(
      m, "SequenceScheduleMetadata")
      .def(py::init<std::size_t, std::string, std::size_t,
                    std::unordered_map<std::size_t, std::size_t>,
                    std::vector<std::size_t>>(),
           py::arg("schedule_id"), py::arg("seq_id"), py::arg("num_q_tokens"),
           py::arg("kvp_group_block_counter"), py::arg("kvp_group_ids"))
      .def("__str__", &SequenceScheduleMetadata::ToString)
      .def("__repr__", &SequenceScheduleMetadata::ToString)
      .def_readonly("schedule_id", &SequenceScheduleMetadata::schedule_id)
      .def_readonly("seq_id", &SequenceScheduleMetadata::seq_id)
      .def_readonly("num_q_tokens", &SequenceScheduleMetadata::num_q_tokens)
      .def_readonly("kvp_group_block_counter",
                    &SequenceScheduleMetadata::kvp_group_block_counter)
      .def_readonly("kvp_group_ids", &SequenceScheduleMetadata::kvp_group_ids)
      .def_readonly("is_kvp_request", &SequenceScheduleMetadata::is_kvp_request)
      .def(py::pickle(
          [](const SequenceScheduleMetadata& p) {
            return py::make_tuple(p.schedule_id, p.seq_id, p.num_q_tokens,
                                  p.kvp_group_block_counter, p.kvp_group_ids);
          },
          [](py::tuple t) {
            ASSERT_VALID_RUNTIME(
                t.size() == 5,
                "Invalid pickled state for SequenceScheduleMetadata");
            return SequenceScheduleMetadata(
                t[0].cast<std::size_t>(), t[1].cast<std::string>(),
                t[2].cast<std::size_t>(),
                t[3].cast<std::unordered_map<std::size_t, std::size_t>>(),
                t[4].cast<std::vector<std::size_t>>());
          }));
}
//==============================================================================
void InitSchedulerOutputPybindClass(py::module_& m) {
  py::class_<SchedulerOutput, std::shared_ptr<SchedulerOutput>>(
      m, "SchedulerOutput")
      .def(py::init<std::size_t, std::vector<std::string>,
                    std::vector<std::string>,
                    std::vector<SequenceScheduleMetadataPtr>>(),
           py::arg("id"), py::arg("ignored_seq_ids"),
           py::arg("preempted_seq_ids"), py::arg("seq_schedule_metadata_list"))
      .def("__str__", &SchedulerOutput::ToString)
      .def("__repr__", &SchedulerOutput::ToString)
      .def_readonly("id", &SchedulerOutput::id)
      .def_readonly("ignored_seq_ids", &SchedulerOutput::ignored_seq_ids)
      .def_readonly("preempted_seq_ids", &SchedulerOutput::preempted_seq_ids)
      .def_readonly("seq_schedule_metadata_list",
                    &SchedulerOutput::seq_schedule_metadata_list)
      .def_readonly("is_empty", &SchedulerOutput::is_empty)
      .def_readonly("has_no_output", &SchedulerOutput::has_no_output)
      .def(py::pickle(
          [](const SchedulerOutput& p) {
            return py::make_tuple(p.id, p.ignored_seq_ids, p.preempted_seq_ids,
                                  p.seq_schedule_metadata_list);
          },
          [](py::tuple t) {
            ASSERT_VALID_RUNTIME(t.size() == 4,
                                 "Invalid pickled state for SchedulerOutput");
            return SchedulerOutput(
                t[0].cast<std::size_t>(), t[1].cast<std::vector<std::string>>(),
                t[2].cast<std::vector<std::string>>(),
                t[3].cast<std::vector<SequenceScheduleMetadataPtr>>());
          }));
}
//==============================================================================
void InitRequestOutputPybindClass(py::module_& m) {
  py::class_<RequestOutput, std::shared_ptr<RequestOutput>>(m, "RequestOutput")
      .def(py::init<std::shared_ptr<Sequence>>(), py::arg("seq"))
      .def("__str__", &RequestOutput::ToString)
      .def("__repr__", &RequestOutput::ToString)
      .def_readonly("seq", &RequestOutput::seq)
      .def_readonly("finished", &RequestOutput::finished)
      .def_readonly("finish_reason", &RequestOutput::finish_reason)
      .def_property_readonly("text", &RequestOutput::GetText)
      .def_property_readonly("request_id", &RequestOutput::GetSeqId)
      .def_property_readonly("prompt", &RequestOutput::GetPrompt)
      .def_property_readonly("prompt_token_ids",
                             [](const vajra::RequestOutput& self) {
                               auto token_ids = self.GetPromptTokenIds();
                               return token_ids ? *(token_ids)
                                                : std::vector<TokenId>();
                             })
      .def_property_readonly("token_ids", [](const vajra::RequestOutput& self) {
        auto token_ids = self.GetTokenIds();
        return token_ids ? *(token_ids) : std::vector<TokenId>();
      });
}
//==============================================================================
void InitBaseSequenceWithPriorityPybindClass(py::module_& m) {
  py::class_<BaseSequenceWithPriority, PySequenceWithPriority,
             MutableBaseSequenceWithPriorityPtr>(m, "BaseSequenceWithPriority")
      .def("__str__", &BaseSequenceWithPriority::ToString)
      .def("__repr__", &BaseSequenceWithPriority::ToString)
      .def("__lt__",
           [](const BaseSequenceWithPriority& self,
              const BaseSequenceWithPriority& other) { return self < other; })
      .def("__gt__",
           [](const BaseSequenceWithPriority& self,
              const BaseSequenceWithPriority& other) { return self > other; })
      .def("__eq__",
           [](const BaseSequenceWithPriority& self,
              const BaseSequenceWithPriority& other) { return self == other; })
      .def("__ne__",
           [](const BaseSequenceWithPriority& self,
              const BaseSequenceWithPriority& other) { return self != other; })
      .def_property_readonly("seq", &BaseSequenceWithPriority::GetSequence)
      .def("get_priority", &BaseSequenceWithPriority::GetPriority);
}
//==============================================================================
void InitStepInputsPybindClass(py::module_& m) {
  py::class_<StepInputs, std::shared_ptr<StepInputs>>(m, "StepInputs")
      .def(py::init<SchedulerOutputPtr, std::vector<SequenceParams>,
                    std::vector<PendingStepOutput>>(),
           py::arg("scheduler_output"), py::arg("new_seq_params"),
           py::arg("pending_step_outputs"))
      .def("__str__", &StepInputs::ToString)
      .def("__repr__", &StepInputs::ToString)
      .def_readonly("scheduler_output", &StepInputs::scheduler_output)
      .def_readonly("new_seq_params", &StepInputs::new_seq_params)
      .def_readonly("pending_step_outputs", &StepInputs::pending_step_outputs);
}
//==============================================================================
void InitStepMicrobatchOutputsPybindClass(py::module_& m) {
  py::class_<StepMicrobatchOutputs, std::shared_ptr<StepMicrobatchOutputs>>(
      m, "StepMicrobatchOutputs")
      .def(py::init<std::size_t>(), py::arg("schedule_id"))
      .def("__str__", &StepMicrobatchOutputs::ToString)
      .def("__repr__", &StepMicrobatchOutputs::ToString)
      .def_readonly("schedule_id", &StepMicrobatchOutputs::schedule_id);
}
//==============================================================================
void InitStepOutputsPybindClass(py::module_& m) {
  py::class_<StepOutputs, std::shared_ptr<StepOutputs>>(m, "StepOutputs")
      .def(py::init<std::size_t, SamplerOutputs>(), py::arg("schedule_id"),
           py::arg("sampler_outputs"))
      .def("__str__", &StepOutputs::ToString)
      .def("__repr__", &StepOutputs::ToString)
      .def_readonly("schedule_id", &StepOutputs::schedule_id)
      .def_readonly("sampler_outputs", &StepOutputs::sampler_outputs);
}
//==============================================================================
void InitPendingStepOutputPybindClass(py::module_& m) {
  py::class_<PendingStepOutput, std::shared_ptr<PendingStepOutput>>(
      m, "PendingStepOutput")
      .def(py::init<SchedulerOutputPtr, ValidSamplerOutputs>(),
           py::arg("scheduler_output"), py::arg("sampler_outputs"))
      .def("__str__", &PendingStepOutput::ToString)
      .def("__repr__", &PendingStepOutput::ToString)
      .def_readonly("scheduler_output", &PendingStepOutput::scheduler_output)
      .def_readonly("sampler_outputs", &PendingStepOutput::sampler_outputs);
}
//==============================================================================
void InitDatatypesPybindSubmodule(py::module_& pm) {
  auto m = pm.def_submodule("datatypes", "Datatypes submodule");

  // Call individual binding functions
  InitCommInfoPybindClass(m);
  InitSequenceMetadataPybindClass(m);
  InitLogicalTokenBlockPybindClass(m);
  InitSamplerOutputPybindClass(m);
  InitSequenceStatusPybindEnum(m);
  InitSamplingTypePybindEnum(m);
  InitSamplingParamsPybindClass(m);
  InitSequenceStatePybindClass(m);
  InitSequenceParamsPybindClass(m);
  InitSequencePybindClass(m);
  InitSequenceScheduleMetadataPybindClass(m);
  InitSchedulerOutputPybindClass(m);
  InitRequestOutputPybindClass(m);
  InitUserSequenceParamsPybindClass(m);
  InitBaseSequenceWithPriorityPybindClass(m);
  InitStepInputsPybindClass(m);
  InitStepMicrobatchOutputsPybindClass(m);
  InitStepOutputsPybindClass(m);
  InitPendingStepOutputPybindClass(m);
}
//==============================================================================
}  // namespace vajra
//==============================================================================
