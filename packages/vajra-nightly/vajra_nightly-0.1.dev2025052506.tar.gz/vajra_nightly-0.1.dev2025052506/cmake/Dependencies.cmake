include(FetchContent)

FetchContent_Declare(
  googletest
  URL https://github.com/google/googletest/archive/refs/tags/v1.13.0.tar.gz
)

FetchContent_Declare(
  glog
  URL https://github.com/google/glog/archive/refs/tags/v0.6.0.tar.gz
)

FetchContent_Declare(
  json
  URL https://github.com/nlohmann/json/releases/download/v3.11.3/json.tar.xz
)

FetchContent_Declare(
  tokenizers_cpp
  GIT_REPOSITORY https://github.com/project-vajra/tokenizers-cpp.git
  GIT_TAG main
)

FetchContent_Declare(
  Boost
  GIT_REPOSITORY https://github.com/boostorg/boost.git
  GIT_TAG        boost-1.78.0  # Replace with your desired Boost version
)

FetchContent_Declare(
  zmq
  GIT_REPOSITORY https://github.com/zeromq/libzmq.git
  GIT_TAG        v4.3.4
)

FetchContent_Declare(
    cppzmq
    GIT_REPOSITORY https://github.com/zeromq/cppzmq.git
    GIT_TAG        v4.10.0
)

set(ZMQ_BUILD_TESTS OFF CACHE BOOL "Build ZeroMQ tests" FORCE)
set(ZMQ_BUILD_DRAFT_API OFF CACHE BOOL "Build ZeroMQ draft API" FORCE)

# Find Vidur package
list(APPEND CMAKE_MODULE_PATH "${CMAKE_CURRENT_SOURCE_DIR}/cmake")
find_package(Vidur REQUIRED)

FetchContent_Declare(
  protobuf
  GIT_REPOSITORY https://github.com/protocolbuffers/protobuf.git
  GIT_TAG        v5.29.4  # Replace with the desired version
)

set(protobuf_BUILD_TESTS OFF CACHE BOOL "Build tests" FORCE)
set(protobuf_BUILD_EXAMPLES OFF CACHE BOOL "Build examples" FORCE)
set(protobuf_BUILD_PROTOC ON CACHE BOOL "Build protoc compiler" FORCE)

FetchContent_MakeAvailable(googletest glog json tokenizers_cpp Boost zmq cppzmq protobuf)