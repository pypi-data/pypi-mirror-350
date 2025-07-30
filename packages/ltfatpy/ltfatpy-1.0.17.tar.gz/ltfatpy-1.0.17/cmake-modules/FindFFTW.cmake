SET(TRIAL_PATHS
 $ENV{FFTW_ROOT}/include
 ${FFTW_ROOT}/include
 /usr/include
 /usr/local/include
 /opt/local/include
 /sw/include
 )
FIND_PATH(FFTW_INCLUDE_DIR fftw3.h ${TRIAL_PATHS} DOC "Include for FFTW")
message("FFTW_INCLUDE_DIR = ${FFTW_INCLUDE_DIR}")

SET(TRIAL_LIBRARY_PATHS
 /usr/lib 
 /usr/local/lib
 /opt/local/lib
 /sw/lib
 $ENV{FFTW_ROOT}/lib
 ${FFTW_ROOT}/lib
 )

SET(FFTW_LIBRARIES "FFTW_LIBRARIES-NOTFOUND" CACHE STRING "FFTW library")
# Try to detect the lib
FIND_LIBRARY(FFTW_LIBRARIES fftw3 fftw3f ${TRIAL_LIBRARY_PATHS} DOC "FFTW library")
FIND_LIBRARY(FFTWF_LIBRARIES fftw3f ${TRIAL_LIBRARY_PATHS} DOC "FFTW library single precision")
message("FFTW_LIBRARIES = ${FFTW_LIBRARIES}")
message("FFTWF_LIBRARIES = ${FFTWF_LIBRARIES}")
mark_as_advanced(FFTW_INCLUDE_DIR)
mark_as_advanced(FFTW_LIBRARIES)
mark_as_advanced(FFTWF_LIBRARIES)
include(FindPackageHandleStandardArgs)
FIND_PACKAGE_HANDLE_STANDARD_ARGS(FFTW DEFAULT_MSG FFTW_LIBRARIES FFTWF_LIBRARIES FFTW_INCLUDE_DIR)
