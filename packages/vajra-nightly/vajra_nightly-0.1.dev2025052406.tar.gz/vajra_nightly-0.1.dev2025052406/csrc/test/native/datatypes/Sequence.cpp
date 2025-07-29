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
#include "native/datatypes/Sequence.h"

#include <gtest/gtest.h>

#include <memory>
#include <vector>

#include "native/datatypes/SamplingParams.h"

using vajra::SamplingParams;
using vajra::Sequence;
using vajra::TimeS;
using vajra::TokenIds;

class SequenceTest : public ::testing::Test {
 protected:
  void SetUp() override {
    // Common setup for tests
    std::string seq_id = "test_sequence";
    std::string prompt = "This is a test prompt";
    std::shared_ptr<TokenIds> prompt_tokens = std::make_shared<TokenIds>();
    prompt_tokens->insert(prompt_tokens->end(), {1, 2, 3, 4, 5});
    std::size_t block_size = 1024;
    std::size_t eos_token_id = 0;
    TimeS arrival_time = 0.0;
    SamplingParams sampling_params;  // Default sampling params

    sequence =
        std::make_unique<Sequence>(seq_id, prompt, prompt_tokens, block_size,
                                   eos_token_id, arrival_time, sampling_params);
  }

  std::unique_ptr<Sequence> sequence;
};

// Test token processing workflow: unprocessed -> stage processed -> processed
TEST_F(SequenceTest, TokenProcessingWorkflow) {
  // Initially no tokens processed
  EXPECT_EQ(sequence->GetNumPromptTokensStageProcessed(), 0);
  EXPECT_EQ(sequence->GetNumPromptTokensProcessed(), 0);
  EXPECT_FALSE(sequence->GetPromptStageProcessingFinished());
  EXPECT_FALSE(sequence->GetPromptProcessingFinished());

  // Step 1: Stage process first 2 tokens
  sequence->UpdatePromptTokensStageProcessed(2);
  EXPECT_EQ(sequence->GetNumPromptTokensStageProcessed(), 2);
  EXPECT_EQ(sequence->GetNumPromptTokensProcessed(), 0);
  EXPECT_FALSE(sequence->GetPromptStageProcessingFinished());

  // Step 2: Fully process first token
  sequence->UpdatePromptTokensProcessed(1);
  EXPECT_EQ(sequence->GetNumPromptTokensStageProcessed(), 2);
  EXPECT_EQ(sequence->GetNumPromptTokensProcessed(), 1);

  // Step 3: Stage process all prompt tokens
  sequence->UpdatePromptTokensStageProcessed(3);
  EXPECT_EQ(sequence->GetNumPromptTokensStageProcessed(), 5);
  EXPECT_TRUE(sequence->GetPromptStageProcessingFinished());
  EXPECT_FALSE(sequence->GetPromptProcessingFinished());

  // Step 4: Process all prompt tokens
  sequence->UpdatePromptTokensProcessed(4);
  EXPECT_EQ(sequence->GetNumPromptTokensProcessed(), 5);
  EXPECT_TRUE(sequence->GetPromptProcessingFinished());
}

// Test AppendTokenId
TEST_F(SequenceTest, AppendTokenId) {
  // process prompt tokens
  sequence->UpdatePromptTokensStageProcessed(5);
  sequence->UpdatePromptTokensProcessed(5);
  EXPECT_TRUE(sequence->GetPromptProcessingFinished());
  EXPECT_EQ(sequence->GetNumTokensProcessed(), 5);

  // Add output tokens
  sequence->AppendTokenId(10);
  sequence->AppendTokenId(20);
  // Verify they're added but not processed
  EXPECT_EQ(sequence->GetOutputLength(), 2);
  EXPECT_EQ(sequence->GetOutputTokenIds()->at(0), 10);
  EXPECT_EQ(sequence->GetOutputTokenIds()->at(1), 20);
  // should not affect number of processed tokens
  EXPECT_EQ(sequence->GetNumTokensProcessed(), 5);
  EXPECT_EQ(sequence->GetNumTokensStageProcessed(), 5);

  // process output tokens
  sequence->UpdateTokensProcessed(2);
  EXPECT_EQ(sequence->GetNumTokensProcessed(), 7);
}

TEST_F(SequenceTest, OutOfBoundsUpdate) {
  // Try to stage process more tokens than exist
  EXPECT_THROW(sequence->UpdatePromptTokensStageProcessed(10),
               std::runtime_error);

  sequence->UpdatePromptTokensStageProcessed(4);
  EXPECT_THROW(sequence->UpdatePromptTokensStageProcessed(2),
               std::runtime_error);

  // Try to append tokens before processing prompt
  EXPECT_THROW(sequence->AppendTokenId(10), std::runtime_error);

  sequence->UpdatePromptTokensStageProcessed(1);
  EXPECT_TRUE(sequence->GetPromptStageProcessingFinished());
  EXPECT_FALSE(sequence->GetPromptProcessingFinished());
  EXPECT_THROW(sequence->AppendTokenId(10), std::runtime_error);

  sequence->UpdatePromptTokensProcessed(4);
  EXPECT_THROW(sequence->UpdatePromptTokensProcessed(2), std::runtime_error);

  sequence->UpdatePromptTokensProcessed(1);
  sequence->AppendTokenId(10);
  EXPECT_EQ(sequence->GetNumTokensProcessed(), 5);
  sequence->UpdateTokensProcessed(1);
  EXPECT_EQ(sequence->GetNumTokensProcessed(), 6);
}

TEST_F(SequenceTest, NumQTokens) {
  EXPECT_EQ(sequence->GetNumProcessableTokens(), 5);
  EXPECT_EQ(sequence->GetNumPromptTokensStageProcessed(), 0);
  EXPECT_EQ(sequence->GetNumPromptTokensProcessed(), 0);
  EXPECT_FALSE(sequence->GetPromptStageProcessingFinished());
  EXPECT_FALSE(sequence->GetPromptProcessingFinished());

  // Step 1: Stage process first 2 tokens
  sequence->UpdatePromptTokensStageProcessed(2);
  EXPECT_EQ(sequence->GetNumPromptTokensStageProcessed(), 2);
  EXPECT_EQ(sequence->GetNumPromptTokensProcessed(), 0);
  EXPECT_FALSE(sequence->GetPromptStageProcessingFinished());
  EXPECT_EQ(sequence->GetNumProcessableTokens(), 3);

  // Step 2: Fully process first token
  sequence->UpdatePromptTokensProcessed(1);
  EXPECT_EQ(sequence->GetNumPromptTokensStageProcessed(), 2);
  EXPECT_EQ(sequence->GetNumPromptTokensProcessed(), 1);
  EXPECT_EQ(sequence->GetNumProcessableTokens(), 3);

  // Step 3: Stage process all prompt tokens
  sequence->UpdatePromptTokensStageProcessed(3);
  EXPECT_EQ(sequence->GetNumPromptTokensStageProcessed(), 5);
  EXPECT_TRUE(sequence->GetPromptStageProcessingFinished());
  EXPECT_FALSE(sequence->GetPromptProcessingFinished());
  EXPECT_EQ(sequence->GetNumProcessableTokens(), 0);

  // Step 4: Process all prompt tokens
  sequence->UpdatePromptTokensProcessed(4);
  EXPECT_EQ(sequence->GetNumPromptTokensProcessed(), 5);
  EXPECT_TRUE(sequence->GetPromptProcessingFinished());

  // Step 5: Append tokens
  sequence->AppendTokenId(10);
  sequence->AppendTokenId(20);
  EXPECT_EQ(sequence->GetNumProcessableTokens(), 2);
}
