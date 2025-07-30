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
#include "commons/StdCommon.h"
#include "ddsketch.h"  // NOLINT
#include "native/metrics_store/datastores/BaseCdfDataStore.h"
//==============================================================================
namespace vajra {
//==============================================================================
class UnlabeledCdfDataStore : public BaseCdfDataStore {
 public:
  // Default constructor with default relative accuracy
  explicit UnlabeledCdfDataStore(double relative_accuracy = 0.001);

  // Constructor with a pre-created DDSketch
  explicit UnlabeledCdfDataStore(const ddsketch::DDSketch& sketch);

  // Add a value to the sketch
  void Put(float value);

  // Override the base class Put method to adapt for a different signature
  void Put([[maybe_unused]] const std::string& label, float value) override {
    // Ignore the label and just use the value
    Put(value);
  }
  // Merge another datastore into this one
  void Merge(const BaseCdfDataStore& other) override;

  // Get the number of values in the sketch
  std::size_t Size() const override;

  // Get the sum of all values in the sketch
  float Sum() const override;

  // Get a quantile value from the sketch
  float GetQuantileValue(float quantile) const;

  // Get the minimum value
  float Min() const;

  // Get the maximum value
  float Max() const;

  // Get the count of values
  std::size_t Count() const;

  // Get the relative accuracy
  float RelativeAccuracy() const;

  // Get serialized data as a string
  std::string GetSerializedState() const;

  // Create from serialized string
  static std::shared_ptr<UnlabeledCdfDataStore> FromSerializedString(
      const std::string& serialized);

  // Reset the datastore to its initial empty state
  void Reset() override;

 private:
  // The DDSketch instance
  ddsketch::DDSketch sketch_;
};
//==============================================================================
}  // namespace vajra
//==============================================================================
