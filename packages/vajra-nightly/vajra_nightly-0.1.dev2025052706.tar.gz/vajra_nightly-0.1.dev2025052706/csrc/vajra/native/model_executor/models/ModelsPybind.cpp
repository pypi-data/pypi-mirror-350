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
#include "native/model_executor/models/ModelsPybind.h"
//==============================================================================
#include "native/model_executor/models/Llama.h"
//==============================================================================
namespace vajra {
//==============================================================================
// Trampoline class for BaseModel
class PyBaseModel : public BaseModel {
 public:
  torch::Tensor Forward(const torch::Tensor& positions /*[in]*/,
                        torch::Tensor& hidden_states /*[inout]*/,
                        std::vector<torch::Tensor>& kv_caches /*[inout]*/
  ) const override {
    PYBIND11_OVERRIDE_PURE_NAME(torch::Tensor,  // Return type
                                BaseModel,      // Parent class
                                "forward",      // Name of function in Python
                                Forward,        // Name of function in C++
                                positions,      // Arguments
                                hidden_states, kv_caches  // Arguments
    );
  }
};
//==============================================================================
void InitLlamaMLPPybindClass(py::module_& m) {
  py::class_<LlamaMLP, std::shared_ptr<LlamaMLP>>(m, "LlamaMLP")
      .def(py::init<std::size_t, ColumnParallelLinearPtr,
                    RowParallelLinearPtr>())
      .def("forward", &LlamaMLP::Forward);
}
//==============================================================================
void InitLlamaAttentionPybindClass(py::module_& m) {
  py::class_<LlamaAttention, std::shared_ptr<LlamaAttention>>(m,
                                                              "LlamaAttention")
      .def(py::init<int, int, float, std::size_t, ColumnParallelLinearPtr,
                    RowParallelLinearPtr, RotaryEmbeddingPtr>())
      .def("forward", &LlamaAttention::Forward);
}
//==============================================================================
void InitLlamaDecoderLayerPybindClass(py::module_& m) {
  py::class_<LlamaDecoderLayer, std::shared_ptr<LlamaDecoderLayer>>(
      m, "LlamaDecoderLayer")
      .def(py::init<std::size_t, LlamaAttentionPtr, LlamaMLPPtr, RMSNormPtr,
                    RMSNormPtr>())
      .def("forward", &LlamaDecoderLayer::Forward);
}
//==============================================================================
void InitBaseModelPybindClass(py::module_& m) {
  py::class_<BaseModel, PyBaseModel, std::shared_ptr<BaseModel>>(m, "BaseModel")
      .def("forward", &BaseModel::Forward);
}
//==============================================================================
void InitLlamaModelPybindClass(py::module_& m) {
  py::class_<LlamaModel, BaseModel, std::shared_ptr<LlamaModel>>(m,
                                                                 "LlamaModel")
      .def(py::init<VocabParallelEmbeddingPtr,
                    std::vector<LlamaDecoderLayerPtr>, RMSNormPtr>())
      .def("forward", &LlamaModel::Forward);
}
//==============================================================================
void InitLlamaPybindSubmodule(py::module& pm) {
  auto m = pm.def_submodule("llama", "Llama submodule");

  InitLlamaMLPPybindClass(m);
  InitLlamaAttentionPybindClass(m);
  InitLlamaDecoderLayerPybindClass(m);
  InitBaseModelPybindClass(m);
  InitLlamaModelPybindClass(m);
}
//==============================================================================
void InitModelsPybindSubmodule(py::module& pm) {
  auto m = pm.def_submodule("models", "Models submodule");

  InitLlamaPybindSubmodule(m);
}
//==============================================================================
}  // namespace vajra
//==============================================================================
