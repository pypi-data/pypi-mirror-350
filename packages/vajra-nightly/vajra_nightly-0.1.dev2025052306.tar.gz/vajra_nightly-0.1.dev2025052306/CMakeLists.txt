########################################################################################################################################################
###
### Copyright (C) 2025 by Georgia Institute of Technology
###
### This file is part of the vajra project.
###
########################################################################################################################################################
### @file                       CMakeLists.txt
### @author                     Vajra Team <agawalamey12@gmail.com>
### @date                       25th Jan 2025
########################################################################################################################################################
cmake_minimum_required(VERSION 3.22)
set(CMAKE_POLICY_VERSION_MINIMUM 3.22)
project(vajra_extensions LANGUAGES CXX CUDA)
cmake_policy(SET CMP0077 NEW)
########################################################################################################################################################
# Set C++ standard and compiler flags
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_FLAGS "-Wall -Wextra")
set(CMAKE_CXX_FLAGS_RELEASE "-g -O3")
set(BUILD_SHARED_LIBS OFF)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)
# Need to add these to get tokenizers_cpp to link properly
set(CMAKE_POSITION_INDEPENDENT_CODE ON)
add_definitions(-D_GLIBCXX_USE_CXX11_ABI=0)
########################################################################################################################################################
# Define supported versions
set(PYTHON_SUPPORTED_VERSIONS "3.12")
set(CUDA_SUPPORTED_ARCHS "7.0;7.5;8.0;8.6;8.9;9.0")
set(TORCH_SUPPORTED_VERSION_CUDA "2.6")
########################################################################################################################################################
# Include utility functions and modular files
include(cmake/Utils.cmake)
include(cmake/Protobuf.cmake)
include(cmake/Dependencies.cmake)
include(cmake/PythonSetup.cmake)
include(cmake/TorchSetup.cmake)
include(cmake/FlashinferSetup.cmake)
include(cmake/Extensions.cmake)
include(cmake/Testing.cmake)
########################################################################################################################################################
# Define default target
add_custom_target(default DEPENDS _kernels _native _kernels_static _native_static)
########################################################################################################################################################
# Enable testing
enable_testing()
########################################################################################################################################################
