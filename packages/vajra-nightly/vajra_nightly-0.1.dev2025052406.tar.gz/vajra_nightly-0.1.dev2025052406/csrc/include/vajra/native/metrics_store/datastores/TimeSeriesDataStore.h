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
#include "commons/ClassTraits.h"
#include "commons/StdCommon.h"
#include "native/core/Types.h"
//==============================================================================
namespace vajra {
//==============================================================================
class TimeSeriesDataStore : public NonCopyableNonMovable {
 public:
  // Default constructor
  TimeSeriesDataStore();

  // Constructor with initial data
  explicit TimeSeriesDataStore(
      const std::vector<std::pair<TimeS, float>>& data);

  // Add a data point to the time series
  void Put(TimeS time, float value);

  // Merge another time series data store into this one
  void Merge(const TimeSeriesDataStore& other);

  // Get the start time of the time series
  std::optional<TimeS> GetStartTime() const;

  // Get the number of data points in the time series
  std::size_t Size() const;

  // Get the sum of all values in the time series
  float Sum() const;

  // Get the data log for serialization (as shared_ptr)
  std::shared_ptr<const std::vector<std::pair<TimeS, float>>> GetDataLog()
      const;

  // Get the data log as a copy for Python conversion
  std::vector<std::pair<TimeS, float>> GetDataLogCopy() const;

  // Reset the datastore to its initial empty state
  void Reset();

 private:
  // Data storage for the time series (time, value) pairs using a shared pointer
  std::shared_ptr<std::vector<std::pair<TimeS, float>>> data_log_;

  // Mutex to protect concurrent puts
  std::mutex data_log_mutex_;
};
//==============================================================================
}  // namespace vajra
//==============================================================================
