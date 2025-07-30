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
#include <atomic>

#include "commons/BoostCommon.h"
#include "commons/StdCommon.h"
#include "native/configs/ReplicasetControllerConfig.h"
#include "native/core/controller/replicaset_controllers/BaseReplicasetController.h"
#include "native/core/scheduler/replicaset_schedulers/BaseReplicasetScheduler.h"
#include "native/core/scheduler/request_prioritizers/BaseRequestPrioritizer.h"
#include "native/core/tokenizer/TokenizerPool.h"
#include "native/datatypes/Sequence.h"
//==============================================================================
namespace vajra {
//==============================================================================
template <typename WaitingQueueType, typename OutputQueueType>
class LlmReplicasetController
    : public BaseReplicasetController<WaitingQueueType, OutputQueueType> {
 public:
  LlmReplicasetController(
      std::shared_ptr<LlmReplicasetControllerConfig> config,
      const std::string& tokenizer_path, TokenId eos_token_id,
      std::shared_ptr<WaitingQueueType> waiting_seq_queue,
      std::shared_ptr<OutputQueueType> output_queue,
      std::shared_ptr<BaseRequestPrioritizer> request_prioritizer,
      std::shared_ptr<BaseReplicasetScheduler> replica_scheduler)
      : BaseReplicasetController<WaitingQueueType, OutputQueueType>(
            config, waiting_seq_queue, output_queue, request_prioritizer,
            replica_scheduler),
        tokenizer_pool_(
            TokenizerPool(tokenizer_path, config->num_tokenizer_workers)),
        eos_token_id_(eos_token_id),
        should_stop_(false) {
    ASSERT_VALID_POINTER_ARGUMENT(config);
    ASSERT_VALID_POINTER_ARGUMENT(request_prioritizer);
    ASSERT_VALID_POINTER_ARGUMENT(replica_scheduler);
    ASSERT_VALID_POINTER_ARGUMENT(waiting_seq_queue);
    ASSERT_VALID_POINTER_ARGUMENT(output_queue);

    tokenizer_pool_.Start();

    tokenizer_output_thread_ =
        std::thread([this]() { this->ProcessTokenizerOutputLoop(); });

    input_queue_watch_thread_ =
        std::thread([this]() { this->InputQueueWatchLoop(); });
  }

  ~LlmReplicasetController() { Stop(); }

  void Stop() {
    should_stop_ = true;
    tokenizer_pool_.Shutdown();
    this->waiting_seq_queue_->close();
    this->output_queue_->close();
    tokenizer_output_thread_.join();
    input_queue_watch_thread_.join();
  }

 private:
  void ProcessTokenizerOutputLoop() {
    auto block_size =
        this->config_->replica_controller_config->cache_config.block_size;

    while (!should_stop_) {
      ProcessTokenizerOutput(block_size);
    }
  }

  void ProcessTokenizerOutput(int block_size) {
    auto tokenizer_output = tokenizer_pool_.GetOutput();
    if (!tokenizer_output) {
      return;  // Skip processing if output is null
    }
    auto seq_params = SequenceParams(
        tokenizer_output->seq_id, tokenizer_output->prompt,
        tokenizer_output->token_ids, block_size, eos_token_id_,
        tokenizer_output->arrival_time, tokenizer_output->sampling_params);
    MutableSequencePtr seq = std::make_shared<Sequence>(Sequence(seq_params));
    auto seq_with_priority =
        this->request_prioritizer_->GetSeqWithPriority(seq);
    this->replica_scheduler_->Schedule(seq_with_priority);
  }

  void InputQueueWatchLoop() {
    while (!should_stop_) {
      if (!ProcessInputQueue()) {
        break;
      }
    }
  }

  bool ProcessInputQueue() {
    try {
      std::shared_ptr<const UserSequenceParams> user_seq_params;
      boost::concurrent::queue_op_status status =
          this->waiting_seq_queue_->try_pull(user_seq_params);
      if (status == boost::concurrent::queue_op_status::success &&
          user_seq_params) {
        ProcessUserSequence(user_seq_params);
        return true;
      } else if (status == boost::concurrent::queue_op_status::closed) {
        return false;
      }
      return true;
    } catch (const boost::sync_queue_is_closed& e) {
      return false;
    }
  }

  void ProcessUserSequence(
      const std::shared_ptr<const UserSequenceParams>& user_seq_params) {
    ASSERT_VALID_POINTER_ARGUMENT(user_seq_params);

    if (user_seq_params->prompt_token_ids->empty()) {
      tokenizer_pool_.AddRequest(TokenizerPoolInput(
          user_seq_params->seq_id, user_seq_params->arrival_time,
          user_seq_params->prompt, user_seq_params->sampling_params));
    } else {
      tokenizer_pool_.AddOutput(TokenizerPoolOutput(
          user_seq_params->seq_id, user_seq_params->arrival_time,
          user_seq_params->prompt, user_seq_params->prompt_token_ids,
          user_seq_params->sampling_params));
    }
  }

  TokenizerPool tokenizer_pool_;
  TokenId eos_token_id_;
  std::atomic<bool> should_stop_;

  std::thread tokenizer_output_thread_;
  std::thread input_queue_watch_thread_;
};
//==============================================================================
}  // namespace vajra
//==============================================================================
