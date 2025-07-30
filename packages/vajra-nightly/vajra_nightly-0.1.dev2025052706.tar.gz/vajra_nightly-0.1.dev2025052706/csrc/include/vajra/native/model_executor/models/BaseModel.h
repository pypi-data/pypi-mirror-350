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
//==============================================================================
namespace vajra {
//==============================================================================
class BaseModel : public NonCopyableNonMovable {
 public:
  virtual ~BaseModel() = default;

  virtual torch::Tensor Forward(
      const torch::Tensor& positions /*[in]*/,
      torch::Tensor& hidden_states /*[inout]*/,
      std::vector<torch::Tensor>& kv_caches /*[inout]*/
  ) const = 0;
};
//==============================================================================
using BaseModelPtr = std::shared_ptr<const BaseModel>;
//==============================================================================
}  // namespace vajra
//==============================================================================
