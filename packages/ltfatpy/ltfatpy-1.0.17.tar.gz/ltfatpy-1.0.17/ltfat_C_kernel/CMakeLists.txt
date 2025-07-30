CMAKE_MINIMUM_REQUIRED(VERSION 2.8.11)

include_directories(${CMAKE_CURRENT_SOURCE_DIR})
include_directories(${CMAKE_CURRENT_SOURCE_DIR}/thirdparty)
SET(CMAKE_C_FLAGS "-O3 -fPIC")
SET(CMAKE_EXE_LINKER_FLAGS "-lc -lm")

set(SRC dgt.c dgt_fac.c dgt_fb.c dgt_multi.c dgt_ola.c dgt_shear.c dgt_walnut.c
        dgtreal_fac.c dwilt.c idwilt.c wmdct.c iwmdct.c filterbank.c ifilterbank.c
        heapint.c idgt.c idgt_fac.c idgt_fb.c iwfac.c pfilt.c reassign.c spread.c
        wfac.c windows.c winmanip.c ltfat_complexindependent.c dgt_shearola.c
        dct_ci.c dst_ci.c fftreal.c)

set(SRC_BLASLAPACK ltfat_blaslapack.c gabdual_fac.c gabtight_fac.c
                   ltfat_complexindependent_bl.c)

set(SRC_NOTYPECHANGE c-safe-memalloc.c integer_manip.c)

add_library(ltfatf STATIC ${SRC} ${SRC_BLASLAPACK})
target_link_libraries(ltfatf ${FFTW_LIBRARIES} ${FFTWF_LIBRARIES} 
${LAPACK_LIBRARIES} ${CMAKE_EXE_LINKER_FLAGS})
target_compile_definitions(ltfatf PUBLIC LTFAT_SINGLE)
install(TARGETS ltfatf ARCHIVE DESTINATION ${CKERNEL_DIR}/lib)

add_library(ltfat STATIC ${SRC} ${SRC_BLASLAPACK} ${SRC_NOTYPECHANGE})
target_link_libraries(ltfat ${FFTW_LIBRARIES} ${FFTWF_LIBRARIES} 
${LAPACK_LIBRARIES} ${CMAKE_EXE_LINKER_FLAGS})
target_compile_definitions(ltfat PUBLIC LTFAT_DOUBLE)
install(TARGETS ltfat ARCHIVE DESTINATION ${CKERNEL_DIR}/lib)

#add_subdirectory(tests)
