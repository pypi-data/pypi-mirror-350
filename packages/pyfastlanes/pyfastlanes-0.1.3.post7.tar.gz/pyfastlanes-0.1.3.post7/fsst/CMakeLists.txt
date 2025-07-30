add_compile_definitions(FSST_CMAKE_SOURCE_DIR="${CMAKE_CURRENT_SOURCE_DIR}")

include_directories(${CMAKE_CURRENT_SOURCE_DIR}/data/include)

add_subdirectory(${CMAKE_CURRENT_SOURCE_DIR}/benchmarks)
