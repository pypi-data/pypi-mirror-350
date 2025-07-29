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
#include "commons/Logging.h"
#include "native/utils/NetworkUtils.h"
//==============================================================================
namespace vajra {
//==============================================================================
struct CommInfo final {
  CommInfo(const std::string& driver_ip) : driver_ip(driver_ip) {
    auto ports = GetRandomPorts(4);
    distributed_init_method = std::format("tcp://{}:{}", driver_ip, ports[0]);
    engine_ip_address = GetLocalIpAddress();
    enqueue_socket_port = ports[1];
    output_socket_port = ports[2];
    microbatch_socket_port = ports[3];
  }

  CommInfo(const std::string& distributed_init_method,
           const std::string& engine_ip_address,
           std::size_t enqueue_socket_port, std::size_t output_socket_port,
           std::size_t microbatch_socket_port)
      : distributed_init_method(distributed_init_method),
        engine_ip_address(engine_ip_address),
        enqueue_socket_port(enqueue_socket_port),
        output_socket_port(output_socket_port),
        microbatch_socket_port(microbatch_socket_port) {}

  /// @brief Convert to string representation
  /// @return String representation of the CommInfo
  [[nodiscard]] std::string ToString() const {
    return std::format(
        "CommInfo(distributed_init_method={}, engine_ip_address={}, "
        "enqueue_socket_port={}, output_socket_port={}, "
        "microbatch_socket_port={})",
        distributed_init_method, engine_ip_address, enqueue_socket_port,
        output_socket_port, microbatch_socket_port);
  }

  const std::string driver_ip;
  std::string distributed_init_method;
  std::string engine_ip_address;
  std::size_t enqueue_socket_port;
  std::size_t output_socket_port;
  std::size_t microbatch_socket_port;
};
//==============================================================================
using CommInfoPtr = std::shared_ptr<const CommInfo>;
//==============================================================================
}  // namespace vajra
//==============================================================================
