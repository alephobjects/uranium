set(CPACK_PACKAGE_VENDOR "Ultimaker")
set(CPACK_PACKAGE_CONTACT "Arjen Hiemstra <a.hiemstra@ultimaker.com>")
set(CPACK_PACKAGE_DESCRIPTION_SUMMARY "Uranium 3D Application Framework")
set(CPACK_PACKAGE_VERSION_MAJOR 15)
set(CPACK_PACKAGE_VERSION_MINOR 05)
set(CPACK_PACKAGE_VERSION_PATCH 93)
set(CPACK_GENERATOR "DEB;RPM")

set(DEB_PACKAGE_TARGET_PLATFORM "debian-stretch" CACHE STRING "Target Debian/Ubuntu platform")

set(MINIMUM_ARCUS_VERSION "15.05.90" CACHE STRING "Minimum Arcus Version")
set(MINIMUM_CURA_LULZBOT_PYTHON_DEPS "0.1.0" CACHE STRING "Minimum Cura LulzBot Edition Python Dependencies")

set(RPM_REQUIRES
    "python3 >= 3.5.0"
    "python3-qt5 >= 5.6.0"
    "qt5-qtquickcontrols >= 5.6.0"
    "arcus >= 15.05.90"
)
string(REPLACE ";" "," RPM_REQUIRES "${RPM_REQUIRES}")
set(CPACK_RPM_PACKAGE_REQUIRES ${RPM_REQUIRES})
if(DEB_PACKAGE_TARGET_PLATFORM STREQUAL "ubuntu-xenial")
  set(DEB_DEPENDS
    "python3 (>= 3.5.0)"
    "cura-lulzbot-python3.5-deps (>=${MINIMUM_CURA_LULZBOT_PYTHON_DEPS})"
    "arcus (>= ${MINIMUM_ARCUS_VERSION})"
  )
else()
  set(DEB_DEPENDS
    "python3 (>= 3.5.0)"
    "python3-pyqt5 (>= 5.6.0)"
    "python3-pyqt5.qtopengl (>= 5.6.0)"
    "python3-pyqt5.qtquick (>= 5.6.0)"
    "python3-pyqt5.qtsvg (>= 5.6.0)"
    "qml-module-qtquick2 (>= 5.6.0)"
    "qml-module-qtquick-window2 (>= 5.6.0)"
    "qml-module-qtquick-layouts (>= 5.6.0)"
    "qml-module-qtquick-dialogs (>= 5.6.0)"
    "qml-module-qtquick-controls (>= 5.6.0)"
    "arcus (>= ${MINIMUM_ARCUS_VERSION})"
  )
endif()
string(REPLACE ";" "," DEB_DEPENDS "${DEB_DEPENDS}")
set(CPACK_DEBIAN_PACKAGE_DEPENDS ${DEB_DEPENDS})

include(CPack)
