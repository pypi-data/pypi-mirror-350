cmake_minimum_required(VERSION 3.22)

set(PROJECT_NAME wadas_runtime)

project(${PROJECT_NAME})

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

if(CMAKE_CXX_COMPILER_ID MATCHES "Clang" OR CMAKE_CXX_COMPILER_ID MATCHES "GNU")
    # lots of warnings and all warnings as errors
    message(STATUS "Setting GCC/Clang specific flags for the entire build")
    add_compile_options(-Wall -Wextra -Werror -pedantic -Wdouble-promotion -Wfloat-conversion)
    set(CMAKE_CXX_FLAGS_DEBUG "-g")
    set(CMAKE_CXX_FLAGS_RELEASE "-O3")
elseif(CMAKE_CXX_COMPILER_ID MATCHES "MSVC")
    message(STATUS "Setting Visual Studio specific flags for the entire build")
    add_compile_options(/W3 /WX /arch:AVX2 /arch:SSE2)
    add_link_options(/WX)
else()
    message(AUTHOR_WARNING "-- Building with unrecognised compiler, not setting any specific flags")
endif()

find_package(Python REQUIRED COMPONENTS Interpreter Development.Module)
find_package(pybind11 REQUIRED)

# Add OpenSSL library for AES decryption
find_package(OpenSSL REQUIRED)

file(GLOB SRC_FILES src/*.cpp)
include_directories(_core ${CMAKE_CURRENT_SOURCE_DIR}/include)

include(FetchContent)
FetchContent_Declare(
    nlohmann_json
    URL https://github.com/nlohmann/json/releases/download/v3.12.0/include.zip
)
FetchContent_GetProperties(nlohmann_json)
if(NOT nlohmann_json_POPULATED)
    FetchContent_Populate(nlohmann_json)
endif()
include_directories(${nlohmann_json_SOURCE_DIR}/include)

python_add_library(_core MODULE ${SRC_FILES} WITH_SOABI)
target_link_libraries(_core PRIVATE pybind11::headers OpenSSL::Crypto)

install(
    TARGETS _core
    DESTINATION ${PROJECT_NAME}
)