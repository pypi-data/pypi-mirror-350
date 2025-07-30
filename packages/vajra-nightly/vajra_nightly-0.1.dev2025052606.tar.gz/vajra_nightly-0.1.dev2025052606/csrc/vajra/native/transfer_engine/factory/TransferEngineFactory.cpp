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
#include "native/transfer_engine/factory/TransferEngineFactory.h"
//==============================================================================
using vajra::BaseTransferEngine;
using vajra::TransferBackendType;
using vajra::TransferEngineConfig;
using vajra::TransferEngineFactory;
//==============================================================================
std::shared_ptr<BaseTransferEngine> TransferEngineFactory::Create(
    TransferEngineConfig transfer_engine_config) {
  ASSERT_VALID_ARGUMENTS(transfer_engine_config.transfer_backend_type ==
                             TransferBackendType::TORCH,
                         "Only Torch backend is supported today");
  return std::make_shared<TorchTransferEngine>(
      transfer_engine_config.global_rank,
      transfer_engine_config.global_resource_config,
      transfer_engine_config.global_process_group);
}
//==============================================================================
