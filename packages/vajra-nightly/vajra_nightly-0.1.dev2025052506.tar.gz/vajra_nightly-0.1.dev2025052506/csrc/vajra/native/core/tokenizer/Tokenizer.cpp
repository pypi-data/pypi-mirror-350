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
#include "native/core/tokenizer/Tokenizer.h"

#include "commons/Logging.h"
#include "commons/StdCommon.h"

namespace vajra {
Tokenizer Tokenizer::FromPath(const std::string& path) {
  std::ifstream file(path);
  ASSERT_VALID_RUNTIME(file.is_open(), "Unable to open file {}", path);

  std::stringstream buffer;
  buffer << file.rdbuf();
  std::string json_blob = buffer.str();

  file.close();

  try {
    return Tokenizer(tokenizers::Tokenizer::FromBlobJSON(json_blob));
  } catch (const std::exception& e) {
    ASSERT_VALID_RUNTIME(false,
                         "Failed to create a tokenizer from {}. Exception: {}",
                         path, e.what());
  }
}

std::vector<std::int32_t> Tokenizer::Encode(const std::string& text) const {
  return tokenizer_->Encode(text);
}

std::string Tokenizer::Decode(const std::vector<std::int32_t>& token_ids) {
  if (token_ids.size() == 0) return "";  // panics otherwise
  return tokenizer_->Decode(token_ids);
}

std::tuple<std::string, std::size_t, std::size_t> Tokenizer::PartialDecode(
    const std::vector<std::int32_t>& token_ids, std::size_t prefix_offset,
    std::size_t read_offset) {
  if (token_ids.size() == 0) {
    return std::make_tuple("", prefix_offset, read_offset);
  }

  ASSERT_VALID_RUNTIME(
      prefix_offset < token_ids.size(),
      "prefix_offset (= {}) is out of bounds. Number of tokens={}",
      prefix_offset, token_ids.size());
  ASSERT_VALID_RUNTIME(
      read_offset <= token_ids.size(),
      "read_offset (= {}) is out of bounds. Number of tokens={}", read_offset,
      token_ids.size());
  ASSERT_VALID_RUNTIME(read_offset >= prefix_offset,
                       "read_offset (= {}) must be >= prefix_offset (= {})",
                       prefix_offset, read_offset);

  auto prefix_text = Decode(std::vector<std::int32_t>(
      token_ids.begin() + prefix_offset, token_ids.begin() + read_offset));
  auto new_text = Decode(std::vector<std::int32_t>(
      token_ids.begin() + prefix_offset, token_ids.end()));

  bool ends_with_replacement_char =
      new_text.size() >= 3 &&
      new_text.substr(new_text.size() - 3) == kReplacementCharacter;
  if (new_text.length() > prefix_text.length() && !ends_with_replacement_char) {
    new_text = new_text.substr(prefix_text.length());
    return std::make_tuple(new_text, read_offset, token_ids.size());
  }
  return std::make_tuple("", prefix_offset, read_offset);
}
}  // namespace vajra
