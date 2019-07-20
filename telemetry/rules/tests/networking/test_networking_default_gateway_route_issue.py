from insights.core.plugins import make_fail
from insights.tests import InputData, archive_provider
from insights.specs import Specs
from telemetry.rules.plugins.networking import (networking_default_gateway_route_issue as no_def_route)

ROUTE_TABLE_HIT = """
10.15.10.0/24 dev p2p1 proto kernel scope link src 10.15.10.230 metric 100
10.200.160.0/24 dev em1 proto kernel scope link src 10.200.160.101 metric 100
broadcast 10.15.10.0 dev p2p1 table local proto kernel scope link src 10.15.10.230
local 10.15.10.230 dev p2p1 table local proto kernel scope host src 10.15.10.230
broadcast 10.15.10.255 dev p2p1 table local proto kernel scope link src 10.15.10.230
broadcast 10.200.160.0 dev em1 table local proto kernel scope link src 10.200.160.101
local 10.200.160.101 dev em1 table local proto kernel scope host src 10.200.160.101
broadcast 10.200.160.255 dev em1 table local proto kernel scope link src 10.200.160.101
broadcast 127.0.0.0 dev lo table local proto kernel scope link src 127.0.0.1
local 127.0.0.0/8 dev lo table local proto kernel scope host src 127.0.0.1
local 127.0.0.1 dev lo table local proto kernel scope host src 127.0.0.1
broadcast 127.255.255.255 dev lo table local proto kernel scope link src 127.0.0.1
fe80::/64 dev em1 proto kernel metric 256 mtu 9216
fe80::/64 dev p2p1 proto kernel metric 256
""".strip()

ROUTE_TABLE_NO_HIT = """
default via 10.15.10.1 dev p2p1 proto static metric 100
10.15.10.0/24 dev p2p1 proto kernel scope link src 10.15.10.230 metric 100
10.200.160.0/24 dev em1 proto kernel scope link src 10.200.160.101 metric 100
broadcast 10.15.10.0 dev p2p1 table local proto kernel scope link src 10.15.10.230
local 10.15.10.230 dev p2p1 table local proto kernel scope host src 10.15.10.230
broadcast 10.15.10.255 dev p2p1 table local proto kernel scope link src 10.15.10.230
broadcast 10.200.160.0 dev em1 table local proto kernel scope link src 10.200.160.101
local 10.200.160.101 dev em1 table local proto kernel scope host src 10.200.160.101
broadcast 10.200.160.255 dev em1 table local proto kernel scope link src 10.200.160.101
broadcast 127.0.0.0 dev lo table local proto kernel scope link src 127.0.0.1
local 127.0.0.0/8 dev lo table local proto kernel scope host src 127.0.0.1
local 127.0.0.1 dev lo table local proto kernel scope host src 127.0.0.1
broadcast 127.255.255.255 dev lo table local proto kernel scope link src 127.0.0.1
fe80::/64 dev em1 proto kernel metric 256 mtu 9216
fe80::/64 dev p2p1 proto kernel metric 256
unreachable default dev lo table unspec proto kernel metric 4294967295 error -101
local ::1 dev lo table local proto none metric 0
local fe80::d294:66ff:fe1c:6c81 dev lo table local proto none metric 0
local fe80::d294:66ff:fe1c:6c85 dev lo table local proto none metric 0
ff00::/8 dev em3 table local metric 256
ff00::/8 dev em4 table local metric 256
ff00::/8 dev p2p2 table local metric 256
ff00::/8 dev em1 table local metric 256 mtu 9216
ff00::/8 dev p2p1 table local metric 256
ff00::/8 dev em2 table local metric 256 mtu 9216
unreachable default dev lo table unspec proto kernel metric 4294967295 error -101
""".strip()

IFCFG_HIT = """
DEVICE="eth0"
BOOTPROTO="static"
GATEWAY="10.8.132.250"
IPADDR="192.168.23.111"
IPV6INIT="yes"
MTU="1500"
NETMASK="255.255.0.0"
NM_CONTROLLED="no"
ONBOOT="yes"
TYPE="Ethernet"
""".strip()

IFCFG_NO_HIT = """
DEVICE="eth0"
BOOTPROTO="static"
IPADDR="192.168.23.111"
IPV6INIT="yes"
MTU="1500"
NETMASK="255.255.0.0"
NM_CONTROLLED="no"
ONBOOT="yes"
TYPE="Ethernet"
""".strip()


@archive_provider(no_def_route.report)
def integration_test_hit():

    bad_env = InputData("Bad_environment_hit_1")
    bad_env.add(Specs.ip_route_show_table_all, ROUTE_TABLE_HIT)
    bad_env.add(Specs.ifcfg, IFCFG_HIT, path="etc/sysconfig/network-scripts/ifcfg-eth0")
    expected = make_fail(no_def_route.ERROR_KEY,
                             kcs=no_def_route.KCS_LINK,
                             interfaces=['eth0'])
    yield bad_env, expected


@archive_provider(no_def_route.report)
def integration_test_no_hit():

    # Default route present
    good_env = InputData("Good_environment_no_hit_1_default_route_present")
    good_env.add(Specs.ip_route_show_table_all, ROUTE_TABLE_NO_HIT)
    good_env.add(Specs.ifcfg, IFCFG_HIT, path="etc/sysconfig/network-scripts/ifcfg-eth0")
    yield good_env, None

    # No active interfaces
    good_env = InputData("Good_environment_no_hit_2_no_active_interfaces")
    good_env.add(Specs.ip_route_show_table_all, ROUTE_TABLE_HIT)
    good_env.add(Specs.ifcfg, IFCFG_NO_HIT, path="etc/sysconfig/network-scripts/ifcfg-eth0")
    yield good_env, None
