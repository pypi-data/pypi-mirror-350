from dataclasses import dataclass
from ipaddress import IPv4Network, IPv6Network, AddressValueError

from constructs import Construct

from terrajinja.imports.vcd.nsxt_ip_set import NsxtIpSet
from .decorators import run_once

global_sbp_vcd_nsxt_ip_set = {}


class IpAddressSetMismatch(Exception):
    """Ip addresses mismatch in set with the same name"""


class EmptyIpAddressesList(Exception):
    """Ip addresses list is empty"""


@dataclass(frozen=True)
class IpSet:
    name: str
    ip_addresses: []

    def __post_init__(self):
        if type(self.ip_addresses) is str:
            object.__setattr__(self, "ip_addresses", [self.ip_addresses])

        object.__setattr__(self, "name", self.name.upper())


@run_once(parameter_match=["name", "ip_addresses"])
class SbpVcdNsxtIpSet(NsxtIpSet):
    """SBP version of vcd.nsxt_ip_set"""

    def __init__(
            self,
            scope: Construct,
            name: str,
            ip_addresses: [list[str], str],
            ns: str = None,
            **kwargs,
    ):
        """Enhances the original vcd.nsxt_ip_set
            Ensures that only one ip set is created, and validates its use across the deployment

        Args:
            scope (Construct): Cdktf App
            id (str): uniq name of the resource

        Original:
            https://registry.terraform.io/providers/vmware/vcd/latest/docs/resources/nsxt_app_port_profile
        """

        # validate that we have ips
        if not ip_addresses:
            raise EmptyIpAddressesList(f"ip set named '{name}' contains no ip addresses")

        # use namer
        ip_set = IpSet(name, ip_addresses)

        # validate ips are correct
        for ip in ip_set.ip_addresses:
            try:
                IPv4Network(ip)
            except AddressValueError:
                try:
                    IPv6Network(ip)
                except AddressValueError:
                    raise AddressValueError(f"ip address defined does not appear to be ipv4 or ipv6: {ip}")

        # cache the resource, so we can return the pointers to the cached resource instead
        cache_name = f"nsxt_ip_set_{ip_set.name}"

        # if app profile is already defined, just return it instead of adding again
        if global_sbp_vcd_nsxt_ip_set.get(cache_name):
            old_ip_addresses = global_sbp_vcd_nsxt_ip_set.get(cache_name)
            if old_ip_addresses != ip_set.ip_addresses:
                raise IpAddressSetMismatch(
                    f"the sbp_nsxt_ip_set with the name '{name}' is defined twice with different ip_addresses"
                    f"({old_ip_addresses} vs: {ip_set.ip_addresses})"
                )

        if not ns:
            ns = ip_set.name

        # call the original resource
        super().__init__(
            scope=scope,
            id_=ns,
            name=ip_set.name,
            ip_addresses=ip_set.ip_addresses,
            **kwargs,
        )
        global_sbp_vcd_nsxt_ip_set[cache_name] = ip_addresses
