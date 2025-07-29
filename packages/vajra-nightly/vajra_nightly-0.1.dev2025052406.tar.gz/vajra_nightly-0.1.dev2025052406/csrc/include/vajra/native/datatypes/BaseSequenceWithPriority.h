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
#include "commons/Constants.h"
#include "commons/StdCommon.h"
#include "native/datatypes/Sequence.h"
//==============================================================================
namespace vajra {
//==============================================================================
class BaseSequenceWithPriority {
 public:
  /// @brief Constructor with priority function
  /// @param[in] seq Shared pointer to a Sequence object
  explicit BaseSequenceWithPriority(MutableSequencePtr seq) : seq_(seq) {
    ASSERT_VALID_POINTER_ARGUMENT(seq);
  }

  virtual ~BaseSequenceWithPriority() = default;

  /// @brief Get the priority of the sequence
  /// @return Priority of the sequence
  [[nodiscard]] virtual float GetPriority() const = 0;

  /// @brief Compares two BaseSequenceWithPriority objects based on their
  /// priorities.
  /// @param[in] other BaseSequenceWithPriority object to compare with.
  /// @return true if priority_ is less than other's priority, false otherwise.
  [[nodiscard]] bool operator<(const BaseSequenceWithPriority& other) const {
    return GetPriority() < other.GetPriority();
  }

  [[nodiscard]] bool operator>(const BaseSequenceWithPriority& other) const {
    return GetPriority() > other.GetPriority();
  }

  [[nodiscard]] bool operator==(const BaseSequenceWithPriority& other) const {
    return GetPriority() == other.GetPriority();
  }

  [[nodiscard]] bool operator!=(const BaseSequenceWithPriority& other) const {
    return GetPriority() != other.GetPriority();
  }

  /// @brief Get the sequence object
  /// @return Shared pointer to the Sequence object
  [[nodiscard]] MutableSequencePtr GetSequence() const { return seq_; }

  /// @brief Convert to string representation
  /// @return String representation of the BaseSequenceWithPriority
  [[nodiscard]] std::string ToString() const {
    return std::format("BaseSequenceWithPriority(priority={}, seq_id={})",
                       GetPriority(), seq_->seq_id);
  }

 private:
  MutableSequencePtr seq_;
};
//==============================================================================
using BaseSequenceWithPriorityPtr =
    std::shared_ptr<const BaseSequenceWithPriority>;
using BaseSequenceWithPriorityPtrList =
    std::vector<BaseSequenceWithPriorityPtr>;
using MutableBaseSequenceWithPriorityPtr =
    std::shared_ptr<BaseSequenceWithPriority>;
using MutableBaseSequenceWithPriorityPtrList =
    std::vector<MutableBaseSequenceWithPriorityPtr>;

/// @brief Comparator struct for shared pointers to BaseSequenceWithPriority
/// Important note on priority semantics:
/// - Lower numerical priority values mean higher actual priority
struct BaseSequenceWithPriorityComparator {
  bool operator()(const MutableBaseSequenceWithPriorityPtr& a,
                  const MutableBaseSequenceWithPriorityPtr& b) const {
    // Compare priorities - lower numerical values come first
    if (a->GetPriority() != b->GetPriority()) {
      return a->GetPriority() < b->GetPriority();
    }
    // Tie-breaker using sequence ID for deterministic ordering
    return a->GetSequence()->seq_id < b->GetSequence()->seq_id;
  }
};
//==============================================================================
}  // namespace vajra
//==============================================================================
