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
#include "native/model_executor/LLMModelRunner.h"
//==============================================================================
using vajra::LLMModelRunner;
using vajra::PreparedInputs;
using vajra::SamplerOutputs;
//==============================================================================
LLMModelRunner::LLMModelRunner(
    std::shared_ptr<BaseReplicaControllerConfig> config /*[in]*/,
    torch::Device device /*[in]*/, std::size_t rank /*[in]*/,
    BaseModelPtr model /*[in]*/,
    ProcessGroupWrapperPtr process_group_wrapper /*[in]*/,
    WorkerMetricsStorePtr worker_metrics_store /*[in]*/,
    SamplerPtr sampler /*[in]*/
    )
    : BaseModelRunner(config, device, rank, model, process_group_wrapper,
                      worker_metrics_store),
      sampler_(sampler),
      is_pipeline_first_stage_(process_group_wrapper->IsPipelineFirstStage()),
      is_pipeline_last_stage_(process_group_wrapper->IsPipelineLastStage()),
      send_stream_(c10::cuda::getStreamFromPool(/* isHighPriority */ true,
                                                device.index())),
      recv_stream_(c10::cuda::getStreamFromPool(/* isHighPriority */ true,
                                                device.index())),
      prepare_inputs_timer_(MetricType::PREPARE_INPUTS, worker_metrics_store),
      sampler_timer_(MetricType::SAMPLER, worker_metrics_store),
      model_execution_timer_(MetricType::MODEL_EXECUTION, worker_metrics_store),
      attn_begin_forward_timer_(MetricType::ATTN_BEGIN_FORWARD,
                                worker_metrics_store) {
  ASSERT_VALID_POINTER_ARGUMENT(config);
  ASSERT_VALID_POINTER_ARGUMENT(worker_metrics_store);
  ASSERT_VALID_POINTER_ARGUMENT(sampler);
  ASSERT_VALID_POINTER_ARGUMENT(model);
  ASSERT_VALID_POINTER_ARGUMENT(process_group_wrapper);
}
//==============================================================================
PreparedInputs LLMModelRunner::PrepareInputs(
    const Sequences& seqs /*[in]*/,
    const SequenceMetadataVector& seq_metadata_list /*[in]*/
) const {
  // This method prepares the input tokens and positions for the model
  // It extracts tokens from sequences based on metadata
  // and converts them to tensors

  std::vector<int64_t> input_tokens;
  std::vector<int64_t> input_positions;

  ASSERT_VALID_RUNTIME(seqs.size() == seq_metadata_list.size(),
                       "seqs and seq_metadata_list must be the same size");
  // Extract tokens and positions from each sequence
  for (size_t i = 0; i < seqs.size(); ++i) {
    const auto& seq = seqs[i];
    const auto& seq_metadata = seq_metadata_list[i];

    // Get the last n token ids from the sequence
    auto token_ids = seq->GetLastNTokenIds(seq_metadata->num_q_tokens);
    input_tokens.insert(input_tokens.end(), token_ids.begin(), token_ids.end());

    // Calculate positions
    auto start_position = seq->GetNumTokensStageProcessed();
    auto end_position = start_position + seq_metadata->num_q_tokens;

    input_positions.reserve(input_positions.size() +
                            (end_position - start_position));
    for (auto pos = start_position; pos < end_position; ++pos) {
      input_positions.push_back(pos);
    }
  }

  // Optimization: Pad the input length to be a multiple of 8.
  // This is required for utilizing the Tensor Cores in NVIDIA GPUs.
  input_tokens = PadToAlignment<int64_t>(input_tokens, 8, 0);
  input_positions = PadToAlignment<int64_t>(input_positions, 8, 0);

  // Convert to tensors
  auto tokens_tensor = torch::tensor(input_tokens, torch::kLong).to(device_);
  auto positions_tensor =
      torch::tensor(input_positions, torch::kLong).to(device_);

  return std::make_pair(tokens_tensor, positions_tensor);
}
//==============================================================================
SamplerOutputs LLMModelRunner::Run(
    const Sequences& seqs /*[in]*/,
    const SequenceMetadataVector& seq_metadata_list /*[in]*/,
    std::vector<torch::Tensor>& gpu_caches /*[inout]*/
) {
  if (seq_metadata_list.empty()) {
    return {};
  }

  // Calculate the total number of tokens, rounded up to a multiple of 8
  size_t batch_num_tokens = 0;
  for (const auto& metadata : seq_metadata_list) {
    batch_num_tokens += metadata->num_q_tokens;
  }
  batch_num_tokens = RoundUpToMultiple(batch_num_tokens, 8);

  // Initialize hidden states if not in the first pipeline stage
  torch::Tensor hidden_states;
  if (!is_pipeline_first_stage_) {
    // Receive hidden states from the previous pipeline stage
    auto hidden_size = config_->model_config.hidden_size;
    auto dtype = GetScalarTypeFromString(config_->model_config.dtype);

    // Use recv_stream_ for receiving hidden states
    {
      at::cuda::CUDAStreamGuard guard(recv_stream_);

      hidden_states = ParallelOps::RecvFromLastPipelineStage(
          {static_cast<int64_t>(batch_num_tokens),
           static_cast<int64_t>(hidden_size)},
          dtype, device_, process_group_wrapper_,
          config_->parallel_config.enable_chunked_pipeline_comm_opt);
    }
  }

  // Prepare input tokens and positions
  PreparedInputs prepared_inputs;
  {
    auto timer_guard = prepare_inputs_timer_.TimeOperation();
    prepared_inputs = PrepareInputs(seqs, seq_metadata_list);
  }

  // Unpack prepared inputs
  auto [input_tokens, input_positions] = prepared_inputs;

  // Get input tensor based on pipeline stage
  torch::Tensor input_tensor;
  if (!is_pipeline_first_stage_) {
    input_tensor = hidden_states;
  } else {
    input_tensor = input_tokens;
  }

  {
    auto timer_guard = attn_begin_forward_timer_.TimeOperation();
    AttentionWrapper::GetOrCreateThreadLocalInstance()->BeginForward(
        seq_metadata_list);
  }

  // CUDA synchronization
  torch::cuda::synchronize();

  // Run the model
  torch::Tensor output;
  {
    auto timer_guard = model_execution_timer_.TimeOperation();
    output = model_->Forward(input_positions, input_tensor, gpu_caches);
  }

  // CUDA synchronization
  torch::cuda::synchronize();

  AttentionWrapper::GetOrCreateThreadLocalInstance()->EndForward();

  // Handle output based on pipeline stage
  if (sampler_ != nullptr) {
    // Apply sampling if this is the last pipeline stage
    auto timer_guard = sampler_timer_.TimeOperation();
    return sampler_->Forward(output, seqs, seq_metadata_list);
  } else {
    // Send output to the next pipeline stage if not the last stage
    ASSERT_VALID_RUNTIME(
        !is_pipeline_last_stage_,
        "Sampler must be set for only the last pipeline stage");

    // Use send_stream_ for sending output
    {
      at::cuda::CUDAStreamGuard guard(send_stream_);

      ParallelOps::SendToNextPipelineStage(
          output, process_group_wrapper_,
          config_->parallel_config.enable_chunked_pipeline_comm_opt);
    }
    return {};
  }
}
//==============================================================================
