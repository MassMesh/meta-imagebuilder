#!/bin/sh

export EXTRA_IMAGE_NAME="massmesh-meshnode"

## Routing
export PACKAGES="${PACKAGES} yggdrasil cjdns" # mesh routing protocols yggdrasil and cjdns
export PACKAGES="${PACKAGES} luci-app-yggdrasil luci-app-cjdns" # LuCI admin for yggdrasil and cjdns
export PACKAGES="${PACKAGES} python3-mm-cli autoygg-go" # via repo.com/massmesh/mm-toolbox.git;

## JQ fast CLI parsing one liner commands (for OpenWrt see: jshn.sh /lib/functions.sh && /usr/lib)
export PACKAGES="${PACKAGES} jq" # jq for scripting json config changes

## Creates a WAN interface, gains IP address from usb-tethered handheld celluar phone with USB connection
export PACKAGES="${PACKAGES} kmod-usb-net-rndis" # USB Tethering

export PACKAGES="${PACKAGES} kmod-usb-net-asix-ax88179 kmod-usb-net-rtl8152" # usb-ethernet kernel mods

## USB Reset utility used for tethering or jammed Wi-Fi devices (see LiMe opkgs: watchping / watchdog)
export PACKAGES="${PACKAGES} usbreset" # USB HC reset (host side, soft reset)

## NEW DESELECT
# ~ Python3 "Light" is selected by python3-mm-cli
# export PACKAGES="${PACKAGES} python3" # Python3.8
# ~ package the source py files
# export PACKAGES="${PACKAGES} python3-mm-cli-src" # via repo.com/massmesh/mm-toolbox.git;

## OLD DESELECT
# ~ Lost Tor support after yggdrasil CKR fixed throughput without need of proxy.
# ~ Please revisit
# export PACKAGES="${PACKAGES} tor tor-fw-helper tor-resolve torsocks" # Tor
# ~ This should be re-enabled, we should be serving HTML or using opennds 9000
# export PACKAGES="${PACKAGES} nodogsplash" # Captive portal - currently breaks peering and gateway
