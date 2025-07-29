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
#include "native/transfer_engine/backend/TorchTransferEngine.h"
//==============================================================================
#include "commons/Logging.h"
#include "commons/StdCommon.h"
#include "commons/TorchCommon.h"
#include "native/transfer_engine/backend/TorchTransferWork.h"
#include "native/transfer_engine/backend/TransferEngineUtils.h"
//==============================================================================
using vajra::BaseTransferWork;
using vajra::GlobalResourceConfig;
using vajra::TorchTransferEngine;
using vajra::TorchTransferWork;
using vajra::TransferEngineUtils;
using vajra::TransferOperationRanksType;
//==============================================================================
TorchTransferEngine::TorchTransferEngine(
    std::size_t global_rank, GlobalResourceConfig global_resource_config,
    const c10::intrusive_ptr<c10d::ProcessGroup> global_process_group)
    : global_rank_(global_rank),
      global_resource_config_(global_resource_config),
      global_process_group_(global_process_group) {
  std::size_t curr_num_gpus_seen = 0;
  bool found_replica_id = false;

  for (std::size_t current_replica_index = 0;
       current_replica_index < global_resource_config.size();
       current_replica_index++) {
    const auto& replica_resource_config =
        global_resource_config[current_replica_index];
    replica_global_offsets_.emplace_back(curr_num_gpus_seen);
    curr_num_gpus_seen += replica_resource_config.world_size;
    if (!found_replica_id && curr_num_gpus_seen > global_rank) {
      replica_id_ = current_replica_index;
      found_replica_id = true;
    }
  }
  ASSERT_VALID_RUNTIME(found_replica_id, "Unable to find a replica id for {}",
                       global_rank);
  local_rank_ = global_rank_ - replica_global_offsets_[replica_id_];
}

std::shared_ptr<BaseTransferWork> TorchTransferEngine::AsyncSend(
    std::size_t dst_replica_id, torch::Tensor const& page_tensor,
    const std::vector<std::size_t>& page_list, std::size_t layer_id,
    bool send_to_all) {
  auto future = std::async(std::launch::async, [this, dst_replica_id,
                                                page_tensor, page_list,
                                                layer_id, send_to_all]() {
    // 1. async get global ranks
    auto transfer_operation_ranks_type = TransferOperationRanksType::MATCHING;
    bool split_along_last_dim = true;
    if (send_to_all) {
      ASSERT_VALID_ARGUMENTS(local_rank_ == 0,
                             "If sending to all, then the transfer engine "
                             "expects local rank 0 to only call send.");
      transfer_operation_ranks_type = TransferOperationRanksType::ALL;
      split_along_last_dim = false;
    }
    std::vector<std::size_t> send_global_ranks = GetMatchingOtherGlobalRanks(
        dst_replica_id, layer_id, transfer_operation_ranks_type);

    std::size_t num_send_global_ranks = send_global_ranks.size();
    ASSERT_VALID_RUNTIME(send_global_ranks.size() > 0,
                         "No matching global ranks found for send replica id "
                         "{} and layer id {}!",
                         this->replica_id_, layer_id);
    // 2. async split along last dim
    auto send_page_tensors =
        TransferEngineUtils::GatherMaybeSplitTensorAlongLastDim(
            page_tensor, page_list, num_send_global_ranks,
            split_along_last_dim);
    // 3. async call send(s)
    std::size_t tag = 0;
    this->global_process_group_->startCoalescing(c10::DeviceType::CUDA);
    for (std::size_t i = 0; i < num_send_global_ranks; i++) {
      this->global_process_group_->send(send_page_tensors[i],
                                        send_global_ranks[i], tag);
    }
    auto work =
        this->global_process_group_->endCoalescing(c10::DeviceType::CUDA);

    return work->wait();
  });

  return std::make_shared<TorchTransferWork>(std::move(future));
}

std::shared_ptr<BaseTransferWork> TorchTransferEngine::AsyncRecv(
    std::size_t src_replica_id, torch::Tensor const& page_tensor,
    const std::vector<std::size_t>& page_list, std::size_t layer_id,
    bool recv_from_single_rank) {
  auto future = std::async(std::launch::async, [this, src_replica_id,
                                                page_tensor, page_list,
                                                layer_id,
                                                recv_from_single_rank]() {
    // 1. async get global ranks
    auto transfer_operation_ranks_type = TransferOperationRanksType::MATCHING;
    if (recv_from_single_rank) {
      transfer_operation_ranks_type = TransferOperationRanksType::SINGLE;
    }
    std::vector<std::size_t> recv_global_ranks = GetMatchingOtherGlobalRanks(
        src_replica_id, layer_id, transfer_operation_ranks_type);
    std::size_t num_recv_global_ranks = recv_global_ranks.size();
    ASSERT_VALID_RUNTIME(recv_global_ranks.size() > 0,
                         "No matching global ranks found for recv replica "
                         "id {} and layer id {}!",
                         this->replica_id_, layer_id);
    ASSERT_VALID_RUNTIME(
        transfer_operation_ranks_type == TransferOperationRanksType::MATCHING ||
            (recv_global_ranks.size() == 1 &&
             transfer_operation_ranks_type ==
                 TransferOperationRanksType::SINGLE),
        "There should only be one global rank to recv from when recv from "
        "send_to_all source replica id {} "
        "recv replica id {} and layer id {}!",
        src_replica_id, this->replica_id_, layer_id);
    // 2. async prepare recv buffers
    auto recv_page_tensors = TransferEngineUtils::PreparePageTensorBuffers(
        page_tensor, page_list, num_recv_global_ranks);
    // 3. async call recv(s)
    std::size_t tag = 0;
    this->global_process_group_->startCoalescing(c10::DeviceType::CUDA);
    for (std::size_t i = 0; i < num_recv_global_ranks; i++) {
      this->global_process_group_->recv(recv_page_tensors[i],
                                        recv_global_ranks[i], tag);
    }
    auto work =
        this->global_process_group_->endCoalescing(c10::DeviceType::CUDA);
    bool wait_success = work->wait();
    ASSERT_VALID_RUNTIME(
        wait_success,
        "Failed to wait for recv work on replica id {}, global rank {}!",
        this->replica_id_, this->global_rank_);
    // 4. async copy-merge pages
    TransferEngineUtils::CopyMergePagesCache(recv_page_tensors, page_tensor,
                                             page_list);
    return true;
  });

  return std::make_shared<TorchTransferWork>(std::move(future));
}

std::vector<std::size_t> TorchTransferEngine::GetMatchingOtherGlobalRanks(
    std::size_t other_replica_id, std::size_t layer_id,
    TransferOperationRanksType transfer_operation_ranks_type) {
  if (transfer_operation_ranks_type == TransferOperationRanksType::ALL) {
    return GetAllGlobalRanksForReplicaId(other_replica_id);
  } else if (transfer_operation_ranks_type ==
             TransferOperationRanksType::SINGLE) {
    // Can assume first local rank in the other replica called the send
    return {replica_global_offsets_[other_replica_id]};
  }

  std::vector<std::size_t> matching_other_global_ranks;
  const auto& replica_resource_config = global_resource_config_[replica_id_];
  const auto& other_replica_resource_config =
      global_resource_config_[other_replica_id];

  std::size_t local_tp_rank =
      GetLocalTPRank(local_rank_, replica_resource_config);
  std::size_t local_pp_rank =
      GetLocalPPRank(local_rank_, replica_resource_config);

  std::size_t expected_local_pp_rank =
      std::floor((static_cast<double>(layer_id) /
                  replica_resource_config.total_num_layers) *
                 replica_resource_config.pipeline_parallel_size);
  ASSERT_VALID_ARGUMENTS(
      expected_local_pp_rank == local_pp_rank,
      "Expected local pp rank {} did not match the actual pp rank of {} "
      "for parameter layer id {} and total num layers {}.",
      expected_local_pp_rank, local_pp_rank, layer_id,
      replica_resource_config.total_num_layers);

  std::size_t other_local_tp_rank_start =
      local_tp_rank *
      (static_cast<double>(other_replica_resource_config.tensor_parallel_size) /
       replica_resource_config.tensor_parallel_size);

  // exclusive end
  std::size_t other_local_tp_rank_end = std::ceil(
      (local_tp_rank + 1) *
      (static_cast<double>(other_replica_resource_config.tensor_parallel_size) /
       replica_resource_config.tensor_parallel_size));

  std::size_t other_local_pp_rank =
      std::floor((static_cast<double>(layer_id) /
                  other_replica_resource_config.total_num_layers) *
                 other_replica_resource_config.pipeline_parallel_size);

  for (std::size_t other_local_tp_rank = other_local_tp_rank_start;
       other_local_tp_rank < other_local_tp_rank_end; other_local_tp_rank++) {
    std::size_t other_local_rank =
        other_local_tp_rank +
        other_replica_resource_config.tensor_parallel_size *
            other_local_pp_rank;
    std::size_t other_global_rank =
        other_local_rank + replica_global_offsets_[other_replica_id];
    matching_other_global_ranks.emplace_back(other_global_rank);
  }
  ASSERT_VALID_RUNTIME(
      !matching_other_global_ranks.empty(),
      "Get matching other global ranks failed to find any other ranks!");
  return matching_other_global_ranks;
}

inline std::size_t TorchTransferEngine::GetLocalPPRank(
    std::size_t local_rank, const ReplicaResourceConfig& replica_config) {
  return std::floor(
      (static_cast<double>(local_rank) / replica_config.world_size) *
      replica_config.pipeline_parallel_size);
}

inline std::size_t TorchTransferEngine::GetLocalTPRank(
    std::size_t local_rank, const ReplicaResourceConfig& replica_config) {
  return (local_rank) % replica_config.tensor_parallel_size;
}

inline std::vector<std::size_t>
TorchTransferEngine::GetAllGlobalRanksForReplicaId(
    ReplicaId replica_id) noexcept {
  const auto& replica_config = global_resource_config_[replica_id];

  std::vector<std::size_t> global_ranks(replica_config.world_size);
  std::iota(global_ranks.begin(), global_ranks.end(),
            replica_global_offsets_[replica_id]);
  return global_ranks;
}
//==============================================================================
