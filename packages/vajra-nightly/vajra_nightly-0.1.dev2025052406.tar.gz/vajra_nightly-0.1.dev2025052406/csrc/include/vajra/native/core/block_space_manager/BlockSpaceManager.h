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
#include "commons/ClassTraits.h"
#include "commons/Logging.h"
#include "commons/StdCommon.h"
#include "native/datatypes/Sequence.h"
//==============================================================================
namespace vajra {
//==============================================================================
// BlockTable is a list of physical block IDs that correspond to logical blocks
using BlockTable = std::vector<int>;
using BlockTablePtr = std::shared_ptr<BlockTable>;
//==============================================================================
/**
 * @brief Manages the mapping between logical and physical token blocks.
 *
 * BlockSpaceManager is responsible for allocating and freeing physical blocks
 * for sequences, and maintaining the mapping between logical and physical
 * blocks.
 */
class BlockSpaceManager : public NonCopyableNonMovable {
 public:
  /**
   * @brief Constructs a BlockSpaceManager
   *
   * @param block_size Size of each token block
   * @param num_gpu_blocks Total number of available GPU blocks
   * @param max_model_len Maximum model sequence length
   * @param watermark Watermark ratio to maintain free blocks (default: 0.01)
   */
  BlockSpaceManager(int block_size /*[in]*/, int num_gpu_blocks /*[in]*/,
                    int max_model_len /*[in]*/,
                    float watermark = 0.01f /*[in]*/);

  /**
   * @brief Checks if enough blocks can be allocated
   *
   * @param num_required_blocks Number of blocks required
   * @return true if there are enough free blocks available
   */
  [[nodiscard]] bool CanAllocateBlocks(int num_required_blocks /*[in]*/) const;

  /**
   * @brief Allocates physical blocks for a sequence
   *
   * @param seq The sequence to allocate blocks for
   * @param num_blocks Number of blocks to allocate
   */
  void Allocate(const SequencePtr seq /*[in]*/, int num_blocks /*[in]*/);

  /**
   * @brief Allocates additional blocks for a sequence
   *
   * @param seq The sequence to allocate blocks for
   * @param total_num_blocks Total number of blocks the sequence should have
   */
  void AllocateDelta(const SequencePtr seq /*[in]*/,
                     int total_num_blocks /*[in]*/);

  /**
   * @brief Checks if a slot can be appended
   *
   * @return true if there are free blocks available
   */
  [[nodiscard]] bool CanAppendSlot() const;

  /**
   * @brief Allocates a physical slot for a new token
   *
   * @param seq The sequence to append a slot to
   * @param num_total_blocks Total number of blocks
   * @return true if a new block was allocated
   */
  [[nodiscard]] bool AppendSlot(const SequencePtr seq /*[in]*/,
                                int num_total_blocks /*[in]*/);

  /**
   * @brief Frees all blocks allocated to a sequence
   *
   * @param seq The sequence to free blocks for
   */
  void Free(const SequencePtr seq /*[in]*/);

  /**
   * @brief Gets the block table for a sequence
   *
   * @param seq The sequence to get the block table for
   * @return The block table
   */
  [[nodiscard]] const BlockTablePtr GetBlockTable(
      const SequencePtr seq /*[in]*/) const;

  /**
   * @brief Gets the block table for a sequence by copying
   *
   * @param seq The sequence to get the block table for
   * @return The block table copy
   */
  [[nodiscard]] BlockTable GetBlockTableCopy(
      const SequencePtr seq /*[in]*/) const;

  /**
   * @brief Checks if a sequence has blocks allocated
   *
   * @param seq The sequence to check
   * @return true if the sequence has blocks allocated
   */
  [[nodiscard]] bool IsAllocated(const SequencePtr seq /*[in]*/) const;

 private:
  /**
   * @brief Allocates a free block
   *
   * @return The allocated block ID
   */
  [[nodiscard]] int AllocateFreeBlock();

  // Block size in tokens
  int block_size_;

  // Total number of GPU blocks available
  int num_total_gpu_blocks_;

  // Maximum model sequence length
  int max_model_len_;

  // Watermark ratio to maintain free blocks
  float watermark_;

  // Number of blocks to keep free based on watermark
  int watermark_blocks_;

  // Mapping from sequence ID to block table
  std::unordered_map<std::string, BlockTablePtr> block_tables_;

  // List of free block IDs
  std::vector<int> free_blocks_;
};
//==============================================================================
}  // namespace vajra
//==============================================================================
