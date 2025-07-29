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
template <typename Container>
std::string JoinStrings(const Container& container,
                        const std::string& delimiter) {
  std::ostringstream oss;
  auto it = std::begin(container);
  if (it != std::end(container)) {
    oss << *it++;
  }
  for (; it != std::end(container); ++it) {
    oss << delimiter << *it;
  }
  return oss.str();
}
//==============================================================================
}  // namespace vajra
//==============================================================================
