#!/bin/sh

export EXTRA_IMAGE_NAME="massmesh-meshnode"

# Packages for all mesh nodes

export PACKAGES="${PACKAGES} yggdrasil cjdns" # mesh routing protocols yggdrasil and cjdns
export PACKAGES="${PACKAGES} luci-app-yggdrasil luci-app-cjdns" # LuCI admin for yggdrasil and cjdns
export PACKAGES="${PACKAGES} jq" # jq for scripting json config changes
# export PACKAGES="${PACKAGES} tor tor-fw-helper tor-resolve torsocks" # Tor
# export PACKAGES="${PACKAGES} nodogsplash" # Captive portal - currently breaks peering and gateway
export PACKAGES="${PACKAGES} kmod-usb-net-rndis" # USB Tethering
export PACKAGES="${PACKAGES} kmod-usb-net-asix-ax88179 kmod-usb-net-rtl8152" # usb-ethernet kernel mods
export PACKAGES="${PACKAGES} usbreset" # USB HC reset (host side, soft reset)
export PACKAGES="${PACKAGES} python3" # Python3.8
