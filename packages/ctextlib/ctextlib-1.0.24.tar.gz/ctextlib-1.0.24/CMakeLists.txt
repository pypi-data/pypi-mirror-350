cmake_minimum_required(VERSION 3.5)
project(ctextlib)

# find_package(pybind11 REQUIRED)

if(CMAKE_CXX_COMPILER_ID STREQUAL "GNU")
   set(CMAKE_CXX_STANDARD 17)
else()
   set(CMAKE_CXX_STANDARD 14)
endif()

add_subdirectory(pybind11)

list(APPEND CMAKE_PREFIX_PATH "${CMAKE_BINARY_DIR}")
# find_package(pybind11 REQUIRED)
pybind11_add_module(ctextlib src/module.cpp)
