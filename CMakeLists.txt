cmake_minimum_required(VERSION 3.21)
project(${SKBUILD_PROJECT_NAME} LANGUAGES C)

# Define source directory
set(PYPOLYLINE_SRC_DIR "${CMAKE_CURRENT_SOURCE_DIR}/src/pypolyline")

# Find Python
find_package(
  Python
  COMPONENTS Interpreter Development.Module NumPy
  REQUIRED)
include(UseCython)

# Get NumPy include directory
message(STATUS "NumPy include directory: ${Python_NumPy_INCLUDE_DIRS}")

cython_transpile(
  "${PYPOLYLINE_SRC_DIR}/cutil.pyx"
  LANGUAGE C
  OUTPUT_VARIABLE cutil
  CYTHON_ARGS -I "${PYPOLYLINE_SRC_DIR}"
)

# Create the extension module
python_add_library(cutil MODULE "${cutil}" WITH_SOABI)

# Set include directories
target_include_directories(cutil PRIVATE
  ${PYPOLYLINE_SRC_DIR}
  ${Python_NumPy_INCLUDE_DIRS}
)

# Link against the Rust library
# The library is pre-built and located in src/pypolyline/
find_library(POLYLINE_LIBRARY
  NAMES polylineffi libpolylineffi
  PATHS ${PYPOLYLINE_SRC_DIR}
  NO_DEFAULT_PATH
  REQUIRED
)
message(STATUS "Found polyline Rust library: ${POLYLINE_LIBRARY}")

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

install(FILES ${PYPOLYLINE_SRC_DIR}/${POLYLINE_LIB_NAME}
        DESTINATION pypolyline)

# Install header file
install(FILES ${PYPOLYLINE_SRC_DIR}/header.h
        DESTINATION pypolyline)
