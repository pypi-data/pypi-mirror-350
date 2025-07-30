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
#include <gtest/gtest.h>

#include "native/core/tokenizer/TokenizerPool.h"

namespace vajra {
namespace {
class TokenizerPoolTest : public ::testing::Test {
 protected:
  void SetUp() override {}
};

TEST_F(TokenizerPoolTest, SingleRequest) {
  std::string filepath = "testdata/native/TokenizerTest/tokenizer.json";
  auto pool = TokenizerPool(filepath, 2);

  auto prompt = "hello there";

  pool.Start();

  pool.AddRequest(TokenizerPoolInput("0", 0.0, prompt, SamplingParams()));

  auto out = pool.GetOutput();
  std::vector<TokenId> expected = {15339, 1070};
  ASSERT_EQ(*out->token_ids, expected);

  pool.Shutdown();
}

TEST_F(TokenizerPoolTest, ManyRequests) {
  std::string filepath = "testdata/native/TokenizerTest/tokenizer.json";
  auto tokenizer = Tokenizer::FromPath(filepath);
  auto num_workers = 8;
  auto pool = TokenizerPool(filepath, num_workers);
  pool.Start();

  std::size_t num_requests = 100;
  for (std::size_t i = 0; i < num_requests; i++) {
    auto id = std::format("{}", i);
    auto prompt = std::format("{}", id);
    pool.AddRequest(TokenizerPoolInput(id, 0.0, prompt, SamplingParams()));
  }

  for (std::size_t i = 0; i < num_requests; i++) {
    auto out = pool.GetOutput();
    auto expected = tokenizer.Encode(out->seq_id);
    ASSERT_EQ(*out->token_ids, expected);
  }

  pool.Shutdown();
}
}  // namespace
}  // namespace vajra
