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
#pragma once
//==============================================================================
#include "commons/Logging.h"
#include "commons/StdCommon.h"
#include "native/metrics_store/datastores/BaseCdfDataStore.h"
//==============================================================================
namespace vajra {
//==============================================================================
class LabeledCdfDataStore : public BaseCdfDataStore {
 public:
  // Default constructor
  LabeledCdfDataStore();

  // Constructor with initial data
  explicit LabeledCdfDataStore(
      const std::vector<std::pair<std::string, float>>& data);

  // Add a data point to the datastore
  void Put(const std::string& label, float value) override;

  // Merge another datastore into this one
  void Merge(const BaseCdfDataStore& other) override;

  // Get the number of data points in the datastore
  std::size_t Size() const override;

  // Get the sum of all values in the datastore
  float Sum() const override;

  // Get the data log for serialization (as shared_ptr)
  std::shared_ptr<const std::vector<std::pair<std::string, float>>> GetDataLog()
      const;

  // Get the data log as a copy for Python conversion
  std::vector<std::pair<std::string, float>> GetDataLogCopy() const;

  // Reset the datastore to its initial empty state
  void Reset() override;

  // Helper method to deduplicate and normalize the data
  void DedupeAndNormalize();

 private:
  // Data storage for the (label, value) pairs using a shared pointer
  std::shared_ptr<std::vector<std::pair<std::string, float>>> data_log_;

  // Flag to indicate if the data needs to be deduplicated and normalized
  bool is_dirty_;
};
//==============================================================================
}  // namespace vajra
//==============================================================================
