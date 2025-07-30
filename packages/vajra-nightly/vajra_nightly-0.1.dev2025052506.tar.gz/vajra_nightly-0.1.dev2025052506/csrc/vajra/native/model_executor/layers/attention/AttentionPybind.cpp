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
#include "native/model_executor/layers/attention/AttentionPybind.h"
//==============================================================================
#include "native/model_executor/layers/attention/AttentionWrapper.h"
#include "native/model_executor/layers/attention/FlashinferAttentionWrapper.h"
#include "native/model_executor/layers/attention/SequenceArrangement.h"
#include "native/model_executor/layers/attention/flashinfer/FlashinferPybind.h"
//==============================================================================
namespace vajra {
//==============================================================================
void InitFlashinferAttentionWrapperPybindClass(py::module& m) {
  py::class_<FlashinferAttentionWrapper,
             std::shared_ptr<FlashinferAttentionWrapper>>(
      m, "FlashinferAttentionWrapper")
      .def(py::init<std::size_t, std::size_t, std::size_t, std::size_t,
                    torch::Device>(),
           py::arg("num_q_heads"), py::arg("num_kv_heads"), py::arg("head_dim"),
           py::arg("block_size"), py::arg("device"))
      .def("begin_forward", &FlashinferAttentionWrapper::BeginForward)
      .def("end_forward", &FlashinferAttentionWrapper::EndForward)
      .def("run", &FlashinferAttentionWrapper::Run)
      .def("save_kv_cache", &FlashinferAttentionWrapper::SaveKVCache)
      .def("get_num_q_tokens", &FlashinferAttentionWrapper::GetNumQTokens)
      .def_property_readonly(
          "num_q_tokens",
          &FlashinferAttentionWrapper::GetNumQTokensWithoutValidation)
      .def_property_readonly("is_no_op", &FlashinferAttentionWrapper::GetIsNoOp)
      .def_property_readonly("should_save_kv_cache",
                             &FlashinferAttentionWrapper::GetShouldSaveKVCache)
      .def_property_readonly(
          "is_metadata_initialized",
          &FlashinferAttentionWrapper::GetIsMetadataInitialized)
      .def_property_readonly("slot_mapping_tensor",
                             &FlashinferAttentionWrapper::GetSlotMappingTensor);
}
//==============================================================================
void InitSequenceArrangementPybindClass(py::module& m) {
  py::class_<SequenceArrangement, std::shared_ptr<SequenceArrangement>>(
      m, "SequenceArrangement")
      .def(py::init<>())
      .def("check_arrangement_and_extend",
           &SequenceArrangement::CheckArrangementAndExtend)
      .def("get_arranged", &SequenceArrangement::GetArranged)
      .def("get_splits", &SequenceArrangement::GetSplits)
      .def("get_num_splits", &SequenceArrangement::GetNumSplits);
}
//==============================================================================
void InitAttentionWrapperPybindClass(py::module& m) {
  py::class_<AttentionWrapper, std::shared_ptr<AttentionWrapper>>(
      m, "AttentionWrapper")
      .def(py::init<std::size_t, std::size_t, std::size_t, std::size_t,
                    torch::Device, torch::ScalarType>(),
           py::arg("num_q_heads"), py::arg("num_kv_heads"), py::arg("head_dim"),
           py::arg("block_size"), py::arg("device"), py::arg("dtype"))
      .def("begin_forward", &AttentionWrapper::BeginForward)
      .def("end_forward", &AttentionWrapper::EndForward)
      .def("forward", &AttentionWrapper::Forward)
      .def_static("get_cache_block", &vajra::AttentionWrapper::GetCacheBlock)
      .def_static("initialize_static_args",
                  &vajra::AttentionWrapper::InitializeStaticArgs,
                  py::arg("num_q_heads"), py::arg("num_kv_heads"),
                  py::arg("head_dim"), py::arg("block_size"), py::arg("device"),
                  py::arg("dtype"))
      .def_static("get_or_create_thread_local_instance",
                  &vajra::AttentionWrapper::GetOrCreateThreadLocalInstance);
}
//==============================================================================
void InitAttentionPybindSubmodule(py::module& pm) {
  auto m = pm.def_submodule("attention", "Attention submodule");

  InitFlashinferAttentionWrapperPybindClass(m);
  InitSequenceArrangementPybindClass(m);
  InitAttentionWrapperPybindClass(m);
  InitFlashinferPybindSubmodule(m);
}
//==============================================================================
}  // namespace vajra
//==============================================================================
