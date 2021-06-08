#!/bin/sh
export EXTRA_IMAGE_NAME="massmesh-meshnode"


## Optware Packages support for TLS/SSL/x509
export PACKAGES="${PACKAGES} libustream-mbedtls ca-bundle ca-certificates"

## Routing
export PACKAGES="${PACKAGES} yggdrasil cjdns" # mesh routing protocols yggdrasil and cjdns
export PACKAGES="${PACKAGES} luci-app-yggdrasil" # LuCI admin for yggdrasil
export PACKAGES="${PACKAGES} luci-app-cjdns" # LuCI admin for cjdns

## MassMesh Packages downloads.massmesh.net/snapshots/packages
export PACKAGES="${PACKAGES} autoygg-go"
export PACKAGES="${PACKAGES} luci-app-autoygg"
export PACKAGES="${PACKAGES} massmesh-gateways"

## Benchmarking / Common Utils
export PACKAGES="${PACKAGES} nano iperf3 curl tcpdump iputils-ping vnstat mtr noping"
export PACKAGES="${PACKAGES} haveged" # Ensure entropy

## JQ fast CLI parsing one liner commands
# ~ for OpenWrt see: jshn.sh, /lib/functions.sh
export PACKAGES="${PACKAGES} jq"

## Creates a WAN interface
# ~ Gain IP address from USB tethered celluar phones
export PACKAGES="${PACKAGES} kmod-usb-net-rndis" # USB Tethering
export PACKAGES="${PACKAGES} kmod-usb-net-asix-ax88179 kmod-usb-net-rtl8152" # USB Adapters

# For prometheus metrics export
export PACKAGES="${PACKAGES} prometheus-node-exporter-lua prometheus-node-exporter-lua-openwrt prometheus-node-exporter-lua-netstat"

# For prometheus metrics support of the meshradio, behind meshnode: we need a reverse proxy
export PACKAGES="${PACKAGES} nginx"

## DESELECTED ##########################################################################
# ~ Lost Tor support after yggdrasil CKR fixed throughput without need of proxy.
# export PACKAGES="${PACKAGES} tor tor-fw-helper tor-resolve torsocks" # Tor
#
# ~ This should be re-enabled, we should be serving HTML or using opennds 9000
# export PACKAGES="${PACKAGES} nodogsplash" # Captive portal - currently breaks peering and gateway
