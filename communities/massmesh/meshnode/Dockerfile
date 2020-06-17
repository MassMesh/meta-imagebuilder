FROM    openwrt-x86-generic-rootfs

ADD     docker/files/etc/inittab           /etc/inittab
ADD     docker/files/etc/config/network    /etc/config/network

ENV     EXTRA_IMAGE_NAME "massmesh-meshnode"

USER    root

CMD     ["/sbin/init"]