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
#pragma once
//==============================================================================
#include "commons/Logging.h"
#include "commons/StringUtils.h"
#include "native/datatypes/SequenceScheduleMetadata.h"
//==============================================================================
namespace vajra {
//==============================================================================
struct SchedulerOutput {
  SchedulerOutput(const std::size_t id_param,
                  const std::vector<std::string> ignored_seq_ids_param,
                  const std::vector<std::string> preempted_seq_ids_param,
                  const std::vector<SequenceScheduleMetadataPtr>
                      seq_schedule_metadata_list_param)
      : id(id_param),
        ignored_seq_ids(ignored_seq_ids_param),
        preempted_seq_ids(preempted_seq_ids_param),
        seq_schedule_metadata_list(seq_schedule_metadata_list_param),
        is_empty(seq_schedule_metadata_list.size() == 0),
        has_no_output((seq_schedule_metadata_list.size() == 0) &&
                      (ignored_seq_ids.size() == 0) &&
                      (preempted_seq_ids.size() == 0)) {}

  std::string ToString() const {
    return std::format(
        "SchedulerOutput(id={}, ignored_seq_ids={}, preempted_seq_ids={}, "
        "seq_schedule_metadata_list_size={}, is_empty={}, has_no_output={})",
        id, JoinStrings(ignored_seq_ids, ", "),
        JoinStrings(preempted_seq_ids, ", "), seq_schedule_metadata_list.size(),
        is_empty, has_no_output);
  }

  const std::size_t id;
  const std::vector<std::string> ignored_seq_ids;
  const std::vector<std::string> preempted_seq_ids;
  const std::vector<SequenceScheduleMetadataPtr> seq_schedule_metadata_list;
  const bool is_empty;
  const bool has_no_output;
};
//==============================================================================
using SchedulerOutputPtr = std::shared_ptr<const SchedulerOutput>;
//==============================================================================
}  // namespace vajra
//==============================================================================
