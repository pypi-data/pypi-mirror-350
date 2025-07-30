#----------------------------------------------------------------
# Generated CMake target import file for configuration "RelWithDebInfo".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "mlc::mlc-shared" for configuration "RelWithDebInfo"
set_property(TARGET mlc::mlc-shared APPEND PROPERTY IMPORTED_CONFIGURATIONS RELWITHDEBINFO)
set_target_properties(mlc::mlc-shared PROPERTIES
  IMPORTED_LOCATION_RELWITHDEBINFO "${_IMPORT_PREFIX}/lib/mlc/libmlc.so"
  IMPORTED_SONAME_RELWITHDEBINFO "libmlc.so"
  )

list(APPEND _cmake_import_check_targets mlc::mlc-shared )
list(APPEND _cmake_import_check_files_for_mlc::mlc-shared "${_IMPORT_PREFIX}/lib/mlc/libmlc.so" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
