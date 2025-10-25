cmake_minimum_required(VERSION 3.15)
project(${SKBUILD_PROJECT_NAME} LANGUAGES C)

# Find Python
find_package(
  Python
  COMPONENTS Interpreter Development.Module NumPy
  REQUIRED)

# Get NumPy include directory
message(STATUS "NumPy include directory: ${Python_NumPy_INCLUDE_DIRS}")

# Cythonize the .pyx file to .c
add_custom_command(
  OUTPUT cutil.c
  COMMENT "Cythonizing ${CMAKE_CURRENT_SOURCE_DIR}/src/pypolyline/cutil.pyx"
  COMMAND Python::Interpreter -m cython
          "${CMAKE_CURRENT_SOURCE_DIR}/src/pypolyline/cutil.pyx"
          --output-file cutil.c
          -I "${CMAKE_CURRENT_SOURCE_DIR}/src/pypolyline"
  DEPENDS src/pypolyline/cutil.pyx src/pypolyline/pypolyline_p.pxd
  VERBATIM)

# Create the extension module
python_add_library(cutil MODULE cutil.c WITH_SOABI)

# Set include directories
target_include_directories(cutil PRIVATE
  ${CMAKE_CURRENT_SOURCE_DIR}/src/pypolyline
  ${Python_NumPy_INCLUDE_DIRS}
)

# Link against the Rust library
# The library is pre-built and located in src/pypolyline/
find_library(POLYLINE_LIBRARY
  NAMES polylineffi libpolylineffi
  PATHS ${CMAKE_CURRENT_SOURCE_DIR}/src/pypolyline
  NO_DEFAULT_PATH
  REQUIRED
)
message(STATUS "Found Rust polyline library: ${POLYLINE_LIBRARY}")

target_link_libraries(cutil PRIVATE ${POLYLINE_LIBRARY})

# Set RPATH for different platforms
if(APPLE)
  set_target_properties(cutil PROPERTIES
    INSTALL_RPATH "@loader_path"
    BUILD_WITH_INSTALL_RPATH TRUE
  )
elseif(UNIX)
  set_target_properties(cutil PROPERTIES
    INSTALL_RPATH "$ORIGIN"
    BUILD_WITH_INSTALL_RPATH TRUE
  )
endif()

# Install the extension module
install(TARGETS cutil DESTINATION pypolyline)

# Install the shared library
if(APPLE)
  set(POLYLINE_LIB_NAME "libpolylineffi.dylib")
elseif(UNIX)
  set(POLYLINE_LIB_NAME "libpolylineffi.so")
elseif(WIN32)
  set(POLYLINE_LIB_NAME "polylineffi.dll")
endif()

install(FILES ${CMAKE_CURRENT_SOURCE_DIR}/src/pypolyline/${POLYLINE_LIB_NAME}
        DESTINATION pypolyline)

# Install header file
install(FILES ${CMAKE_CURRENT_SOURCE_DIR}/src/pypolyline/header.h
        DESTINATION pypolyline)
