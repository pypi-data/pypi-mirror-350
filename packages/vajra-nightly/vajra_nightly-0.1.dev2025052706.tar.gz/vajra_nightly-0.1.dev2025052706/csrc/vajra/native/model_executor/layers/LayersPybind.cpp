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
#include "native/model_executor/layers/LayersPybind.h"
//==============================================================================
#include "native/model_executor/layers/Activation.h"
#include "native/model_executor/layers/LinearLayers.h"
#include "native/model_executor/layers/NormLayers.h"
#include "native/model_executor/layers/RotaryEmbedding.h"
#include "native/model_executor/layers/Sampler.h"
#include "native/model_executor/layers/attention/AttentionPybind.h"
//==============================================================================
namespace vajra {
//==============================================================================
void InitColumnParallelLinearPybindClass(py::module_& m) {
  py::class_<ColumnParallelLinear, std::shared_ptr<ColumnParallelLinear>>(
      m, "ColumnParallelLinear")
      .def(py::init<int, int, bool, int, bool, torch::Tensor,
                    std::optional<torch::Tensor>, ProcessGroupWrapperPtr>())
      .def("forward", &ColumnParallelLinear::Forward);
}
//==============================================================================
void InitRowParallelLinearPybindClass(py::module_& m) {
  py::class_<RowParallelLinear, std::shared_ptr<RowParallelLinear>>(
      m, "RowParallelLinear")
      .def(py::init<int, int, bool, bool, int, int, bool, torch::Tensor,
                    std::optional<torch::Tensor>, ProcessGroupWrapperPtr>())
      .def("forward", &RowParallelLinear::Forward);
}
//==============================================================================
void InitVocabParallelEmbeddingPybindClass(py::module_& m) {
  py::class_<VocabParallelEmbedding, std::shared_ptr<VocabParallelEmbedding>>(
      m, "VocabParallelEmbedding")
      .def(py::init<int, int, int, int, bool, int, int, int, torch::Tensor,
                    ProcessGroupWrapperPtr>())
      .def("forward", &VocabParallelEmbedding::Forward);
}
//==============================================================================
void InitRMSNormPybindClass(py::module_& m) {
  py::class_<RMSNorm, std::shared_ptr<RMSNorm>>(m, "RMSNorm")
      .def(py::init<torch::Tensor, double>())
      .def("forward", &RMSNorm::Forward);
}
//==============================================================================
void InitRotaryEmbeddingPybindClass(py::module_& m) {
  py::class_<RotaryEmbedding, std::shared_ptr<RotaryEmbedding>>(
      m, "RotaryEmbedding")
      .def(py::init<int, int, int64_t, int64_t, bool, torch::Tensor>())
      .def("forward", &RotaryEmbedding::Forward);
}
//==============================================================================
void InitSamplerPybindClass(py::module_& m) {
  py::class_<Sampler, std::shared_ptr<Sampler>>(m, "Sampler")
      .def(py::init<torch::Tensor, int, ProcessGroupWrapperPtr>())
      .def("forward", &Sampler::Forward)
      .def("__call__", &Sampler::Forward);
}
//==============================================================================
void InitSiluAndMulPybindClass(py::module_& m) {
  py::class_<SiluAndMul, std::shared_ptr<SiluAndMul>>(m, "SiluAndMul")
      .def(py::init<>())
      .def_static("forward", &SiluAndMul::Forward)
      .def("__call__", &SiluAndMul::operator());
}
//==============================================================================
void InitNewGELUPybindClass(py::module_& m) {
  py::class_<NewGELU, std::shared_ptr<NewGELU>>(m, "NewGELU")
      .def(py::init<>())
      .def_static("forward", &NewGELU::Forward)
      .def("__call__", &NewGELU::operator());
}
//==============================================================================
void InitFastGELUPybindClass(py::module_& m) {
  py::class_<FastGELU, std::shared_ptr<FastGELU>>(m, "FastGELU")
      .def(py::init<>())
      .def_static("forward", &FastGELU::Forward)
      .def("__call__", &FastGELU::operator());
}
//==============================================================================
void InitLayersPybindSubmodule(py::module& pm) {
  auto m = pm.def_submodule("layers", "Layers submodule");

  InitColumnParallelLinearPybindClass(m);
  InitRowParallelLinearPybindClass(m);
  InitVocabParallelEmbeddingPybindClass(m);
  InitRMSNormPybindClass(m);
  InitRotaryEmbeddingPybindClass(m);
  InitSamplerPybindClass(m);
  InitSiluAndMulPybindClass(m);
  InitNewGELUPybindClass(m);
  InitFastGELUPybindClass(m);

  InitAttentionPybindSubmodule(m);
}
//==============================================================================
}  // namespace vajra
//==============================================================================
