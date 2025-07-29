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
#include "commons/BoostCommon.h"
#include "commons/ClassTraits.h"
#include "commons/StdCommon.h"
#include "native/data_structures/Queues.h"
#include "native/datatypes/RequestOutput.h"
#include "native/datatypes/SamplingParams.h"
#include "native/datatypes/Sequence.h"
#include "native/metrics_store/EngineMetricsStore.h"
//==============================================================================
namespace vajra {
//==============================================================================
class InferenceEngine : public NonCopyableNonMovable {
 public:
  explicit InferenceEngine(const EngineMetricsStorePtr& metrics_store)
      : metrics_store_(metrics_store),
        waiting_seq_queue_(std::make_shared<UserSequenceParamQueue>()),
        output_queue_(std::make_shared<RequestOutputQueue>()) {
    ASSERT_VALID_POINTER_ARGUMENT(metrics_store)
  }

  ~InferenceEngine() = default;

  void AddRequest(const std::optional<std::string>& seq_id,
                  const std::string& prompt, const TokenIdsPtr prompt_token_ids,
                  const SamplingParams& sampling_params);

  [[nodiscard]] UserSequenceParamQueuePtr GetWaitingSeqQueue() const {
    return waiting_seq_queue_;
  }

  [[nodiscard]] RequestOutputQueuePtr GetOutputQueue() const {
    return output_queue_;
  }

  [[nodiscard]] std::vector<RequestOutput> GetOutputs(bool block = false) const;

 private:
  EngineMetricsStorePtr metrics_store_;
  UserSequenceParamQueuePtr waiting_seq_queue_;
  RequestOutputQueuePtr output_queue_;
  std::atomic<std::size_t> seq_id_counter_ = 0;
};
//==============================================================================
}  // namespace vajra
//==============================================================================
