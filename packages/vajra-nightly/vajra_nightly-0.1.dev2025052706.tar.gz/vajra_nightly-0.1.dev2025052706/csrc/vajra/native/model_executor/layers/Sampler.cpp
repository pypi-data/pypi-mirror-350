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
#include "native/model_executor/layers/Sampler.h"

#include "kernels/ops.h"
#include "native/model_executor/layers/attention/flashinfer/Utils.h"
#include "native/model_executor/parallel_utils/ParallelOps.h"
//==============================================================================
using vajra::Sampler;
//==============================================================================
namespace vajra {
//==============================================================================
torch::Tensor PruneHiddenStates(
    const torch::Tensor& hidden_states /*[in]*/,
    const SequenceMetadataVector& seq_metadata_list /*[in]*/) {
  std::vector<int64_t> last_token_indices;
  int64_t token_idx = 0;

  for (const auto& seq_metadata : seq_metadata_list) {
    last_token_indices.push_back(token_idx + seq_metadata->num_q_tokens - 1);
    token_idx += seq_metadata->num_q_tokens;
  }

  auto indices_tensor =
      torch::tensor(last_token_indices, torch::TensorOptions()
                                            .dtype(torch::kInt64)
                                            .device(hidden_states.device()));

  return hidden_states.index_select(0, indices_tensor);
}
//==============================================================================
torch::Tensor GetLogits(
    const torch::Tensor& hidden_states /*[in]*/,
    const torch::Tensor& embedding /*[in]*/, int vocab_size /*[in]*/,
    const c10::intrusive_ptr<c10d::ProcessGroup>& process_group /*[in]*/) {
  auto logits = torch::matmul(hidden_states, embedding.t());
  logits =
      ParallelOps::GatherFromTensorModelParallelRegion(logits, process_group);
  return logits.index(
      {torch::indexing::Slice(), torch::indexing::Slice(0, vocab_size)});
}
//==============================================================================
std::vector<double> GetTemperatures(const Sequences& seqs /*[in]*/) {
  std::vector<double> temperatures;
  temperatures.reserve(seqs.size());

  for (const auto& seq : seqs) {
    double temperature = seq->sampling_params.temperature;
    if (temperature < kSamplingEps) {
      temperature = 1.0;
    }
    temperatures.push_back(temperature);
  }
  return temperatures;
}
//==============================================================================
std::pair<std::vector<double>, std::vector<int>> GetTopPTopK(
    const Sequences& seqs /*[in]*/, int vocab_size /*[in]*/) {
  std::vector<double> top_ps;
  std::vector<int> top_ks;
  top_ps.reserve(seqs.size());
  top_ks.reserve(seqs.size());

  for (const auto& seq : seqs) {
    top_ps.push_back(seq->sampling_params.top_p);
    int top_k = std::min(seq->sampling_params.top_k, vocab_size);
    top_k = (top_k == -1) ? vocab_size : top_k;
    top_ks.push_back(top_k);
  }

  return {top_ps, top_ks};
}
//==============================================================================
Sampler::Sampler(torch::Tensor embedding /*[in]*/, int vocab_size /*[in]*/,
                 ProcessGroupWrapperPtr process_group_wrapper /*[in]*/)
    : embedding_(embedding),
      vocab_size_(vocab_size),
      process_group_(process_group_wrapper->GetTensorModelParallelGroup()) {
  ASSERT_VALID_POINTER_ARGUMENT(process_group_wrapper);
}
//==============================================================================
SamplerOutputs Sampler::Forward(
    const torch::Tensor& logits /*[in]*/, const Sequences& seqs /*[in]*/,
    const SequenceMetadataVector& seq_metadata_list /*[in]*/) const {
  auto pruned_logits = PruneHiddenStates(logits, seq_metadata_list);
  auto next_token_logits =
      GetLogits(pruned_logits, embedding_, vocab_size_, process_group_);

  auto temperatures = GetTemperatures(seqs);
  bool has_non_unity_temp =
      std::any_of(temperatures.begin(), temperatures.end(),
                  [](double t) { return t != 1.0; });

  if (has_non_unity_temp) {
    auto temp_tensor = torch::tensor(
        temperatures,
        torch::TensorOptions().dtype(logits.dtype()).device(logits.device()));
    next_token_logits.div_(temp_tensor.unsqueeze(1));
  }

  auto [top_ps, top_ks] = GetTopPTopK(seqs, vocab_size_);

  auto k_tensor = torch::tensor(
      top_ks,
      torch::TensorOptions().dtype(torch::kInt).device(logits.device()));
  auto p_tensor = torch::tensor(
      top_ps,
      torch::TensorOptions().dtype(torch::kFloat32).device(logits.device()));

  auto sample_results = flashinfer::TopKTopPSamplingFromLogits(
      next_token_logits, k_tensor, p_tensor);
  auto sample_results_cpu = sample_results.cpu();

  SamplerOutputs outputs;
  outputs.reserve(seq_metadata_list.size());

  auto sample_results_accessor = sample_results_cpu.accessor<int, 1>();

  for (size_t seq_idx = 0; seq_idx < seq_metadata_list.size(); ++seq_idx) {
    const auto& metadata = seq_metadata_list[seq_idx];
    outputs.emplace_back(std::make_shared<SamplerOutput>(
        metadata->schedule_id, metadata->seq_id,
        std::vector<TokenId>{
            static_cast<TokenId>(sample_results_accessor[seq_idx])}));
  }

  return outputs;
}
//==============================================================================
}  // namespace vajra
//==============================================================================
