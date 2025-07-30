//==============================================================================
// Copyright 2023-2025 Codeium, Inc. All Rights Reserved.
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
#include "native/metrics_store/datastores/LabeledCdfDataStore.h"

#include "commons/StdCommon.h"
//==============================================================================
namespace vajra {
//==============================================================================
LabeledCdfDataStore::LabeledCdfDataStore()
    : data_log_(std::make_shared<std::vector<std::pair<std::string, float>>>()),
      is_dirty_(false) {}
//==============================================================================
LabeledCdfDataStore::LabeledCdfDataStore(
    const std::vector<std::pair<std::string, float>>& data)
    : data_log_(
          std::make_shared<std::vector<std::pair<std::string, float>>>(data)),
      is_dirty_(true) {
  // Deduplicate and normalize the data
  DedupeAndNormalize();
}
//==============================================================================
void LabeledCdfDataStore::Put(const std::string& label, float value) {
  data_log_->emplace_back(label, value);
  is_dirty_ = true;
}
//==============================================================================
void LabeledCdfDataStore::Merge(const BaseCdfDataStore& other) {
  // Check that other is a LabeledCdfDataStore
  ASSERT_VALID_RUNTIME(typeid(other) == typeid(LabeledCdfDataStore),
                       "Cannot merge with a non-LabeledCdfDataStore");
  const auto& other_labeled = static_cast<const LabeledCdfDataStore&>(other);

  // Reserve space for the merged data
  data_log_->reserve(data_log_->size() + other_labeled.GetDataLog()->size());

  // Append the other data log
  data_log_->insert(data_log_->end(), other_labeled.GetDataLog()->begin(),
                    other_labeled.GetDataLog()->end());

  is_dirty_ = true;
}
//==============================================================================
std::size_t LabeledCdfDataStore::Size() const { return data_log_->size(); }
//==============================================================================
float LabeledCdfDataStore::Sum() const {
  if (is_dirty_) {
    LOG_WARNING("Data log is dirty and needs deduplication");
  }

  return std::accumulate(
      data_log_->begin(), data_log_->end(), 0.0f,
      [](float sum, const auto& pair) { return sum + pair.second; });
}
//==============================================================================
std::shared_ptr<const std::vector<std::pair<std::string, float>>>
LabeledCdfDataStore::GetDataLog() const {
  return std::static_pointer_cast<
      const std::vector<std::pair<std::string, float>>>(data_log_);
}
//==============================================================================
std::vector<std::pair<std::string, float>> LabeledCdfDataStore::GetDataLogCopy()
    const {
  return *data_log_;
}
//==============================================================================
void LabeledCdfDataStore::DedupeAndNormalize() {
  if (!is_dirty_) {
    return;
  }

  // Convert to map to deduplicate and compute averages
  std::unordered_map<std::string, std::vector<float>> data_map;
  for (const auto& [label, value] : *data_log_) {
    data_map[label].push_back(value);
  }

  // Create a new vector for the deduplicated and normalized data
  std::vector<std::pair<std::string, float>> new_data;
  new_data.reserve(data_map.size());

  // Compute average for each label
  for (const auto& [label, values] : data_map) {
    float sum = std::accumulate(values.begin(), values.end(), 0.0f);
    float avg = sum / static_cast<float>(values.size());
    new_data.emplace_back(label, avg);
  }

  // Sort by label
  std::sort(new_data.begin(), new_data.end(),
            [](const auto& a, const auto& b) { return a.first < b.first; });

  // Replace the data log with the new data
  *data_log_ = std::move(new_data);

  is_dirty_ = false;
}
//==============================================================================
void LabeledCdfDataStore::Reset() {
  data_log_->clear();
  is_dirty_ = false;
}
//==============================================================================
}  // namespace vajra
//==============================================================================
