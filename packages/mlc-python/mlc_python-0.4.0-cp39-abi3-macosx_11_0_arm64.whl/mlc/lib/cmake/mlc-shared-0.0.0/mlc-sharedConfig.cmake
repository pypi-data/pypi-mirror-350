include(CMakeFindDependencyMacro)

string(REGEX MATCHALL "[^;]+" SEPARATE_DEPENDENCIES "mlc-backtrace 0.1.5")

foreach(dependency ${SEPARATE_DEPENDENCIES})
  string(REPLACE " " ";" args "${dependency}")
  find_dependency(${args})
endforeach()

include("${CMAKE_CURRENT_LIST_DIR}/mlc-sharedTargets.cmake")
