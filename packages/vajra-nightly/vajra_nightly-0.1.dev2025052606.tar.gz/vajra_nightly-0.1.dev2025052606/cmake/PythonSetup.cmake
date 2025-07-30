if(NOT VAJRA_PYTHON_EXECUTABLE)
  message(FATAL_ERROR "Please set VAJRA_PYTHON_EXECUTABLE to the desired Python executable.")
endif()

find_python_from_executable(${VAJRA_PYTHON_EXECUTABLE} "${PYTHON_SUPPORTED_VERSIONS}")
find_package(Python REQUIRED COMPONENTS Development.Embed)

message(STATUS "Python version: ${Python_VERSION}")
message(STATUS "Python include dirs: ${Python_INCLUDE_DIRS}")

add_library(vajra_python INTERFACE)
target_include_directories(vajra_python INTERFACE ${Python_INCLUDE_DIRS})
target_link_libraries(vajra_python INTERFACE Python::Python)

# If using a conda environment, sometimes we need to explicitly add the lib path
if(DEFINED ENV{CONDA_PREFIX})
  message(STATUS "Conda environment detected: $ENV{CONDA_PREFIX}")
  target_include_directories(vajra_python INTERFACE 
    $ENV{CONDA_PREFIX}/include
    $ENV{CONDA_PREFIX}/include/python${Python_VERSION_MAJOR}.${Python_VERSION_MINOR}
  )
  target_link_directories(vajra_python INTERFACE 
    $ENV{CONDA_PREFIX}/lib
  )
endif()
