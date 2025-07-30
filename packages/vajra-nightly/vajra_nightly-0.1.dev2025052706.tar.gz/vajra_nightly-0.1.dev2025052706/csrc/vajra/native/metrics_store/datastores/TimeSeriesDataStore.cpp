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
#include "native/metrics_store/datastores/TimeSeriesDataStore.h"

#include "commons/StdCommon.h"
#include "native/core/Types.h"
//==============================================================================
namespace vajra {
//==============================================================================
TimeSeriesDataStore::TimeSeriesDataStore()
    : data_log_(std::make_shared<std::vector<std::pair<TimeS, float>>>()),
      data_log_mutex_(std::mutex()) {}
//==============================================================================
TimeSeriesDataStore::TimeSeriesDataStore(
    const std::vector<std::pair<TimeS, float>>& data)
    : data_log_(std::make_shared<std::vector<std::pair<TimeS, float>>>(data)),
      data_log_mutex_(std::mutex()) {
  // Sort data by time if needed
  if (!data_log_->empty()) {
    std::sort(data_log_->begin(), data_log_->end(),
              [](const auto& a, const auto& b) { return a.first < b.first; });
  }
}
//==============================================================================
void TimeSeriesDataStore::Put(TimeS time, float value) {
  std::lock_guard<std::mutex> lock(data_log_mutex_);
  data_log_->emplace_back(time, value);
}
//==============================================================================
void TimeSeriesDataStore::Merge(const TimeSeriesDataStore& other) {
  if (other.data_log_->empty()) {
    return;
  }

  // Reserve space for the merged data
  data_log_->reserve(data_log_->size() + other.data_log_->size());

  // Append the other data log
  data_log_->insert(data_log_->end(), other.data_log_->begin(),
                    other.data_log_->end());

  // Sort data by time
  std::sort(data_log_->begin(), data_log_->end(),
            [](const auto& a, const auto& b) { return a.first < b.first; });
}
//==============================================================================
std::optional<TimeS> TimeSeriesDataStore::GetStartTime() const {
  if (data_log_->empty()) {
    return std::nullopt;
  }

  // Find the minimum time value
  auto min_element = std::min_element(
      data_log_->begin(), data_log_->end(),
      [](const auto& a, const auto& b) { return a.first < b.first; });

  return min_element->first;
}
//==============================================================================
std::size_t TimeSeriesDataStore::Size() const { return data_log_->size(); }
//==============================================================================
float TimeSeriesDataStore::Sum() const {
  float sum = 0.0f;
  for (const auto& [_, value] : *data_log_) {
    sum += value;
  }
  return sum;
}
//==============================================================================
std::shared_ptr<const std::vector<std::pair<TimeS, float>>>
TimeSeriesDataStore::GetDataLog() const {
  return std::static_pointer_cast<const std::vector<std::pair<TimeS, float>>>(
      data_log_);
}
//==============================================================================
std::vector<std::pair<TimeS, float>> TimeSeriesDataStore::GetDataLogCopy()
    const {
  return *data_log_;
}
//==============================================================================
void TimeSeriesDataStore::Reset() { data_log_->clear(); }
//==============================================================================
}  // namespace vajra
//==============================================================================
