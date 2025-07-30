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

#include "commons/Logging.h"
#include "native/core/block_space_manager/BlockSpaceManager.h"
#include "native/datatypes/Sequence.h"

namespace vajra {
namespace {

class BlockSpaceManagerTest : public ::testing::Test {
 protected:
  void SetUp() override {
    // Create a test sequence
    std::string seq_id = "test_seq";
    std::string prompt = "This is a test prompt";
    std::vector<TokenId> prompt_token_ids = {1, 2, 3, 4, 5};
    std::size_t block_size = 2;
    TokenId eos_token_id = 0;
    TimeS arrival_time = 0.0d;
    SamplingParams sampling_params = SamplingParams();
    test_seq_ = std::make_shared<Sequence>(
        seq_id, prompt, std::make_shared<TokenIds>(prompt_token_ids),
        block_size, eos_token_id, arrival_time, sampling_params);
  }

  SequencePtr test_seq_;
};

TEST_F(BlockSpaceManagerTest, InitializationTest) {
  BlockSpaceManager manager(2, 10, 100, 0.1f);
  EXPECT_TRUE(manager.CanAllocateBlocks(8));    // 10 - 8 = 2 > 1 (watermark)
  EXPECT_FALSE(manager.CanAllocateBlocks(10));  // 10 - 10 = 0 < 1 (watermark)
}

TEST_F(BlockSpaceManagerTest, AllocationTest) {
  BlockSpaceManager manager(2, 10, 100, 0.1f);

  // Allocate 3 blocks
  manager.Allocate(test_seq_, 3);

  // Check if the sequence is allocated
  EXPECT_TRUE(manager.IsAllocated(test_seq_));

  // Check the block table
  auto block_table = manager.GetBlockTable(test_seq_);
  EXPECT_EQ(block_table->size(), 3);

  // Check if we can allocate more blocks
  EXPECT_TRUE(manager.CanAllocateBlocks(6));  // 10 - 3 - 6 = 1 == 1 (watermark)
  EXPECT_FALSE(manager.CanAllocateBlocks(7));  // 10 - 3 - 7 = 0 < 1 (watermark)
}

TEST_F(BlockSpaceManagerTest, AllocateDeltaTest) {
  BlockSpaceManager manager(2, 10, 100, 0.1f);

  // Allocate 3 blocks
  manager.Allocate(test_seq_, 3);

  // Allocate 2 more blocks (total 5)
  manager.AllocateDelta(test_seq_, 5);

  // Check the block table
  auto block_table = manager.GetBlockTable(test_seq_);
  EXPECT_EQ(block_table->size(), 5);

  // Check if we can allocate more blocks
  EXPECT_TRUE(manager.CanAllocateBlocks(4));  // 10 - 5 - 4 = 1 == 1 (watermark)
  EXPECT_FALSE(manager.CanAllocateBlocks(5));  // 10 - 5 - 5 = 0 < 1 (watermark)
}

TEST_F(BlockSpaceManagerTest, FreeTest) {
  BlockSpaceManager manager(2, 10, 100, 0.1f);

  // Allocate 5 blocks
  manager.Allocate(test_seq_, 5);

  // Free the sequence
  manager.Free(test_seq_);

  // Check if the sequence is not allocated
  EXPECT_FALSE(manager.IsAllocated(test_seq_));

  // Check if we can allocate blocks again
  EXPECT_TRUE(manager.CanAllocateBlocks(9));  // 10 - 9 = 1 == 1 (watermark)
}

TEST_F(BlockSpaceManagerTest, AppendSlotTest) {
  BlockSpaceManager manager(2, 10, 100, 0.1f);

  // Allocate 3 blocks
  manager.Allocate(test_seq_, 3);

  // Append 3 slots (should not allocate a new block since the logical blocks
  // are not full)
  bool allocated = manager.AppendSlot(test_seq_, 3);
  EXPECT_FALSE(allocated);

  // Check the block table
  auto block_table = manager.GetBlockTable(test_seq_);
  EXPECT_EQ(block_table->size(), 3);
}

}  // namespace
}  // namespace vajra
