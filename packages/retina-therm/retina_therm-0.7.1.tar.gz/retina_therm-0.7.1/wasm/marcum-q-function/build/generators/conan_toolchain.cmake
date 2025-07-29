

# Conan automatically generated toolchain file
# DO NOT EDIT MANUALLY, it will be overwritten

# Avoid including toolchain file several times (bad if appending to variables like
#   CMAKE_CXX_FLAGS. See https://github.com/android/ndk/issues/323
include_guard()

message(STATUS "Using Conan toolchain: ${CMAKE_CURRENT_LIST_FILE}")

if(${CMAKE_VERSION} VERSION_LESS "3.15")
    message(FATAL_ERROR "The 'CMakeToolchain' generator only works with CMake >= 3.15")
endif()


include("/home/cclark/.conan2/p/b/emsdk629b3f8c78cdf/p/bin/upstream/emscripten/cmake/Modules/Platform/Emscripten.cmake")


########## generic_system block #############
# Definition of system, platform and toolset
#############################################





set(CMAKE_C_COMPILER "/home/cclark/.conan2/p/b/emsdk629b3f8c78cdf/p/bin/upstream/emscripten/emcc")
set(CMAKE_CXX_COMPILER "/home/cclark/.conan2/p/b/emsdk629b3f8c78cdf/p/bin/upstream/emscripten/em++")


string(APPEND CONAN_CXX_FLAGS " -stdlib=libc++")


# Conan conf flags start: Release
# Conan conf flags end

foreach(config IN LISTS CMAKE_CONFIGURATION_TYPES)
    string(TOUPPER ${config} config)
    if(DEFINED CONAN_CXX_FLAGS_${config})
      string(APPEND CMAKE_CXX_FLAGS_${config}_INIT " ${CONAN_CXX_FLAGS_${config}}")
    endif()
    if(DEFINED CONAN_C_FLAGS_${config})
      string(APPEND CMAKE_C_FLAGS_${config}_INIT " ${CONAN_C_FLAGS_${config}}")
    endif()
    if(DEFINED CONAN_SHARED_LINKER_FLAGS_${config})
      string(APPEND CMAKE_SHARED_LINKER_FLAGS_${config}_INIT " ${CONAN_SHARED_LINKER_FLAGS_${config}}")
    endif()
    if(DEFINED CONAN_EXE_LINKER_FLAGS_${config})
      string(APPEND CMAKE_EXE_LINKER_FLAGS_${config}_INIT " ${CONAN_EXE_LINKER_FLAGS_${config}}")
    endif()
endforeach()

if(DEFINED CONAN_CXX_FLAGS)
  string(APPEND CMAKE_CXX_FLAGS_INIT " ${CONAN_CXX_FLAGS}")
endif()
if(DEFINED CONAN_C_FLAGS)
  string(APPEND CMAKE_C_FLAGS_INIT " ${CONAN_C_FLAGS}")
endif()
if(DEFINED CONAN_SHARED_LINKER_FLAGS)
  string(APPEND CMAKE_SHARED_LINKER_FLAGS_INIT " ${CONAN_SHARED_LINKER_FLAGS}")
endif()
if(DEFINED CONAN_EXE_LINKER_FLAGS)
  string(APPEND CMAKE_EXE_LINKER_FLAGS_INIT " ${CONAN_EXE_LINKER_FLAGS}")
endif()


get_property( _CMAKE_IN_TRY_COMPILE GLOBAL PROPERTY IN_TRY_COMPILE )
if(_CMAKE_IN_TRY_COMPILE)
    message(STATUS "Running toolchain IN_TRY_COMPILE")
    return()
endif()

set(CMAKE_FIND_PACKAGE_PREFER_CONFIG ON)

# Definition of CMAKE_MODULE_PATH
list(PREPEND CMAKE_MODULE_PATH "/home/cclark/.conan2/p/b/emsdk629b3f8c78cdf/p/bin/releases/src" "/home/cclark/.conan2/p/b/emsdk629b3f8c78cdf/p/bin/upstream/emscripten/cmake/Modules" "/home/cclark/.conan2/p/b/emsdk629b3f8c78cdf/p/bin/upstream/emscripten/cmake/Modules/Platform" "/home/cclark/.conan2/p/b/emsdk629b3f8c78cdf/p/bin/upstream/emscripten/system/lib/libunwind/cmake/Modules" "/home/cclark/.conan2/p/b/emsdk629b3f8c78cdf/p/bin/upstream/emscripten/system/lib/libunwind/cmake" "/home/cclark/.conan2/p/b/emsdk629b3f8c78cdf/p/bin/upstream/emscripten/tests/cmake/target_library" "/home/cclark/.conan2/p/b/emsdk629b3f8c78cdf/p/bin/upstream/lib/cmake/llvm")
# the generators folder (where conan generates files, like this toolchain)
list(PREPEND CMAKE_MODULE_PATH ${CMAKE_CURRENT_LIST_DIR})

# Definition of CMAKE_PREFIX_PATH, CMAKE_XXXXX_PATH
# The explicitly defined "builddirs" of "host" context dependencies must be in PREFIX_PATH
list(PREPEND CMAKE_PREFIX_PATH "/home/cclark/.conan2/p/b/emsdk629b3f8c78cdf/p/bin/releases/src" "/home/cclark/.conan2/p/b/emsdk629b3f8c78cdf/p/bin/upstream/emscripten/cmake/Modules" "/home/cclark/.conan2/p/b/emsdk629b3f8c78cdf/p/bin/upstream/emscripten/cmake/Modules/Platform" "/home/cclark/.conan2/p/b/emsdk629b3f8c78cdf/p/bin/upstream/emscripten/system/lib/libunwind/cmake/Modules" "/home/cclark/.conan2/p/b/emsdk629b3f8c78cdf/p/bin/upstream/emscripten/system/lib/libunwind/cmake" "/home/cclark/.conan2/p/b/emsdk629b3f8c78cdf/p/bin/upstream/emscripten/tests/cmake/target_library" "/home/cclark/.conan2/p/b/emsdk629b3f8c78cdf/p/bin/upstream/lib/cmake/llvm")
# The Conan local "generators" folder, where this toolchain is saved.
list(PREPEND CMAKE_PREFIX_PATH ${CMAKE_CURRENT_LIST_DIR} )
list(PREPEND CMAKE_PROGRAM_PATH "/home/cclark/.conan2/p/b/emsdk629b3f8c78cdf/p/bin" "/home/cclark/.conan2/p/b/emsdk629b3f8c78cdf/p/bin/upstream/emscripten")
list(PREPEND CMAKE_INCLUDE_PATH "/home/cclark/.conan2/p/boostfffbedcd6bfa8/p/include")

if(NOT DEFINED CMAKE_FIND_ROOT_PATH_MODE_PACKAGE OR CMAKE_FIND_ROOT_PATH_MODE_PACKAGE STREQUAL "ONLY")
    set(CMAKE_FIND_ROOT_PATH_MODE_PACKAGE "BOTH")
endif()
if(NOT DEFINED CMAKE_FIND_ROOT_PATH_MODE_PROGRAM OR CMAKE_FIND_ROOT_PATH_MODE_PROGRAM STREQUAL "ONLY")
    set(CMAKE_FIND_ROOT_PATH_MODE_PROGRAM "BOTH")
endif()
if(NOT DEFINED CMAKE_FIND_ROOT_PATH_MODE_LIBRARY OR CMAKE_FIND_ROOT_PATH_MODE_LIBRARY STREQUAL "ONLY")
    set(CMAKE_FIND_ROOT_PATH_MODE_LIBRARY "BOTH")
endif()
if(NOT DEFINED CMAKE_FIND_ROOT_PATH_MODE_INCLUDE OR CMAKE_FIND_ROOT_PATH_MODE_INCLUDE STREQUAL "ONLY")
    set(CMAKE_FIND_ROOT_PATH_MODE_INCLUDE "BOTH")
endif()


if (DEFINED ENV{PKG_CONFIG_PATH})
set(ENV{PKG_CONFIG_PATH} "${CMAKE_CURRENT_LIST_DIR}:$ENV{PKG_CONFIG_PATH}")
else()
set(ENV{PKG_CONFIG_PATH} "${CMAKE_CURRENT_LIST_DIR}:")
endif()




# Variables
# Variables  per configuration


# Preprocessor definitions
# Preprocessor definitions per configuration


if(CMAKE_POLICY_DEFAULT_CMP0091)  # Avoid unused and not-initialized warnings
endif()
