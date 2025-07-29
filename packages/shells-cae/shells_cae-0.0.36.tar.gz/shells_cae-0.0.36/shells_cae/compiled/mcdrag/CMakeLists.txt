CMAKE_MINIMUM_REQUIRED(VERSION 3.2)
SET(PROJ_NAME "mcdrag_lib")

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

SET(SRC_DLL "src/mcdrag.f90")
SET(SRC_EXE "src/test.f90")

FILE(GLOB SRC ${PROJECT_SOURCE_DIR}/src/*.f90)

ADD_EXECUTABLE(${PROJ_NAME} ${SRC_EXE})
ADD_LIBRARY("mcdrag" SHARED ${SRC_DLL})

TARGET_LINK_LIBRARIES(${PROJ_NAME} mcdrag)
