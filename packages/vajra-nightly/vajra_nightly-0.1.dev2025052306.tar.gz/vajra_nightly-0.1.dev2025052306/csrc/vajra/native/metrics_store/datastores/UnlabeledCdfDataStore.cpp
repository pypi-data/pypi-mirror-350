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
#include "native/metrics_store/datastores/UnlabeledCdfDataStore.h"

#include "commons/StdCommon.h"
//==============================================================================
namespace vajra {
//==============================================================================
UnlabeledCdfDataStore::UnlabeledCdfDataStore(double relative_accuracy)
    : sketch_(relative_accuracy) {}
//==============================================================================
UnlabeledCdfDataStore::UnlabeledCdfDataStore(const ddsketch::DDSketch& sketch)
    : sketch_(sketch) {}
//==============================================================================
void UnlabeledCdfDataStore::Put(float value) {
  sketch_.add(static_cast<double>(value));
}
//==============================================================================
void UnlabeledCdfDataStore::Merge(const BaseCdfDataStore& other) {
  // Check that other is an UnlabeledCdfDataStore
  ASSERT_VALID_RUNTIME(typeid(other) == typeid(UnlabeledCdfDataStore),
                       "Cannot merge with a non-UnlabeledCdfDataStore");
  const auto& other_unlabeled =
      static_cast<const UnlabeledCdfDataStore&>(other);

  sketch_.merge(other_unlabeled.sketch_);
}
//==============================================================================
std::size_t UnlabeledCdfDataStore::Size() const {
  return static_cast<std::size_t>(sketch_.num_values());
}
//==============================================================================
float UnlabeledCdfDataStore::Sum() const {
  return static_cast<float>(sketch_.sum());
}
//==============================================================================
float UnlabeledCdfDataStore::GetQuantileValue(float quantile) const {
  return static_cast<float>(sketch_.get_quantile_value(quantile));
}
//==============================================================================
float UnlabeledCdfDataStore::Min() const {
  return static_cast<float>(sketch_.min());
}
//==============================================================================
float UnlabeledCdfDataStore::Max() const {
  return static_cast<float>(sketch_.max());
}
//==============================================================================
std::size_t UnlabeledCdfDataStore::Count() const {
  return static_cast<std::size_t>(sketch_.num_values());
}
//==============================================================================
float UnlabeledCdfDataStore::RelativeAccuracy() const {
  return static_cast<float>(sketch_.relative_accuracy());
}
//==============================================================================
std::string UnlabeledCdfDataStore::GetSerializedState() const {
  // Use the new string-based serialization method
  return sketch_.serialize();
}
//==============================================================================
std::shared_ptr<UnlabeledCdfDataStore>
UnlabeledCdfDataStore::FromSerializedString(const std::string& serialized) {
  // Create a sketch from the serialized string
  ddsketch::DDSketch reconstructed_sketch =
      ddsketch::DDSketch::deserialize(serialized);
  return std::make_shared<UnlabeledCdfDataStore>(reconstructed_sketch);
}
//==============================================================================
void UnlabeledCdfDataStore::Reset() {
  sketch_ = ddsketch::DDSketch(sketch_.relative_accuracy());
}
//==============================================================================
}  // namespace vajra
//==============================================================================
