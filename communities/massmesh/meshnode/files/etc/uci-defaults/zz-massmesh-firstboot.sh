#!/bin/sh

# Remove all forwardings (LAN -> WAN should be the only one by default)
uci show firewall | grep -o "firewall\.\@forwarding\[[0-9]\+\]" | uniq | xargs uci delete
uci commit

# Re-add forwardings between ygg and lan
uci add firewall forwarding
uci set firewall.@forwarding[-1].dest='yggdrasil'
uci set firewall.@forwarding[-1].src='lan'
uci commit

# Enable masquerading on ygg interface
uci set firewall.yggdrasil.masq='1'
uci commit

# Allow Iperf3 testing TCP/UDP on port 5201
uci add firewall rule
uci set firewall.@rule[-1].name='Iperf3 Throughput / Bandwidth'
uci set firewall.@rule[-1].src='*'
uci set firewall.@rule[-1].dest_port='5201'
uci set firewall.@rule[-1].target='ACCEPT'
uci commit

# Allow a default-disabled firewall rule for prometheus metrics access from
# prometheus.massmesh.net
uci add firewall rule
uci set firewall.@rule[-1].name='Metrics access from prometheus.massmesh.net'
uci set firewall.@rule[-1].src='yggdrasil'
uci add_list firewall.@rule[-1].proto='tcp'
uci set firewall.@rule[-1].family='ipv6'
uci set firewall.@rule[-1].dest_port='9100-9101'
uci add_list firewall.@rule[-1].src_ip='201:506e:60d6:bd66:e35c:606:4883:ea9a'
uci set firewall.@rule[-1].target='ACCEPT'
uci set firewall.@rule[-1].enabled=0
uci commit


# Add yggdrasil peers
uci add yggdrasil interface_peer
uci set yggdrasil.@interface_peer[-1].uri='tcp://45.77.107.150:34660'
uci set yggdrasil.@interface_peer[-1].interface=`uci get network.wan.ifname`
uci add yggdrasil interface_peer
uci set yggdrasil.@interface_peer[-1].uri='tcp://45.76.166.128:12345'
uci set yggdrasil.@interface_peer[-1].interface=`uci get network.wan.ifname`
uci add yggdrasil interface_peer
uci set yggdrasil.@interface_peer[-1].uri='tcp://50.236.201.218:56088'
uci set yggdrasil.@interface_peer[-1].interface=`uci get network.wan.ifname`
uci add yggdrasil interface_peer
uci set yggdrasil.@interface_peer[-1].uri='tcp://64.112.176.176:1617'
uci set yggdrasil.@interface_peer[-1].interface=`uci get network.wan.ifname`
uci add yggdrasil interface_peer
uci set yggdrasil.@interface_peer[-1].uri='tls://67.205.187.55:19102'
uci set yggdrasil.@interface_peer[-1].interface=`uci get network.wan.ifname`
uci add yggdrasil interface_peer
uci set yggdrasil.@interface_peer[-1].uri='tcp://67.205.187.55:19103'
uci set yggdrasil.@interface_peer[-1].interface=`uci get network.wan.ifname`
uci add yggdrasil interface_peer
uci set yggdrasil.@interface_peer[-1].uri='tcp://104.248.15.125:31337'
uci set yggdrasil.@interface_peer[-1].interface=`uci get network.wan.ifname`
uci add yggdrasil interface_peer
uci set yggdrasil.@interface_peer[-1].uri='tcp://108.175.10.127:61216'
uci set yggdrasil.@interface_peer[-1].interface=`uci get network.wan.ifname`
uci add yggdrasil interface_peer
uci set yggdrasil.@interface_peer[-1].uri='tcp://198.58.100.240:44478'
uci set yggdrasil.@interface_peer[-1].interface=`uci get network.wan.ifname`
uci add yggdrasil interface_peer
uci set yggdrasil.@interface_peer[-1].uri='tcp://lancis.iscute.moe:49273'
uci set yggdrasil.@interface_peer[-1].interface=`uci get network.wan.ifname`
uci add yggdrasil interface_peer
uci set yggdrasil.@interface_peer[-1].uri='tcp://longseason.1200bps.xyz:13121'
uci set yggdrasil.@interface_peer[-1].interface=`uci get network.wan.ifname`
uci add yggdrasil interface_peer
uci set yggdrasil.@interface_peer[-1].uri='tcp://gateway1.clearnet.massmesh.net:1617'
uci set yggdrasil.@interface_peer[-1].interface=`uci get network.wan.ifname`
uci commit

# Add yggdrasil tunnel routing config
uci set yggdrasil.yggdrasil.TunnelRouting_Enable=1
uci add yggdrasil ipv4_local_subnet
uci set yggdrasil.@ipv4_local_subnet[-1].subnet='0.0.0.0/0'
uci commit

# Set ula
uci set network.globals.ula_prefix=$(ygguci get | yggdrasil -useconf -normaliseconf -json | yggdrasil -useconf -subnet)
uci commit
