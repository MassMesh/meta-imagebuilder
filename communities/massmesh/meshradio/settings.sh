#!/bin/sh

export EXTRA_IMAGE_NAME="massmesh-meshradio"

## wireless controller code: We want to deselect micro wpad package and support full feature
export PACKAGES="${PACKAGES} -wpad-basic"

## batman-adv fully blown and in-kernel layer 2 switch from ozzy hell
export PACKAGES="${PACKAGES} batctl-full"
export PACKAGES="${PACKAGES} kmod-batman-adv"

## support encrypted radios and routing jointhemesh.net
export PACKAGES="${PACKAGES} wpad-mesh-openssl"
export PACKAGES="${PACKAGES} luci-app-cjdns cjdns"
