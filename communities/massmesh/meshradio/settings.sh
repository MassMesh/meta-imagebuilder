#!/bin/sh

export EXTRA_IMAGE_NAME="massmesh-meshradio"

## wireless controller code: We want to deselect micro wpad package and support full feature
export PACKAGES="${PACKAGES} -wpad-basic"

## support encrypted radios and routing jointhemesh.net
export PACKAGES="${PACKAGES} wpad-mesh-openssl"

## for opkg to be able to access https links
export PACKAGES="${PACKAGES} libustream-openssl ca-bundle ca-certificates"

## add debugging tools
export PACKAGES="${PACKAGES} tcpdump"

## add prometheus-node-exporter packages
export PACKAGES="${PACKAGES} prometheus-node-exporter-lua prometheus-node-exporter-lua-wifi prometheus-node-exporter-lua-wifi_stations prometheus-node-exporter-lua-openwrt prometheus-node-exporter-lua-netstat"
