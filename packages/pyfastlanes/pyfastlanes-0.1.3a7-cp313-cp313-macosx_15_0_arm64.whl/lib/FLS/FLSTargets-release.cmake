#----------------------------------------------------------------
# Generated CMake target import file for configuration "Release".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "FLS::FastLanes" for configuration "Release"
set_property(TARGET FLS::FastLanes APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(FLS::FastLanes PROPERTIES
  IMPORTED_LINK_INTERFACE_LANGUAGES_RELEASE "CXX"
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/libFastLanes.a"
  )

list(APPEND _cmake_import_check_targets FLS::FastLanes )
list(APPEND _cmake_import_check_files_for_FLS::FastLanes "${_IMPORT_PREFIX}/lib/libFastLanes.a" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
