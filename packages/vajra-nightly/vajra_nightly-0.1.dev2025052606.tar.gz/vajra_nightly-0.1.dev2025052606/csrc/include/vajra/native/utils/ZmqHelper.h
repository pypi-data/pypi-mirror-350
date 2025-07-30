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
#include <google/protobuf/io/coded_stream.h>
#include <google/protobuf/io/zero_copy_stream_impl_lite.h>
//==============================================================================
#include <zmq.hpp>
//==============================================================================
#include "commons/ClassTraits.h"
#include "commons/Logging.h"
#include "commons/StdCommon.h"
#include "native/utils/ProtoUtils.h"
//==============================================================================
namespace vajra {
//==============================================================================
class ZmqHelper : public NonCopyableNonMovable {
 public:
  /**
   * @brief Send a vajra object over ZMQ socket by converting it to protobuf
   * first
   *
   * @tparam T The vajra type to send
   * @param socket The ZMQ socket to send over
   * @param obj The vajra object to send
   */
  template <typename T>
  static void Send(zmq::socket_t& socket, const T& obj) {
    // Convert vajra object to protobuf
    auto proto = ProtoUtils::ToProto(obj);

    // Send the protobuf object
    SendProto(socket, proto);
  }

  /**
   * @brief Receive a vajra object over ZMQ socket by converting from protobuf
   *
   * @tparam T The vajra type to receive
   * @param socket The ZMQ socket to receive from
   * @return T The received vajra object
   */
  template <typename T>
  [[nodiscard]] static T Recv(zmq::socket_t& socket) {
    // Determine the corresponding protobuf type for T
    using ProtoType = typename CorrespondingProtoType<T>::type;

    // Receive the protobuf object
    auto proto = RecvProto<ProtoType>(socket);

    // Convert protobuf to vajra object
    return ProtoUtils::FromProto<T>(proto);
  }

 private:
  /**
   * @brief Send a protobuf object over ZMQ socket
   *
   * @tparam ProtoType The protobuf type to send
   * @param socket The ZMQ socket to send over
   * @param proto The protobuf object to send
   */
  template <typename ProtoType>
  static void SendProto(zmq::socket_t& socket, const ProtoType& proto) {
    std::string serialized_data;
    proto.SerializeToString(&serialized_data);

    ASSERT_VALID_RUNTIME(socket.send(zmq::buffer(serialized_data)),
                         "Failed to send protobuf message");
  }

  /**
   * @brief Receive a protobuf object over ZMQ socket
   *
   * @tparam ProtoType The protobuf type to receive
   * @param socket The ZMQ socket to receive from
   * @return ProtoType The received protobuf object
   */
  template <typename ProtoType>
  [[nodiscard]] static ProtoType RecvProto(zmq::socket_t& socket) {
    zmq::message_t message;
    ASSERT_VALID_RUNTIME(socket.recv(message),
                         "Failed to receive protobuf message");

    ProtoType proto;
    std::string message_str(static_cast<char*>(message.data()), message.size());

    ASSERT_VALID_RUNTIME(proto.ParseFromString(message_str),
                         "Failed to parse protobuf message");

    return proto;
  }
};
//==============================================================================
using ZmqSocketPtr = std::shared_ptr<zmq::socket_t>;
using ZmqContextPtr = std::shared_ptr<zmq::context_t>;
//==============================================================================
}  // namespace vajra
//==============================================================================
