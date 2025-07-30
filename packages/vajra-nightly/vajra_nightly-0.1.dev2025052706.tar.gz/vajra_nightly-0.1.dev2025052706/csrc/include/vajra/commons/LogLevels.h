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
enum class LogLevel {
  DEBUG = 0,
  INFO = 1,
  WARNING = 2,
  ERROR = 3,
  CRITICAL = 4
};
//==============================================================================
}  // namespace vajra
//==============================================================================
template <>
struct std::formatter<vajra::LogLevel> : std::formatter<std::string_view> {
  template <typename FormatContext>
  auto format(vajra::LogLevel level, FormatContext& ctx) const {
    std::string_view name = "UNKNOWN";
    switch (level) {
      case vajra::LogLevel::DEBUG:
        name = "DEBUG";
        break;
      case vajra::LogLevel::INFO:
        name = "INFO";
        break;
      case vajra::LogLevel::WARNING:
        name = "WARNING";
        break;
      case vajra::LogLevel::ERROR:
        name = "ERROR";
        break;
      case vajra::LogLevel::CRITICAL:
        name = "CRITICAL";
        break;
    }
    return std::formatter<std::string_view>::format(name, ctx);
  }
};
//==============================================================================
