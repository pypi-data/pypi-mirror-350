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
#include "native/model_executor/layers/attention/flashinfer/FlashinferPybind.h"
//==============================================================================
#include "native/model_executor/layers/attention/flashinfer/BatchPrefillWithPagedKVCacheWrapper.h"
//==============================================================================
namespace vajra {
//==============================================================================
void InitBatchPrefillWithPagedKVCacheWrapperPybindClass(py::module& m) {
  py::class_<flashinfer::BatchPrefillWithPagedKVCacheWrapper,
             std::shared_ptr<flashinfer::BatchPrefillWithPagedKVCacheWrapper>>(
      m, "BatchPrefillWithPagedKVCacheWrapper")
      .def(py::init<torch::Tensor, std::string, std::string>(),
           py::arg("float_workspace_buffer"), py::arg("kv_layout") = "NHD",
           py::arg("backend") = "auto")
      .def("plan", &flashinfer::BatchPrefillWithPagedKVCacheWrapper::Plan,
           py::arg("qo_indptr"), py::arg("paged_kv_indptr"),
           py::arg("paged_kv_indices"), py::arg("paged_kv_last_page_len"),
           py::arg("num_qo_heads"), py::arg("num_kv_heads"),
           py::arg("head_dim_qk"), py::arg("page_size"),
           py::arg("non_blocking") = false, py::arg("causal") = true,
           py::arg("head_dim_vo") = std::nullopt,
           py::arg("custom_mask") = std::nullopt,
           py::arg("packed_custom_mask") = std::nullopt,
           py::arg("pos_encoding_mode") = "NONE",
           py::arg("use_fp16_qk_reduction") = false,
           py::arg("sm_scale") = std::nullopt, py::arg("window_left") = -1,
           py::arg("logits_soft_cap") = std::nullopt,
           py::arg("rope_scale") = std::nullopt,
           py::arg("rope_theta") = std::nullopt,
           py::arg("q_data_type") = "float16",
           py::arg("kv_data_type") = std::nullopt)
      .def("run", &flashinfer::BatchPrefillWithPagedKVCacheWrapper::Run,
           py::arg("q"), py::arg("paged_kv_cache"),
           py::arg("k_scale") = std::nullopt, py::arg("v_scale") = std::nullopt,
           py::arg("out") = std::nullopt, py::arg("lse") = std::nullopt,
           py::arg("return_lse") = false);
}
//==============================================================================
void InitFlashinferPybindSubmodule(py::module& pm) {
  auto m = pm.def_submodule("flashinfer", "Flashinfer submodule");

  InitBatchPrefillWithPagedKVCacheWrapperPybindClass(m);
}
//==============================================================================
}  // namespace vajra
//==============================================================================
