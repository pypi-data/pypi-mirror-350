cmake_minimum_required(VERSION 3.15...3.26)
project(markov_cpp VERSION 0.1.0 LANGUAGES CXX)

# Set C++ standard
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Find Python
find_package(Python 3.10 REQUIRED COMPONENTS Interpreter Development.Module)

# Add nanobind as a dependency
include(FetchContent)
FetchContent_Declare(
  nanobind
  GIT_REPOSITORY https://github.com/wjakob/nanobind.git
  GIT_TAG v2.7.0  # Use the latest stable release version
)
FetchContent_MakeAvailable(nanobind)

# Create the nanobind module
nanobind_add_module(
  cpp_markov_algorithms
  src/markov/algorithms.cpp
)

# Include directories
# target_include_directories(cpp_markov_algorithms PRIVATE
#   ${CMAKE_CURRENT_SOURCE_DIR}/include
# )

# Set compiler flags
if(MSVC)
  target_compile_options(cpp_markov_algorithms PRIVATE /W4 /EHsc)
else()
  target_compile_options(cpp_markov_algorithms PRIVATE -Wall -Wextra -O3)
endif()

# Installation configuration
install(TARGETS cpp_markov_algorithms DESTINATION .)
