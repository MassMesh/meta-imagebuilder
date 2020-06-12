#!/bin/sh

export VERSION="snapshots"

export TARGET="bcm27xx/bcm2711"
export PROFILE="rpi-4"
export PACKAGES="${PACKAGES} bcm27xx-eeprom bcm27xx-userland"
# ~ selects the following:
# libpci libkmod pciutils bcm27xx-userland blkid bcm27xx-eeprom

