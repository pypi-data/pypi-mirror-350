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
#include "native/metrics_store/ChromeTracer.h"

#include "commons/Time.h"
//==============================================================================
using vajra::ChromeTracer;
//==============================================================================
ChromeTracer::ChromeTracer(std::string output_dir)
    : output_dir_(std::move(output_dir)) {
  trace_ = nlohmann::json::array();
}
//==============================================================================
ChromeTracer::ChromeTracer(std::string output_dir,
                           const std::string& serialized_trace)
    : output_dir_(std::move(output_dir)) {
  try {
    trace_ = nlohmann::json::parse(serialized_trace);
  } catch (const nlohmann::json::exception& e) {
    ASSERT_VALID_RUNTIME(false, "Failed to parse serialized trace: {}",
                         e.what());
  }
}
//==============================================================================
void ChromeTracer::Put(const SequenceMetadataVector& seq_metadata_list,
                       ReplicaId replica_id, std::size_t tensor_parallel_rank,
                       std::size_t pipeline_parallel_rank,
                       std::size_t kv_parallel_rank, double start_time,
                       double end_time) {
  if (tensor_parallel_rank != 0 || seq_metadata_list.empty()) {
    return;
  }

  std::vector<std::string> seq_ids;
  std::vector<std::size_t> num_q_tokens;
  std::vector<std::size_t> num_kv_tokens;
  for (const auto& metadata : seq_metadata_list) {
    seq_ids.push_back(metadata->seq_id);
    num_q_tokens.push_back(metadata->num_q_tokens);
    num_kv_tokens.push_back(metadata->num_kv_tokens);
  }

  nlohmann::json event;
  event["name"] = std::format("{}", JoinStrings(seq_ids, ", "));
  event["ph"] = "X";
  event["ts"] = start_time * 1e6;
  event["dur"] = (end_time - start_time) * 1e6;
  event["pid"] = std::format("Replica {}-kvp{}", replica_id, kv_parallel_rank);
  event["tid"] = pipeline_parallel_rank;

  nlohmann::json args;
  args["batch_size"] = seq_metadata_list.size();
  args["request_ids"] = seq_ids;
  args["num_q_tokens"] = num_q_tokens;
  args["num_kv_tokens"] = num_kv_tokens;
  event["args"] = args;

  trace_.push_back(event);
}
//==============================================================================
void ChromeTracer::PutSchedulerEvent(
    ReplicaId replica_id, std::size_t scheduler_id,
    const SequenceScheduleMetadataPtrList& seq_schedule_metadata_list,
    double start_time, double end_time) {
  if (seq_schedule_metadata_list.empty()) {
    return;
  }

  std::vector<std::string> seq_ids;
  std::vector<std::size_t> num_q_tokens;

  for (const auto& metadata_ptr : seq_schedule_metadata_list) {
    ASSERT_VALID_POINTER_ARGUMENT(metadata_ptr);

    seq_ids.push_back(metadata_ptr->seq_id);
    num_q_tokens.push_back(metadata_ptr->num_q_tokens);
  }

  nlohmann::json event;
  event["name"] = std::format("{}", JoinStrings(seq_ids, ", "));
  event["ph"] = "X";
  event["ts"] = start_time * 1e6;
  event["dur"] = (end_time - start_time) * 1e6;
  event["pid"] = std::format("Replica {}", replica_id);
  event["tid"] = "Scheduler";

  nlohmann::json args;
  args["scheduler_id"] = scheduler_id;
  args["batch_size"] = seq_schedule_metadata_list.size();
  args["request_ids"] = seq_ids;
  args["num_q_tokens"] = num_q_tokens;
  event["args"] = args;

  trace_.push_back(event);
}
//==============================================================================
void ChromeTracer::Merge(const ChromeTracer& other) {
  for (const auto& event : other.trace_) {
    trace_.push_back(event);
  }
}
//==============================================================================
void ChromeTracer::Store() {
  std::string file_path = output_dir_ + "/chrome_trace.json";
  std::ofstream output_file(file_path);
  ASSERT_VALID_RUNTIME(output_file.is_open(),
                       "Failed to open file for writing: {}", file_path);
  output_file << trace_.dump();
  output_file.close();
}
//==============================================================================
void ChromeTracer::Reset() { trace_.clear(); }
//==============================================================================
std::string ChromeTracer::GetState() const { return trace_.dump(); }
//==============================================================================
std::string ChromeTracer::GetOutputDir() const { return output_dir_; }
//==============================================================================
