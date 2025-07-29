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
#include "commons/Logging.h"
//==============================================================================
namespace vajra {
//==============================================================================
void Logger::InitializeLogLevel() {
  const char* env_log_level = std::getenv("VAJRA_LOG_LEVEL");
  if (!env_log_level) {
    log_level = LogLevel::INFO;
    return;
  }

  std::string level_str = env_log_level;
  if (level_str == "DEBUG") {
    log_level = LogLevel::DEBUG;
  } else if (level_str == "INFO") {
    log_level = LogLevel::INFO;
  } else if (level_str == "WARNING") {
    log_level = LogLevel::WARNING;
  } else if (level_str == "ERROR") {
    log_level = LogLevel::ERROR;
  } else if (level_str == "CRITICAL") {
    log_level = LogLevel::CRITICAL;
  } else {
    log_level = LogLevel::INFO;
  }
}
//==============================================================================
}  // namespace vajra
//==============================================================================
