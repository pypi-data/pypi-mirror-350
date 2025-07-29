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
#include "native/utils/UtilsPybind.h"
//==============================================================================
#include "native/datatypes/StepInputs.h"
#include "native/datatypes/StepMicrobatchOutputs.h"
#include "native/datatypes/StepOutputs.h"
#include "native/enums/Enums.h"
#include "native/utils/ZmqHelper.h"
//==============================================================================
namespace vajra {
//==============================================================================
void InitZmqHelperPybindClass(py::module_& m) {
  // We need to create specific instantiations for the Python bindings
  // since ZmqHelper uses templates
  py::class_<zmq::socket_t, ZmqSocketPtr>(m, "ZmqSocket", py::module_local())
      .def(py::init<zmq::context_t&, int>(), py::arg("context"),
           py::arg("type"))
      .def("bind",
           static_cast<void (zmq::socket_t::*)(const std::string&)>(
               &zmq::socket_t::bind),
           py::arg("endpoint"), "Bind the socket to an endpoint")
      .def("connect",
           static_cast<void (zmq::socket_t::*)(const std::string&)>(
               &zmq::socket_t::connect),
           py::arg("endpoint"), "Connect the socket to an endpoint")
      .def(
          "setsockopt_string",
          [](zmq::socket_t& socket, int option, const std::string& value) {
// Revert to using setsockopt with a compiler warning suppression
// This is a temporary solution until we can properly update to the newer ZMQ
// API
#pragma GCC diagnostic push
#pragma GCC diagnostic ignored "-Wdeprecated-declarations"
            socket.setsockopt(option, value.c_str(), value.size());
#pragma GCC diagnostic pop
          },
          py::arg("option"), py::arg("value"),
          "Set a socket option with a string value");

  py::class_<zmq::context_t, ZmqContextPtr>(m, "ZmqContext", py::module_local())
      .def(py::init<>());

  // Create a wrapper module for ZmqHelper
  auto zmq_helper = m.def_submodule("zmq_helper", "ZMQ Helper functions");

  // Expose the Send and Recv methods for specific types
  zmq_helper.def(
      "send_step_inputs",
      [](zmq::socket_t& socket, const StepInputs& inputs) {
        ZmqHelper::Send(socket, inputs);
      },
      py::arg("socket"), py::arg("inputs"),
      "Send StepInputs over a ZMQ socket");

  zmq_helper.def(
      "recv_step_inputs",
      [](zmq::socket_t& socket) {
        // Release the GIL during the blocking receive operation
        py::gil_scoped_release release;
        return ZmqHelper::Recv<StepInputs>(socket);
      },
      py::arg("socket"), "Receive StepInputs from a ZMQ socket");

  zmq_helper.def(
      "send_step_outputs",
      [](zmq::socket_t& socket, const StepOutputs& outputs) {
        ZmqHelper::Send(socket, outputs);
      },
      py::arg("socket"), py::arg("outputs"),
      "Send StepOutputs over a ZMQ socket");

  zmq_helper.def(
      "recv_step_outputs",
      [](zmq::socket_t& socket) {
        // Release the GIL during the blocking receive operation
        py::gil_scoped_release release;
        return ZmqHelper::Recv<StepOutputs>(socket);
      },
      py::arg("socket"), "Receive StepOutputs from a ZMQ socket");

  zmq_helper.def(
      "send_step_microbatch_outputs",
      [](zmq::socket_t& socket, const StepMicrobatchOutputs& outputs) {
        ZmqHelper::Send(socket, outputs);
      },
      py::arg("socket"), py::arg("outputs"),
      "Send StepMicrobatchOutputs over a ZMQ socket");

  zmq_helper.def(
      "recv_step_microbatch_outputs",
      [](zmq::socket_t& socket) {
        // Release the GIL during the blocking receive operation
        py::gil_scoped_release release;
        return ZmqHelper::Recv<StepMicrobatchOutputs>(socket);
      },
      py::arg("socket"), "Receive StepMicrobatchOutputs from a ZMQ socket");
}
//==============================================================================
void InitUtilsPybindSubmodule(py::module_& pm) {
  auto m = pm.def_submodule("utils", "Utils submodule");

  // Expose the C++ clock function
  m.def("now_s", &time_utils::now_s,
        "Get current time in seconds using C++ clock");

  InitZmqHelperPybindClass(m);
}
//==============================================================================
}  // namespace vajra
//==============================================================================
