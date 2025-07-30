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
#include "native/datatypes/DatatypesPybind.h"
//==============================================================================
#include "native/engine/InferenceEngine.h"
//==============================================================================
namespace vajra {
//==============================================================================
void InitInferenceEnginePybindClass(py::module_& pm) {
  py::class_<InferenceEngine, std::shared_ptr<InferenceEngine>>(
      pm, "InferenceEngine")
      .def(py::init<const EngineMetricsStorePtr&>())
      .def("add_request",
           [](InferenceEngine& self, const std::optional<std::string>& seq_id,
              const std::string& prompt, const TokenIds& prompt_token_ids,
              const SamplingParams& sampling_params) {
             auto prompt_token_ids_shared =
                 std::make_shared<TokenIds>(prompt_token_ids);
             self.AddRequest(seq_id, prompt, prompt_token_ids_shared,
                             sampling_params);
           })
      .def("get_waiting_seq_queue", &InferenceEngine::GetWaitingSeqQueue)
      .def("get_output_queue", &InferenceEngine::GetOutputQueue)
      .def("get_outputs", [](InferenceEngine& self, const bool block) {
        // release the GIL while waiting for outputs
        py::gil_scoped_release release;
        return self.GetOutputs(block);
      });
}
//==============================================================================
void InitEnginePybindSubmodule(py::module_& pm) {
  auto m = pm.def_submodule("engine", "Engine submodule");

  InitInferenceEnginePybindClass(m);
}
//==============================================================================
}  // namespace vajra
//==============================================================================
