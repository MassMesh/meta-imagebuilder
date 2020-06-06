#!/bin/sh

export VERSION="snapshots"

export TARGET="brcm27xx/bcm2711"
export PROFILE="rpi-4"

export PACKAGES="${PACKAGES} kmod-usb-net-asix-ax88179 kmod-usb-net-rtl8152 python3-mm-cli autoygg-go python3-argh python3-netaddr"
