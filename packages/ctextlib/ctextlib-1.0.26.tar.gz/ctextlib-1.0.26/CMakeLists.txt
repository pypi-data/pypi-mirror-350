cmake_minimum_required(VERSION 3.5)
project(ctextlib)

# Set C++ standard
if(CMAKE_CXX_COMPILER_ID STREQUAL "GNU")
    set(CMAKE_CXX_STANDARD 17)
else()
    set(CMAKE_CXX_STANDARD 14)
endif()

# Use manually-specified executable if provided
if (DEFINED Python_EXECUTABLE)
    set(Python3_EXECUTABLE ${Python_EXECUTABLE})
endif()

find_package(Python3 REQUIRED COMPONENTS Interpreter Development)

# Get pybind11 cmake dir using Python
execute_process(
    COMMAND "${Python3_EXECUTABLE}" -m pybind11 --cmakedir
    OUTPUT_VARIABLE PYBIND11_CMAKE_DIR
    OUTPUT_STRIP_TRAILING_WHITESPACE
)

# Add pybind11's cmake dir to CMAKE_PREFIX_PATH
list(APPEND CMAKE_PREFIX_PATH "${PYBIND11_CMAKE_DIR}")

# Find pybind11 package
find_package(pybind11 REQUIRED)

# Include pybind11 headers
include_directories(${pybind11_INCLUDE_DIRS})

# Build the Python module (shared object or DLL)
add_library(ctextlib MODULE src/module.cpp)

# Link against pybind11
target_link_libraries(ctextlib PRIVATE pybind11::module)

# Avoid "lib" prefix (e.g., produce ctextlib.pyd or ctextlib.so, not libctextlib)
set_target_properties(ctextlib PROPERTIES PREFIX "")

# Set the correct extension for the module (pyd on Windows, so on Unix)
if(WIN32)
    set_target_properties(ctextlib PROPERTIES SUFFIX ".pyd")
else()
    set_target_properties(ctextlib PROPERTIES SUFFIX ".so")
endif()
