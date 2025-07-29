CMAKE_MINIMUM_REQUIRED(VERSION 3.2)

SET(PROJ_NAME "external_ballistics")

PROJECT(${PROJ_NAME} Fortran)

IF(WIN32)
  SET(CMAKE_SHARED_LINKER_FLAGS "-static")
ELSE()
  SET(CMAKE_FORTRAN_FLAGS "${CMAKE_FORTRAN_FLAGS} -fPIC")
ENDIF(WIN32)

IF(NOT CMAKE_BUILD_TYPE)
  SET(CMAKE_BUILD_TYPE "Release")
  MESSAGE("Default build type is RELEASE!")
ENDIF()

IF(CMAKE_BUILD_TYPE STREQUAL "Debug")
  SET(CMAKE_Fortran_FLAGS "${CMAKE_Fortran_FLAGS_Debug} -ffree-line-length-0 -Wall -g")
ELSE()
  SET(CMAKE_Fortran_FLAGS "-O3 -ffree-line-length-0 -ffast-math -funroll-loops ${CMAKE_Fortran_FLAGS_Release}")
ENDIF()

SET(SRC_DLL "src/solve_eb.f90"
            "src/solve_ebh.f90"
)

FILE(GLOB SRC ${PROJECT_SOURCE_DIR}/src/*.f90)
ADD_LIBRARY("sextbal" SHARED ${SRC_DLL})
