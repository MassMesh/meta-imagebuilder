#!/bin/sh

export VERSION="snapshots"

export TARGET="bcm27xx/bcm2710"
export PROFILE="rpi-3"

# Avoid errors like:
# Unknown package 'cypress-nvram-43430-sdio-rpi-3b'.
# Unknown package 'cypress-nvram-43455-sdio-rpi-3b-plus'.
# ...
# Collected errors:
# * opkg_install_cmd: Cannot install package cypress-nvram-43430-sdio-rpi-3b.
# * opkg_install_cmd: Cannot install package cypress-nvram-43455-sdio-rpi-3b-plus.
#make[2]: *** [Makefile:166: package_install] Error 255
#make[1]: *** [Makefile:121: _call_image] Error 2
#make: *** [Makefile:239: image] Error 2
export PACKAGES="${PACKAGES} -cypress-nvram-43430-sdio-rpi-3b -cypress-nvram-43455-sdio-rpi-3b-plus"
