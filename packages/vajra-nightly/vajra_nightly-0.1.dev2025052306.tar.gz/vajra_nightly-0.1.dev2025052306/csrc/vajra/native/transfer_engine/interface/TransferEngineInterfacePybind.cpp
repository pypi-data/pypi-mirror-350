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
#include "native/transfer_engine/interface/TransferEngineInterfacePybind.h"
//==============================================================================
#include "native/configs/TransferEngineConfig.h"
#include "native/transfer_engine/factory/TransferEngineFactory.h"
#include "native/transfer_engine/interface/BaseTransferEngine.h"
#include "native/transfer_engine/interface/BaseTransferWork.h"
//==============================================================================
namespace vajra {
//==============================================================================
class PyTransferWork : public BaseTransferWork {
 public:
  bool Synchronize() override {
    PYBIND11_OVERRIDE(bool, BaseTransferWork, Synchronize);
  }
};
//==============================================================================
class PyTransferEngine : public BaseTransferEngine {
 public:
  std::shared_ptr<BaseTransferWork> AsyncSend(
      std::size_t dst_replica_id /*[in]*/,
      const torch::Tensor& page_tensor /*[in]*/,
      const std::vector<std::size_t>& page_list /*[in]*/,
      std::size_t layer_id /*[in]*/, bool send_to_all /*[in]*/) override {
    PYBIND11_OVERRIDE(std::shared_ptr<BaseTransferWork>, BaseTransferEngine,
                      AsyncSend, dst_replica_id, page_tensor, page_list,
                      layer_id, send_to_all);
  }

  std::shared_ptr<BaseTransferWork> AsyncRecv(
      std::size_t src_replica_id /*[in]*/,
      torch::Tensor const& page_tensor /*[out]*/,
      const std::vector<std::size_t>& page_list /*[in]*/,
      std::size_t layer_id /*[in]*/,
      bool recv_from_single_rank /*[in]*/) override {
    PYBIND11_OVERRIDE(std::shared_ptr<BaseTransferWork>, BaseTransferEngine,
                      AsyncRecv, src_replica_id, page_tensor, page_list,
                      layer_id, recv_from_single_rank);
  }

  std::vector<std::size_t> GetMatchingOtherGlobalRanks(
      std::size_t other_replica_id /*[in]*/, std::size_t layer_id /*[in]*/,
      TransferOperationRanksType transfer_operation_ranks_type =
          TransferOperationRanksType::MATCHING /*[in]*/) override {
    PYBIND11_OVERRIDE(std::vector<std::size_t>, BaseTransferEngine,
                      GetMatchingOtherGlobalRanks, other_replica_id, layer_id,
                      transfer_operation_ranks_type);
  }
};
//==============================================================================
void InitTransferEnginePybindClass(py::module_& m) {
  py::class_<BaseTransferEngine, PyTransferEngine,
             std::shared_ptr<BaseTransferEngine>>(m, "BaseTransferEngine")
      .def("async_send", &BaseTransferEngine::AsyncSend,
           py::return_value_policy::take_ownership, py::arg("dst_replica_id"),
           py::arg("page_tensor"), py::arg("page_list"), py::arg("layer_id"),
           py::arg("send_to_all"))
      .def("async_recv", &BaseTransferEngine::AsyncRecv,
           py::return_value_policy::take_ownership, py::arg("src_replica_id"),
           py::arg("page_tensor"), py::arg("page_list"), py::arg("layer_id"),
           py::arg("recv_from_single_rank"))
      .def("get_matching_other_global_ranks",
           &BaseTransferEngine::GetMatchingOtherGlobalRanks,
           py::arg("other_replica_id"), py::arg("layer_id"),
           py::arg("transfer_operation_ranks_type") =
               TransferOperationRanksType::MATCHING)
      .def_static(
          "create_from",  // Expose the static factory method
          [](const TransferEngineConfig& transfer_engine_config) {
            std::shared_ptr<BaseTransferEngine> engine =
                TransferEngineFactory::Create(transfer_engine_config);
            return engine;
          },
          py::return_value_policy::take_ownership,
          py::arg("transfer_engine_config"));
}
//==============================================================================
void InitTransferWorkPybindClass(py::module_& m) {
  py::class_<BaseTransferWork, PyTransferWork,
             std::shared_ptr<BaseTransferWork>>(m, "BaseTransferWork")
      .def("synchronize", &BaseTransferWork::Synchronize);
}
//==============================================================================
void InitTransferEngineInterfacePybindSubmodule(py::module& pm) {
  auto m = pm.def_submodule("interface", "Transfer Engine Interface submodule");

  InitTransferEnginePybindClass(m);
  InitTransferWorkPybindClass(m);
}
//==============================================================================
}  // namespace vajra
//==============================================================================
