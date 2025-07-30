# Defines the CMake commands/policies
cmake_minimum_required( VERSION 2.8.5 )

# Set the project name
project( LTFATPY )

# If the user specifies -DCMAKE_BUILD_TYPE on the command line, take their
# definition and dump it in the cache along with proper documentation, 
# otherwise set CMAKE_BUILD_TYPE to Debug prior to calling project()
#
IF(DEFINED CMAKE_BUILD_TYPE)
   SET(CMAKE_BUILD_TYPE ${CMAKE_BUILD_TYPE} CACHE STRING "Choose the type of
build, options are: None(CMAKE_CXX_FLAGS or CMAKE_C_FLAGS used) Debug
Release RelWithDebInfo MinSizeRel.")
ELSE()
   SET(CMAKE_BUILD_TYPE Release CACHE STRING "Choose the type of build,
options are: None(CMAKE_CXX_FLAGS or CMAKE_C_FLAGS used) Debug Release
RelWithDebInfo MinSizeRel.")
ENDIF()

#### Set global variables
set( CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH} ${CMAKE_CURRENT_LIST_DIR}/cmake-modules )
set(FFTW_ROOT "/usr/lib" CACHE PATH "FFTW lib folder")
set(LTFATPY_DIR "${CMAKE_SOURCE_DIR}/ltfatpy")
set(CKERNEL_DIR "${LTFATPY_SOURCE_DIR}/ltfat_C_kernel")
set(DOC_DIR "${LTFATPY_SOURCE_DIR}/doc")

#### Find FFTW
find_package(FFTW REQUIRED)
message ("FFTW found")
include_directories(${FFTW_INCLUDE_DIR})

### Find Lapack
find_package(LAPACK REQUIRED)
message ("LAPACK found")
message("BLAS VENDOR : ${BLA_VENDOR}")
message("LAPACK LIBRARIES : ${LAPACK_LIBRARIES}")

### Set PYTHON_SITE_DIR
#find_package ( PythonLibs REQUIRED )
#find_package ( PythonInterp REQUIRED )

#if ( PYTHON_VERSION_STRING AND PYTHONLIBS_VERSION_STRING )
#   if ( NOT PYTHON_VERSION_STRING VERSION_EQUAL PYTHONLIBS_VERSION_STRING )
#     message ( FATAL_ERROR "Version mismatch between python interpreter and libraries")
#   endif ( NOT PYTHON_VERSION_STRING VERSION_EQUAL PYTHONLIBS_VERSION_STRING )
#endif ( PYTHON_VERSION_STRING AND PYTHONLIBS_VERSION_STRING )

### Build c kernel (Using ${PYTHON_SITE_DIR} for install)
add_subdirectory(${CKERNEL_DIR})

#### uninstall target
configure_file(
    "${CMAKE_SOURCE_DIR}/cmake-modules/cmake_uninstall.cmake.in"
    "${CMAKE_CURRENT_BINARY_DIR}/cmake_uninstall.cmake"
    IMMEDIATE @ONLY)

add_custom_target(uninstall COMMAND ${CMAKE_COMMAND} 
                   -P ${CMAKE_CURRENT_BINARY_DIR}/cmake_uninstall.cmake)

