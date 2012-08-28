project(vc_poppler)
cmake_minimum_required(VERSION 2.8)
SET(CMAKE_MODULE_PATH "${CMAKE_SOURCE_DIR}/cmake/modules")

# get boost
set(Boost_USE_STATIC_LIBS   ON)
set(Boost_USE_MULTITHREADED ON)
find_package(Boost COMPONENTS
                system
                thread
                python
             REQUIRED)
include_directories(${Boost_INCLUDE_DIRS})
link_directories(${Boost_LIBRARY_DIRS})

# get python
find_package(PythonLibs REQUIRED)
include_directories(${PYTHON_INCLUDE_DIRS})
link_directories(${PYTHON_LIBRARIES})

find_package(Poppler REQUIRED)
include_directories(${POPPLER_CPP_INCLUDE_DIRS})

add_library(vc_poppler SHARED
        vc_pypoppler.cpp
    )

target_link_libraries(vc_poppler
        ${Boost_LIBRARIES}
        ${PYTHON_LIBRARIES}
        ${POPPLER_LIBRARIES}
    )