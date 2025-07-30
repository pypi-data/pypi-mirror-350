# Define common interface library for tests
add_library(vajra_test_common INTERFACE)
target_include_directories(vajra_test_common INTERFACE
  ${CMAKE_CURRENT_SOURCE_DIR}/csrc/include/vajra
  ${VIDUR_INCLUDE_DIR}
)
target_link_libraries(vajra_test_common INTERFACE
  vajra_common
  gtest
  gtest_main  
)

# Function to configure common test target properties
function(vajra_test_config TARGET_NAME)
  target_link_libraries(${TARGET_NAME} PRIVATE vajra_test_common)
  target_compile_options(${TARGET_NAME} PRIVATE $<$<COMPILE_LANGUAGE:${VAJRA_GPU_LANG}>:${VAJRA_GPU_FLAGS} -fPIC>)
  if(VAJRA_GPU_ARCHES)
    set_target_properties(${TARGET_NAME} PROPERTIES ${VAJRA_GPU_LANG}_ARCHITECTURES "${VAJRA_GPU_ARCHES}")
  endif()
endfunction()

# Function to add test suites
function(add_vajra_test_suite NAME SOURCE_DIR LIBS)
  file(GLOB_RECURSE CPP_TEST_SRC "${SOURCE_DIR}/*.cpp")
  file(GLOB_RECURSE CUDA_TEST_SRC "${SOURCE_DIR}/*.cu")
  set(ALL_TEST_SRC ${CPP_TEST_SRC} ${CUDA_TEST_SRC})
  if(ALL_TEST_SRC)
    add_executable(${NAME}_tests ${ALL_TEST_SRC})
    vajra_test_config(${NAME}_tests)
    target_link_libraries(${NAME}_tests PRIVATE ${LIBS})
    if(CUDA_TEST_SRC)
      set_source_files_properties(${CUDA_TEST_SRC} PROPERTIES LANGUAGE CUDA)
      target_compile_options(${NAME}_tests PRIVATE $<$<COMPILE_LANGUAGE:${VAJRA_GPU_LANG}>:${VAJRA_GPU_FLAGS} -fPIC> $<$<COMPILE_LANGUAGE:CXX>:-Werror>)
      if(VAJRA_GPU_ARCHES)
        set_target_properties(${NAME}_tests PROPERTIES ${VAJRA_GPU_LANG}_ARCHITECTURES "${VAJRA_GPU_ARCHES}")
      endif()
    endif()
    add_test(NAME ${NAME}_tests COMMAND ${NAME}_tests --gtest_output=xml:test_reports/${NAME}_tests_results.xml)
  endif()
endfunction()

# Add test suites
add_vajra_test_suite(kernel "csrc/test/kernels" "_kernels_static")
add_vajra_test_suite(native "csrc/test/native" "_native_static" "_kernels_static")

set(TESTDATA_DIR ${CMAKE_CURRENT_SOURCE_DIR}/csrc/test/testdata)
add_custom_target(
  copy_testdata
  COMMAND ${CMAKE_COMMAND} -E copy_directory
  ${TESTDATA_DIR}
  ${CMAKE_CURRENT_BINARY_DIR}/testdata
)

# Define all_tests target
add_custom_target(all_tests DEPENDS default kernel_tests native_tests copy_testdata)


