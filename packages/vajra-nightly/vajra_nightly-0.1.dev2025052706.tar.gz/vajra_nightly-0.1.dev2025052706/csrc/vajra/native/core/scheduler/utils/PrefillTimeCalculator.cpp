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
#include "native/core/scheduler/utils/PrefillTimeCalculator.h"
//==============================================================================
#include "commons/Logging.h"
#include "commons/StdCommon.h"
#include "native/utils/HashUtils.h"
#include "native/utils/NumericalUtils.h"
//==============================================================================
namespace vajra {
//==============================================================================
constexpr std::size_t PREFILL_TIME_CALCULATOR_CACHE_KEY_LENGTH = 10;
//==============================================================================
PrefillTimeCalculator::PrefillTimeCalculator(
    std::shared_ptr<ExecutionTimePredictor> execution_time_predictor,
    std::size_t pipeline_parallel_size, std::size_t kv_parallel_size,
    std::size_t max_num_tokens_per_kvp_group, float target_batch_time,
    std::size_t max_chunk_size, std::size_t min_chunk_size,
    bool enable_sequence_pipeline_parallelism)
    : execution_time_predictor_(execution_time_predictor),
      pipeline_parallel_size_(pipeline_parallel_size),
      kv_parallel_size_(kv_parallel_size),
      max_num_tokens_per_kvp_group_(max_num_tokens_per_kvp_group),
      target_batch_time_(target_batch_time),
      max_prefill_length_(PREFILL_TIME_PREDICTION_CACHE_MAX_TOKENS),
      max_chunk_size_(max_chunk_size),
      min_chunk_size_(min_chunk_size),
      enable_sequence_pipeline_parallelism_(
          enable_sequence_pipeline_parallelism) {
  ASSERT_VALID_POINTER_ARGUMENT(execution_time_predictor);

  // Initialize cache for different prompt lengths
  std::string cache_file_path =
      std::format("{}/prefill_time_cache_{}.bin",
                  execution_time_predictor_->GetCacheDir(), GetHash());

  if (std::filesystem::exists(cache_file_path)) {
    LoadPrefillTimeCache(cache_file_path);
  } else {
    InitializePrefillTimeCache();
    StorePrefillTimeCache(cache_file_path);
  }
}
//==============================================================================
void PrefillTimeCalculator::LoadPrefillTimeCache(std::string cache_file_path) {
  std::ifstream cache_file(cache_file_path, std::ios::binary);

  if (!cache_file.is_open()) {
    ASSERT_VALID_RUNTIME(false, "Failed to open cache file");
    return;
  }

  // Read the cache from the file (implementation depends on the serialization
  // format)
  std::size_t key;
  float value;
  while (cache_file.read(reinterpret_cast<char*>(&key), sizeof(std::size_t)) &&
         cache_file.read(reinterpret_cast<char*>(&value), sizeof(float))) {
    prefill_time_cache_[key] = value;
  }

  cache_file.close();
}
//==============================================================================
void PrefillTimeCalculator::StorePrefillTimeCache(
    std::string cache_file_path) const {
  std::ofstream cache_file(cache_file_path, std::ios::binary);

  if (!cache_file.is_open()) {
    ASSERT_VALID_RUNTIME(false, "Failed to open cache file");
    return;
  }

  // Write the cache to the file
  for (const auto& pair : prefill_time_cache_) {
    cache_file.write(reinterpret_cast<const char*>(&pair.first),
                     sizeof(std::size_t));
    cache_file.write(reinterpret_cast<const char*>(&pair.second),
                     sizeof(float));
  }

  cache_file.close();
}
//==============================================================================
std::pair<std::size_t, float> PrefillTimeCalculator::GetOptimalChunkSize(
    std::size_t remaining_tokens, std::size_t num_kvp_groups,
    std::size_t num_kv_tokens) const {
  if (min_chunk_size_ == max_chunk_size_) {
    auto chunk_size = std::min(remaining_tokens, max_chunk_size_);

    // Create batch for execution time prediction
    std::vector<std::size_t> num_q_tokens = {chunk_size};
    std::vector<std::size_t> num_kv_tokens_vec = {num_kv_tokens};
    std::vector<std::size_t> num_active_kvp_groups = {num_kvp_groups};

    vidur::entities::Batch batch(
        0,                      // replica_id
        1,                      // num seqs
        num_q_tokens,           // num q tokens
        num_kv_tokens_vec,      // num kv tokens
        num_active_kvp_groups,  // num active kvp groups
        0                       // kvp group id
    );

    auto execution_time_result =
        execution_time_predictor_->GetExecutionTimeBatch(batch, 0);
    float execution_time = static_cast<float>(
        execution_time_result.GetTotalTime() * pipeline_parallel_size_);

    return {chunk_size, execution_time};
  }
  // Binary search for optimal chunk size
  std::size_t high = std::min(2 * EXECUTION_TIME_PREDICTION_START_CHUNK_SIZE,
                              remaining_tokens);
  std::size_t low = 0;
  std::size_t closest_match = 0;
  float closest_time = -1.0f;
  std::unordered_set<std::size_t> seen_chunk_sizes;

  while (low <= high) {
    std::size_t mid = (low + high) / 2;

    mid = std::min(max_chunk_size_, mid);

    if (mid < remaining_tokens) {
      mid = RoundDownToNearestMultiple(
          mid, EXECUTION_TIME_PREDICTION_CHUNK_SIZE_GRANULARITY);
      if (mid == 0) {
        mid = std::min(min_chunk_size_, remaining_tokens);
      }
    } else {
      mid = remaining_tokens;
    }

    if (seen_chunk_sizes.find(mid) != seen_chunk_sizes.end() || mid == 0) {
      break;
    }

    seen_chunk_sizes.insert(mid);

    // Create batch for execution time prediction
    std::vector<std::size_t> num_q_tokens = {mid};
    std::vector<std::size_t> num_kv_tokens_vec = {num_kv_tokens};
    std::vector<std::size_t> num_active_kvp_groups = {num_kvp_groups};

    vidur::entities::Batch batch(
        0,                      // replica_id
        1,                      // num seqs
        num_q_tokens,           // num q tokens
        num_kv_tokens_vec,      // num kv tokens
        num_active_kvp_groups,  // num active kvp groups
        0                       // kvp group id
    );

    auto execution_time_result =
        execution_time_predictor_->GetExecutionTimeBatch(batch, 0);
    float execution_time = static_cast<float>(
        execution_time_result.GetTotalTime() * pipeline_parallel_size_);

    // Check if execution time is within slack range
    if (execution_time >=
            target_batch_time_ * (1 - EXECUTION_TIME_PREDICTION_SLACK) &&
        execution_time <=
            target_batch_time_ * (1 + EXECUTION_TIME_PREDICTION_SLACK)) {
      closest_match = mid;
      closest_time = execution_time;
      break;
    } else if (execution_time <
               target_batch_time_ * (1 - EXECUTION_TIME_PREDICTION_SLACK)) {
      low = mid;
    } else {
      high = mid;
    }

    // Keep track of closest match
    if (closest_time < 0 || std::abs(execution_time - target_batch_time_) <
                                std::abs(closest_time - target_batch_time_)) {
      closest_match = mid;
      closest_time = execution_time;
    }
  }

  return {closest_match, closest_time};
}
//==============================================================================
float PrefillTimeCalculator::CalculateTotalPrefillTime(
    std::size_t num_prefill_tokens) const {
  float total_time = 0.0f;
  std::size_t current_tokens = 0;

  ASSERT_VALID_RUNTIME(max_num_tokens_per_kvp_group_ > 0,
                       "Invalid max_num_tokens_per_kvp_group");

  // Process tokens in chunks until all prefill is complete
  while (current_tokens < num_prefill_tokens) {
    std::size_t num_kvp_groups =
        (current_tokens / max_num_tokens_per_kvp_group_) + 1;
    std::size_t num_kv_tokens;
    if (num_kvp_groups > 1) {
      num_kv_tokens = max_num_tokens_per_kvp_group_;
    } else {
      num_kv_tokens = current_tokens;
    }

    std::size_t remaining = num_prefill_tokens - current_tokens;

    // Find optimal chunk size for target batch time
    auto [chunk_size, execution_time] = GetOptimalChunkSize(
        std::min(remaining, max_chunk_size_), num_kvp_groups, num_kv_tokens);

    if (chunk_size == 0) {
      break;
    }

    total_time += execution_time;
    current_tokens += chunk_size;
  }

  LOG_INFO("Prefill time for {} tokens: {}", num_prefill_tokens, total_time);

  return total_time;
}
//==============================================================================
void PrefillTimeCalculator::InitializePrefillTimeCache() {
  prefill_time_cache_[0] = 0.0f;

  for (std::size_t num_tokens = PREFILL_TIME_PREDICTION_CACHE_GRANULARITY;
       num_tokens <= max_prefill_length_;
       num_tokens += PREFILL_TIME_PREDICTION_CACHE_GRANULARITY) {
    prefill_time_cache_[num_tokens] = CalculateTotalPrefillTime(num_tokens);
  }
}
//==============================================================================
float PrefillTimeCalculator::GetPrefillTime(
    std::size_t num_prefill_tokens, std::size_t num_processed_tokens) const {
  std::size_t remaining_tokens = num_prefill_tokens - num_processed_tokens;
  ASSERT_VALID_RUNTIME(remaining_tokens > 0, "No tokens to prefill");

  // Get nearest cached sizes
  std::size_t total_cached_size = RoundUpToNearestMultiple(
      num_prefill_tokens, PREFILL_TIME_PREDICTION_CACHE_GRANULARITY);
  std::size_t processed_cached_size = RoundUpToNearestMultiple(
      num_processed_tokens, PREFILL_TIME_PREDICTION_CACHE_GRANULARITY);

  // Get base time from cache difference
  float total_time = prefill_time_cache_.at(total_cached_size) -
                     prefill_time_cache_.at(processed_cached_size);

  if (enable_sequence_pipeline_parallelism_) {
    total_time = total_time / pipeline_parallel_size_;
  }

  return total_time;
}
//==============================================================================
std::string PrefillTimeCalculator::GetHash() const {
  // Create a string of attributes
  std::string cache_key =
      std::format("{}{}{}{}{}{}", pipeline_parallel_size_, kv_parallel_size_,
                  max_num_tokens_per_kvp_group_, max_prefill_length_,
                  target_batch_time_, execution_time_predictor_->GetHash());

  return vajra::GetHash(cache_key, PREFILL_TIME_CALCULATOR_CACHE_KEY_LENGTH);
}
}  // namespace vajra
//==============================================================================
