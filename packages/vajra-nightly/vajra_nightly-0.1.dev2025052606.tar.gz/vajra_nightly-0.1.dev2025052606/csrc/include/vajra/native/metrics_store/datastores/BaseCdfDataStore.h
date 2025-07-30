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
//==============================================================================
namespace vajra {
//==============================================================================
class BaseCdfDataStore : public NonCopyableNonMovable {
 public:
  // Default constructor
  BaseCdfDataStore();

  // Virtual destructor for proper cleanup in derived classes
  virtual ~BaseCdfDataStore() = default;

  // Add a data point to the datastore (abstract)
  virtual void Put(const std::string& label, float value) = 0;

  // Merge another datastore into this one (abstract)
  virtual void Merge(const BaseCdfDataStore& other) = 0;

  // Get the number of data points in the datastore (abstract)
  virtual std::size_t Size() const = 0;

  // Get the sum of all values in the datastore (abstract)
  virtual float Sum() const = 0;

  virtual void Reset() = 0;
};
//==============================================================================
}  // namespace vajra
//==============================================================================
