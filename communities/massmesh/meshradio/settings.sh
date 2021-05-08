#!/bin/sh

export EXTRA_IMAGE_NAME="massmesh-meshradio"

## wireless controller code: We want to deselect micro wpad package and support full feature
export PACKAGES="${PACKAGES} -wpad-basic"

## support encrypted radios and routing jointhemesh.net
export PACKAGES="${PACKAGES} wpad-mesh-openssl"

## add debugging tools
export PACKAGES="${PACKAGES} tcpdump"
