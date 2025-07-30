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
#include "native/core/tokenizer/TokenizerPybind.h"
//==============================================================================
#include "commons/TorchCommon.h"
#include "native/core/tokenizer/Tokenizer.h"
#include "native/core/tokenizer/TokenizerPool.h"
//==============================================================================
namespace vajra {
//==============================================================================
void InitTokenizerPybindClass(py::module_& m) {
  py::class_<Tokenizer, std::shared_ptr<Tokenizer>>(m, "Tokenizer")
      .def_static("from_path", &Tokenizer::FromPath)
      .def("encode", &Tokenizer::Encode)
      .def("decode", &Tokenizer::Decode)
      .def("partial_decode", &Tokenizer::PartialDecode);
}
//==============================================================================
void InitTokenizerPybindSubmodule(py::module& pm) {
  auto m = pm.def_submodule("tokenizer", "Tokenizer submodule");
  InitTokenizerPybindClass(m);

  py::class_<vajra::TokenizerPoolInput>(m, "TokenizerPoolInput")
      .def(
          py::init<std::string&, double, std::string&, vajra::SamplingParams>(),
          py::arg("seq_id"), py::arg("arrival_time"), py::arg("prompt"),
          py::arg("sampling_params"))
      .def_readonly("seq_id", &vajra::TokenizerPoolInput::seq_id)
      .def_readonly("arrival_time", &vajra::TokenizerPoolInput::arrival_time)
      .def_readonly("prompt", &vajra::TokenizerPoolInput::prompt)
      .def_readonly("sampling_params",
                    &vajra::TokenizerPoolInput::sampling_params);

  py::class_<vajra::TokenizerPoolOutput>(m, "TokenizerPoolOutput")
      .def(py::init([](std::string& seq_id, TimeS arrival_time,
                       std::string& prompt, TokenIds& token_ids,
                       vajra::SamplingParams sampling_params) {
             return vajra::TokenizerPoolOutput(
                 seq_id, arrival_time, prompt,
                 std::make_shared<TokenIds>(token_ids), sampling_params);
           }),
           py::arg("seq_id"), py::arg("arrival_time"), py::arg("prompt"),
           py::arg("token_ids"), py::arg("sampling_params"))
      .def_readonly("seq_id", &vajra::TokenizerPoolOutput::seq_id)
      .def_readonly("arrival_time", &vajra::TokenizerPoolOutput::arrival_time)
      .def_readonly("prompt", &vajra::TokenizerPoolOutput::prompt)
      .def_property_readonly("token_ids",
                             [](const vajra::TokenizerPoolOutput& self) {
                               return self.token_ids ? *(self.token_ids)
                                                     : std::vector<TokenId>();
                             })
      .def_readonly("sampling_params",
                    &vajra::TokenizerPoolOutput::sampling_params);

  py::class_<vajra::TokenizerPool>(m, "TokenizerPool")
      .def(py::init<std::string&, std::size_t>(), py::arg("tokenizer_path"),
           py::arg("num_workers"))
      .def("start", &vajra::TokenizerPool::Start)
      .def("shutdown", &vajra::TokenizerPool::Shutdown)
      .def("add_request", &vajra::TokenizerPool::AddRequest)
      .def("add_output", &vajra::TokenizerPool::AddOutput)
      .def("get_output", &vajra::TokenizerPool::GetOutput,
           py::call_guard<py::gil_scoped_release>());
}
//==============================================================================
}  // namespace vajra
//==============================================================================
