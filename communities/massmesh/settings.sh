#!/bin/sh

export PACKAGES="${PACKAGES} luci luci-theme-material" # Luci for web configuration
export PACKAGES="${PACKAGES} haveged" # Ensure entropy
export PACKAGES="${PACKAGES} kmod-ath10k-ct ath10k-firmware-qca988x-ct -kmod-ath10k-ct-smallbuffers" # QCA wireless firmware for mesh mode
export PACKAGES="${PACKAGES} nano iperf3 curl tcpdump iputils-ping vnstat mtr noping " # Benchmarking / debugging

