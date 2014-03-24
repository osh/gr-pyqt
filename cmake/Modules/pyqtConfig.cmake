INCLUDE(FindPkgConfig)
PKG_CHECK_MODULES(PC_PYQT pyqt)

FIND_PATH(
    PYQT_INCLUDE_DIRS
    NAMES pyqt/api.h
    HINTS $ENV{PYQT_DIR}/include
        ${PC_PYQT_INCLUDEDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/include
          /usr/local/include
          /usr/include
)

FIND_LIBRARY(
    PYQT_LIBRARIES
    NAMES gnuradio-pyqt
    HINTS $ENV{PYQT_DIR}/lib
        ${PC_PYQT_LIBDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/lib
          ${CMAKE_INSTALL_PREFIX}/lib64
          /usr/local/lib
          /usr/local/lib64
          /usr/lib
          /usr/lib64
)

INCLUDE(FindPackageHandleStandardArgs)
FIND_PACKAGE_HANDLE_STANDARD_ARGS(PYQT DEFAULT_MSG PYQT_LIBRARIES PYQT_INCLUDE_DIRS)
MARK_AS_ADVANCED(PYQT_LIBRARIES PYQT_INCLUDE_DIRS)

