cmake_minimum_required(VERSION 3.16)

project(test_0624_fileproc_00 LANGUAGES CXX)

set(CMAKE_AUTOUIC ON)
set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTORCC ON)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

find_package(QT NAMES Qt6 Qt5 REQUIRED COMPONENTS Core)
find_package(Qt${QT_VERSION_MAJOR} REQUIRED COMPONENTS Core)

add_executable(test_0624_fileproc_00
  main.cpp
)
target_link_libraries(test_0624_fileproc_00 Qt${QT_VERSION_MAJOR}::Core)

include(GNUInstallDirs)
install(TARGETS test_0624_fileproc_00
    LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
    RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}
)
