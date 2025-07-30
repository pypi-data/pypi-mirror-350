# Define common interface library for all targets
add_library(vajra_common INTERFACE)
target_include_directories(vajra_common INTERFACE
  ${CMAKE_CURRENT_SOURCE_DIR}/csrc/include/vajra
  ${CMAKE_CURRENT_SOURCE_DIR}/csrc/third_party/ddsketch/include
  ${CMAKE_CURRENT_SOURCE_DIR}/csrc/third_party/flashinfer/include
  ${VIDUR_INCLUDE_DIR}
  ${cppzmq_SOURCE_DIR}
  ${CMAKE_CURRENT_BINARY_DIR}
)
target_link_libraries(vajra_common INTERFACE
  ${TORCH_LIBRARIES}
  tokenizers_cpp
  glog::glog
  nlohmann_json::nlohmann_json
  Vidur::Vidur
  Flashinfer::Flashinfer
  Boost::thread
  Boost::uuid
  libzmq-static
  proto_lib
  vajra_python
)

add_dependencies(vajra_common proto_lib)

# Function to configure common target properties
function(vajra_target_config TARGET_NAME IS_MODULE)
  target_link_libraries(${TARGET_NAME} PRIVATE vajra_common)
  if(NOT ${IS_MODULE})
    set_target_properties(${TARGET_NAME} PROPERTIES POSITION_INDEPENDENT_CODE ON)
  endif()
  if(VAJRA_GPU_ARCHES)
    set_target_properties(${TARGET_NAME} PROPERTIES ${VAJRA_GPU_LANG}_ARCHITECTURES "${VAJRA_GPU_ARCHES}")
  endif()
  target_compile_options(${TARGET_NAME} PRIVATE $<$<COMPILE_LANGUAGE:${VAJRA_GPU_LANG}>:${VAJRA_GPU_FLAGS} -fPIC> $<$<COMPILE_LANGUAGE:CXX>:-Werror>)
  target_compile_definitions(${TARGET_NAME} PRIVATE "-DTORCH_EXTENSION_NAME=${TARGET_NAME}")
endfunction()

# Function to define Python extension modules
function(define_vajra_extension NAME SOURCES LIBS)
  Python_add_library(${NAME} MODULE "${SOURCES}" WITH_SOABI)
  target_link_libraries(${NAME} PRIVATE ${LIBS})
  vajra_target_config(${NAME} TRUE)
endfunction()

# Function to define static libraries
function(define_vajra_static NAME SOURCES LIBS)
  add_library(${NAME} STATIC ${SOURCES})
  target_link_libraries(${NAME} PRIVATE ${LIBS})
  vajra_target_config(${NAME} FALSE)
endfunction()

# Define specific targets
file(GLOB_RECURSE COMMON_SRC "csrc/vajra/commons/*.cpp")

file(GLOB_RECURSE KERNEL_COMMON_SRC "csrc/vajra/kernels/*.cu")
define_vajra_static(_kernels_common "${KERNEL_COMMON_SRC};${COMMON_SRC}" "")

file(GLOB_RECURSE KERNELS_SRC "csrc/vajra/kernels/*.cpp")
define_vajra_extension(_kernels "${KERNELS_SRC};${COMMON_SRC}" "_kernels_common")
define_vajra_static(_kernels_static "${KERNELS_SRC};${COMMON_SRC}" "_kernels_common")

file(GLOB_RECURSE NATIVE_SRC "csrc/vajra/native/**/*.cpp")
define_vajra_extension(_native "${NATIVE_SRC};${COMMON_SRC};csrc/vajra/native/pybind.cpp" "_kernels_common")
define_vajra_static(_native_static "${NATIVE_SRC};${COMMON_SRC}" "_kernels_common")
