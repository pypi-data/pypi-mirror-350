CMAKE_MINIMUM_REQUIRED(VERSION 3.1)

PROJECT(KONTUR Fortran C)

SET(CMAKE_Fortran_FLAGS_DEBUG "${CMAKE_Fortran_FLAGS_DEBUG} -Wall -Werror -std=legacy")
SET(CMAKE_Fortran_FLAGS_RELEASE "${CMAKE_Fortran_FLAGS_RELEASE} -O0 -Wall -Werror -std=legacy")
SET(CMAKE_C_FLAGS_DEBUG "${CMAKE_C_FLAGS_DEBUG} -Wall -Werror")
SET(CMAKE_C_FLAGS_RELEASE "${CMAKE_C_FLAGS_RELEASE} -O2 -ffast-math -funroll-loops")

IF(WIN32)
  SET(CMAKE_SHARED_LINKER_FLAGS "-static")
ELSE()
  SET(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -fPIC")
ENDIF(WIN32)

IF(NOT CMAKE_BUILD_TYPE)
  SET(CMAKE_BUILD_TYPE "Release")
  MESSAGE("Default build type is RELEASE!")
ENDIF(NOT CMAKE_BUILD_TYPE)

SET(LIBKONTUR_SRC src/csv.c
                  src/csvstep.c
                  src/structs.c
                  src/dcel.for
                  src/disco.for
                  src/geom.for
                  src/ggr.for
                  src/hybrid.for
                  src/inter5.for
                  src/interp.for
                  src/nave.for
                  src/newt.for
                  src/normfo.for
                  src/popin.for
                  src/prebr.for
                  src/prod.for
                  src/s4.for
                  src/schape.for
                  src/simp.for
                  src/skbarb.for
                  src/trans.for
                  #src/kontur.for
                  )

SET(EXEC_SRC src/kontur.c )

INCLUDE_DIRECTORIES(include)

ADD_LIBRARY(kontur SHARED ${LIBKONTUR_SRC})

ADD_EXECUTABLE(kontur_test ${EXEC_SRC})
TARGET_LINK_LIBRARIES(kontur_test kontur)
