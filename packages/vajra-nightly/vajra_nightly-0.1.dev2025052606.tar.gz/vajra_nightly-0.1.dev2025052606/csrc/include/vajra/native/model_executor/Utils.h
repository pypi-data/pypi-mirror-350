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
//==============================================================================
namespace vajra {
//==============================================================================
template <typename T>
[[nodiscard]] std::vector<T> PadToAlignment(
    const std::vector<T>& input /*[in]*/, std::size_t multiple_of /*[in]*/,
    T value /*[in]*/) {
  std::size_t padding =
      (multiple_of - (input.size() % multiple_of)) % multiple_of;
  std::vector<T> output(input);
  output.insert(output.end(), padding, value);
  return output;
}
//==============================================================================
[[nodiscard]] inline std::size_t RoundUpToMultiple(
    std::size_t value /*[in]*/, std::size_t multiple_of /*[in]*/) {
  return ((value + multiple_of - 1) / multiple_of) * multiple_of;
}
//==============================================================================
}  // namespace vajra
//==============================================================================
