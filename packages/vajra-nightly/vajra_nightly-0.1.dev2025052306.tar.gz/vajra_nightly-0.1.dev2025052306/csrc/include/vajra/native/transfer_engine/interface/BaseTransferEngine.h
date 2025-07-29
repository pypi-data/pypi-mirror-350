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
#include "commons/StdCommon.h"
#include "commons/TorchCommon.h"
#include "native/configs/ReplicaResourceConfig.h"
#include "native/enums/Enums.h"
#include "native/transfer_engine/interface/BaseTransferWork.h"
//==============================================================================
namespace vajra {
//==============================================================================
class BaseTransferEngine : public NonCopyableNonMovable {
 public:
  virtual ~BaseTransferEngine() = default;

  virtual std::shared_ptr<BaseTransferWork> AsyncSend(
      std::size_t dst_replica_id /*[in]*/,
      const torch::Tensor& page_tensor /*[in]*/,
      const std::vector<std::size_t>& page_list /*[in]*/,
      std::size_t layer_id /*[in]*/, bool send_to_all /*[in]*/) = 0;

  virtual std::shared_ptr<BaseTransferWork> AsyncRecv(
      std::size_t src_replica_id /*[in]*/,
      torch::Tensor const& page_tensor /*[out]*/,
      const std::vector<std::size_t>& page_list /*[in]*/,
      std::size_t layer_id /*[in]*/, bool recv_from_single_rank /*[in]*/
      ) = 0;

  virtual std::vector<std::size_t> GetMatchingOtherGlobalRanks(
      std::size_t other_replica_id /*[in]*/, std::size_t layer_id /*[in]*/,
      TransferOperationRanksType transfer_operation_ranks_type =
          TransferOperationRanksType::MATCHING /*[in]*/) = 0;
};
//==============================================================================
}  // namespace vajra
//==============================================================================
