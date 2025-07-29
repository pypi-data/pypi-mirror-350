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
#include "vidur/execution_time_predictor/execution_time_predictor.h"
//==============================================================================
#include "commons/ClassTraits.h"
#include "commons/StdCommon.h"
#include "native/core/scheduler/replica_schedulers/trackers/BatchFormationTrackerWithRuntimePrediction.h"
//==============================================================================
namespace vajra {
//==============================================================================
constexpr std::size_t PREFILL_TIME_PREDICTION_CACHE_MAX_TOKENS =
    2 * 1024 * 1024;
constexpr std::size_t PREFILL_TIME_PREDICTION_CACHE_GRANULARITY = 256;
//==============================================================================
using ExecutionTimePredictor =
    vidur::execution_time_predictor::ExecutionTimePredictor;
//==============================================================================
class PrefillTimeCalculator : public NonCopyableNonMovable {
 public:
  PrefillTimeCalculator(
      std::shared_ptr<ExecutionTimePredictor> execution_time_predictor,
      std::size_t pipeline_parallel_size, std::size_t kv_parallel_size,
      std::size_t max_num_tokens_per_kvp_group, float target_batch_time,
      std::size_t max_chunk_size, std::size_t min_chunk_size,
      bool enable_sequence_pipeline_parallelism);

  [[nodiscard]] float GetPrefillTime(
      std::size_t num_prefill_tokens,
      std::size_t num_processed_tokens = 0) const;
  [[nodiscard]] std::string GetHash() const;

 private:
  void InitializePrefillTimeCache();
  void StorePrefillTimeCache(std::string cache_file_path) const;
  void LoadPrefillTimeCache(std::string cache_file_path);

  [[nodiscard]] std::pair<std::size_t, float> GetOptimalChunkSize(
      std::size_t remaining_tokens, std::size_t num_kvp_groups,
      std::size_t num_kv_tokens) const;

  [[nodiscard]] float CalculateTotalPrefillTime(
      std::size_t num_prefill_tokens) const;

  const std::shared_ptr<ExecutionTimePredictor> execution_time_predictor_;
  const std::size_t pipeline_parallel_size_;
  const std::size_t kv_parallel_size_;
  const std::size_t max_num_tokens_per_kvp_group_;
  const float target_batch_time_;
  const std::size_t max_prefill_length_;
  const std::size_t max_chunk_size_;
  const std::size_t min_chunk_size_;
  const bool enable_sequence_pipeline_parallelism_;
  std::unordered_map<std::size_t, float> prefill_time_cache_;
};
//==============================================================================
}  // namespace vajra
//==============================================================================
