#!/bin/sh

export VERSION="snapshots"

export TARGET="bcm27xx/bcm2710"
export PROFILE="rpi-3"

export PACKAGES="${PACKAGES} -kmod-ath10k-ct kmod-usb-net-asix-ax88179 python3-mm-cli autoygg-go"
