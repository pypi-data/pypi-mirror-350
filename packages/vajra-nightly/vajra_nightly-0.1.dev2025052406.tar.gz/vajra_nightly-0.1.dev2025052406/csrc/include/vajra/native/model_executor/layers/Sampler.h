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
#include "commons/TorchCommon.h"
#include "native/datatypes/SamplerOutput.h"
#include "native/datatypes/Sequence.h"
#include "native/datatypes/SequenceMetadata.h"
#include "native/model_executor/parallel_utils/ProcessGroupWrapper.h"
//==============================================================================
namespace vajra {
//==============================================================================
constexpr double kSamplingEps = 1e-5f;
//==============================================================================
class Sampler : public NonCopyableNonMovable {
 public:
  Sampler(torch::Tensor embedding /*[in]*/, int vocab_size /*[in]*/,
          ProcessGroupWrapperPtr process_group_wrapper /*[in]*/);

  [[nodiscard]] SamplerOutputs Forward(
      const torch::Tensor& logits /*[in]*/, const Sequences& seqs /*[in]*/,
      const SequenceMetadataVector& seq_metadata_list /*[in]*/) const;

 private:
  const torch::Tensor embedding_;
  const int vocab_size_;
  const c10::intrusive_ptr<c10d::ProcessGroup> process_group_;
};
//==============================================================================
using SamplerPtr = std::shared_ptr<const Sampler>;
//==============================================================================
}  // namespace vajra
//==============================================================================
