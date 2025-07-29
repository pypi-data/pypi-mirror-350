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
#include "commons/StdCommon.h"
#include "native/enums/Enums.h"
//==============================================================================
namespace vajra {
//==============================================================================
struct BaseReplicaSchedulerConfig {
  explicit BaseReplicaSchedulerConfig(std::size_t max_batch_size_param = 128)
      : max_batch_size(max_batch_size_param) {}

  virtual ~BaseReplicaSchedulerConfig() = default;

  virtual std::size_t GetMaxBatchSize() const { return max_batch_size; }
  virtual std::size_t GetMaxChunkSize() const = 0;
  virtual std::size_t GetMinChunkSize() const = 0;
  virtual float GetTargetBatchTime() const = 0;

  virtual ReplicaSchedulerType GetType() const = 0;

  /// @brief Convert to string representation
  /// @return String representation of the BaseReplicaSchedulerConfig
  [[nodiscard]] virtual std::string ToString() const {
    return std::format(
        "BaseReplicaSchedulerConfig(type={}, max_batch_size={}, "
        "max_chunk_size={}, min_chunk_size={}, target_batch_time={})",
        GetType(), GetMaxBatchSize(), GetMaxChunkSize(), GetMinChunkSize(),
        GetTargetBatchTime());
  }

 private:
  const std::size_t max_batch_size;
};
//==============================================================================
struct FixedChunkReplicaSchedulerConfig final
    : public BaseReplicaSchedulerConfig {
  FixedChunkReplicaSchedulerConfig(std::size_t max_batch_size_param = 128,
                                   std::size_t chunk_size_param = 2048)
      : BaseReplicaSchedulerConfig(max_batch_size_param),
        chunk_size(chunk_size_param) {}

  std::size_t GetMaxChunkSize() const override { return chunk_size; }
  std::size_t GetMinChunkSize() const override { return chunk_size; }
  float GetTargetBatchTime() const override { return 0; }

  ReplicaSchedulerType GetType() const override {
    return ReplicaSchedulerType::FIXED_CHUNK;
  }

  /// @brief Convert to string representation
  /// @return String representation of the FixedChunkReplicaSchedulerConfig
  [[nodiscard]] std::string ToString() const override {
    return std::format("FixedChunkReplicaSchedulerConfig(chunk_size={})",
                       chunk_size);
  }

 private:
  const std::size_t chunk_size;
};

//==============================================================================
struct DynamicChunkReplicaSchedulerConfig : public BaseReplicaSchedulerConfig {
  DynamicChunkReplicaSchedulerConfig(std::size_t max_batch_size_param = 128,
                                     std::size_t max_chunk_size_param = 8192,
                                     std::size_t min_chunk_size_param = 32,
                                     float target_batch_time_param = 0.05)
      : BaseReplicaSchedulerConfig(max_batch_size_param),
        max_chunk_size(max_chunk_size_param),
        min_chunk_size(min_chunk_size_param),
        target_batch_time(target_batch_time_param) {}

  std::size_t GetMaxChunkSize() const override { return max_chunk_size; }
  std::size_t GetMinChunkSize() const override { return min_chunk_size; }
  float GetTargetBatchTime() const override { return target_batch_time; }

  ReplicaSchedulerType GetType() const override {
    return ReplicaSchedulerType::DYNAMIC_CHUNK;
  }

  /// @brief Convert to string representation
  /// @return String representation of the DynamicChunkReplicaSchedulerConfig
  [[nodiscard]] std::string ToString() const override {
    return std::format(
        "DynamicChunkReplicaSchedulerConfig(max_batch_size={}, "
        "max_chunk_size={}, min_chunk_size={}, target_batch_time={})",
        GetMaxBatchSize(), max_chunk_size, min_chunk_size, target_batch_time);
  }

 private:
  const std::size_t max_chunk_size;
  const std::size_t min_chunk_size;
  const float target_batch_time;
};

//==============================================================================
struct SpaceSharingReplicaSchedulerConfig final
    : public DynamicChunkReplicaSchedulerConfig {
  SpaceSharingReplicaSchedulerConfig(
      std::size_t max_batch_size_param = 128,
      std::size_t max_chunk_size_param = 8192,
      std::size_t min_chunk_size_param = 32,
      float target_batch_time_param = 0.05,
      std::size_t long_seq_kv_cache_len_threshold_param = 256 * 1024)
      : DynamicChunkReplicaSchedulerConfig(
            max_batch_size_param, max_chunk_size_param, min_chunk_size_param,
            target_batch_time_param),
        long_seq_kv_cache_len_threshold(long_seq_kv_cache_len_threshold_param) {
  }

  std::size_t GetLongSeqKvCacheLenThreshold() const {
    return long_seq_kv_cache_len_threshold;
  }

  ReplicaSchedulerType GetType() const override {
    return ReplicaSchedulerType::SPACE_SHARING;
  }

  /// @brief Convert to string representation
  /// @return String representation of the SpaceSharingReplicaSchedulerConfig
  [[nodiscard]] std::string ToString() const override {
    return std::format(
        "SpaceSharingReplicaSchedulerConfig(max_batch_size={}, "
        "max_chunk_size={}, min_chunk_size={}, target_batch_time={}, "
        "long_seq_kv_cache_len_threshold={})",
        GetMaxBatchSize(), GetMaxChunkSize(), GetMinChunkSize(),
        GetTargetBatchTime(), long_seq_kv_cache_len_threshold);
  }

 private:
  const std::size_t long_seq_kv_cache_len_threshold;
};
//==============================================================================
}  // namespace vajra
//==============================================================================
