# Set the directory for generated files
set(PROTO_GEN_DIR ${CMAKE_CURRENT_BINARY_DIR}/generated)
file(MAKE_DIRECTORY ${PROTO_GEN_DIR})

# Use the protoc compiler that was just built
set(PROTOC_PATH ${CMAKE_CURRENT_BINARY_DIR}/_deps/protobuf-build/protoc)

# Gather all .proto files
file(GLOB PROTO_FILES "${CMAKE_CURRENT_SOURCE_DIR}/proto/*.proto")

# Generate C++ sources and headers for each .proto file
set(PROTO_GEN_SOURCES "")
foreach(PROTO_FILE ${PROTO_FILES})
  get_filename_component(PROTO_NAME ${PROTO_FILE} NAME_WE)
  set(PROTO_GEN_SRCS ${PROTO_GEN_DIR}/${PROTO_NAME}.pb.cc)
  set(PROTO_GEN_HDRS ${PROTO_GEN_DIR}/${PROTO_NAME}.pb.h)
  
  add_custom_command(
    OUTPUT ${PROTO_GEN_SRCS} ${PROTO_GEN_HDRS}
    COMMAND ${PROTOC_PATH} 
            --cpp_out=${PROTO_GEN_DIR} 
            --proto_path=${CMAKE_CURRENT_SOURCE_DIR}/proto 
            ${PROTO_FILE}
    DEPENDS ${PROTO_FILE} protoc
    COMMENT "Generating protobuf files for ${PROTO_NAME}"
  )
  
  list(APPEND PROTO_GEN_SOURCES ${PROTO_GEN_SRCS})
endforeach()

# Create a library for the generated protobuf code
add_library(proto_lib STATIC ${PROTO_GEN_SOURCES})
target_include_directories(proto_lib PUBLIC 
  ${PROTO_GEN_DIR}
  ${CMAKE_CURRENT_BINARY_DIR}/_deps/protobuf-src/src
)
target_link_libraries(proto_lib PUBLIC libprotobuf)
