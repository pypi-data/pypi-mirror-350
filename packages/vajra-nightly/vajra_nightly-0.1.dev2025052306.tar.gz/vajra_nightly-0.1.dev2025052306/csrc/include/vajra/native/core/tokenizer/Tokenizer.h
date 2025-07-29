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
#include <tokenizers_cpp.h>
//==============================================================================
#include "commons/Logging.h"
#include "commons/StdCommon.h"
//==============================================================================
namespace vajra {
//==============================================================================
static constexpr const char* kReplacementCharacter = "\xef\xbf\xbd";
//==============================================================================
/**
 * @class Tokenizer
 * @brief A wrapper class for tokenization operations using the tokenizers_cpp
 * library
 */
class Tokenizer {
 public:
  /**
   * @brief Construct a Tokenizer with a pre-configured tokenizer
   *
   * @param tokenizer A unique pointer to a tokenizers::Tokenizer instance
   */
  explicit Tokenizer(std::unique_ptr<tokenizers::Tokenizer> tokenizer)
      : tokenizer_(std::move(tokenizer)) {}

  /**
   * @brief Create a Tokenizer instance from a tokenizer configuration file
   *
   * @param path The file path to the tokenizer configuration
   * @return Tokenizer A new Tokenizer instance
   *
   * @example
   * auto tokenizer = vajra::Tokenizer::FromPath("tokenizers.json");
   */
  static Tokenizer FromPath(const std::string& path);

  /**
   * @brief Encode a text string into a vector of token IDs
   *
   * @param text The input text to be tokenized
   * @return std::vector<std::int32_t> A vector of token IDs representing the
   * input text
   *
   * @example
   * std::string text = "Hello, world!";
   * auto token_ids = tokenizer.Encode(text);
   */
  std::vector<std::int32_t> Encode(const std::string& text) const;

  /**
   * @brief Decode a vector of token IDs back to a text string
   *
   * @param token_ids A vector of token IDs to be converted to text
   * @return std::string The decoded text
   *
   * @example
   * std::vector<std::int32_t> token_ids = {101, 7592, 1010, 2088, 999, 102};
   * std::string decoded_text = tokenizer.Decode(token_ids);
   */
  std::string Decode(const std::vector<std::int32_t>& token_ids);

  /**
   * @brief Partially decode a sequence for incremental decoding.
   *
   * This function decodes new tokens that have been appended to a previously
   * processed sequence. It works with two offsets:
   * - prefix_offset: Starting position for both the previous and new decoding
   * - read_offset: End position of previously decoded tokens
   *
   * The function:
   * 1. Decodes the prefix text (tokens[prefix_offset:read_offset])
   * 2. Decodes the full text (tokens[prefix_offset:])
   * 3. Returns the incremental portion (full_text - prefix_text) if:
   *    - The incremental portion has content (length > 0)
   *    - The full text doesn't end with a replacement character
   *
   * @param token_ids The complete token sequence
   * @param prefix_offset Starting offset for decoding
   * @param read_offset End offset of previously decoded tokens
   *
   * @return A tuple containing:
   *   - The newly decoded text (empty string if conditions aren't met)
   *   - Updated prefix_offset for next call (unchanged if no new content)
   *   - Updated read_offset for next call (unchanged if no new content,
   *     or set to token_ids.size() if new content was decoded)
   */
  std::tuple<std::string, std::size_t, std::size_t> PartialDecode(
      const std::vector<std::int32_t>& token_ids, std::size_t prefix_offset,
      std::size_t read_offset);

 private:
  std::unique_ptr<tokenizers::Tokenizer> tokenizer_;
};
//==============================================================================
}  // namespace vajra
//==============================================================================
