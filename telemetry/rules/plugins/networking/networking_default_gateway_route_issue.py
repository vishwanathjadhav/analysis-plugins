"""
Default gateway route disappeared after service restart
=======================================================

Configured default gateway address disappeared from IP routing table
after restarting `network.service` or server reboot. The issue occurs
when `NETWORK` parameter is assigned an incorrect value. The directive
`DEFROUTE=no` is used if the interface should never act as a default
gateway.

* Resolution:
   Remove the following directives if present in
   `/etc/sysconfig/network-scripts/ifcfg-XXX`.

    ```
    NETWORK=XX.XX.XX.XX
    ```

Impact: Network default gateway address cannot be added

* JIRA: https://projects.engineering.redhat.com/browse/CPSEARCH-3926
* KCS: https://access.redhat.com/solutions/705403
* Trigger conditions:
  1. IPADDR and GATEWAY present in ifcfg configuration
  2. Defualt route is absent
"""
from insights.core.plugins import condition, make_fail, rule
from insights.parsers.ifcfg import IfCFG
from insights.parsers.ip import RouteDevices

ERROR_KEY = "NO_DEFAULT_ROUTE_CONFIGURE"
KCS_LINK = "https://access.redhat.com/solutions/705403"


@condition(IfCFG)
def get_active_interfaces(nics):
    active_interfaces = []
    for nic in nics:
        if ('IPADDR' in nic) and ('GATEWAY' in nic):
            active_interfaces.append(nic.ifname)

    if active_interfaces:
        return active_interfaces


@condition(RouteDevices)
def no_default_route(routes):
    if not routes.defaults:
        return True


@rule(get_active_interfaces, no_default_route)
def report(inames, no_default_route):
    if all([inames, no_default_route]):
        return make_fail(ERROR_KEY,
                             kcs=KCS_LINK,
                             interfaces=inames)
