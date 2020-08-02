#!/bin/sh

# Add the massmesh package repos. The meta script will replace the {{ pkg_arch }} string with the package architecture.
export REPOS=`echo -en "${REPOS}\n# Massmesh package repo\nsrc/gz custom http://downloads.massmesh.net/snapshots/packages/{{ pkg_arch }}/generic"`;

export PACKAGES="${PACKAGES} luci luci-theme-material" # Luci for web configuration
export PACKAGES="${PACKAGES} kmod-ath10k-ct ath10k-firmware-qca988x-ct -kmod-ath10k-ct-smallbuffers" # QCA wireless firmware for mesh mode

