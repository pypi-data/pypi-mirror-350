from dataclasses import dataclass

from constructs import Construct

from terrajinja.imports.vcd.nsxt_app_port_profile import NsxtAppPortProfile
from .decorators import run_once


class InvalidProtocolName(Exception):
    """Invalid protocol name"""


@dataclass(frozen=True)
class AppPortProfile:
    environment: str
    protocol: str
    scope: str
    port: int = None

    def __post_init__(self):
        if self.protocol:
            object.__setattr__(self, "protocol", self.protocol.upper().replace("ICMPV", "ICMPv"))
            allowed_protocols = ["ICMPv4", "ICMPv6", "TCP", "UDP"]
            if self.protocol not in allowed_protocols:
                raise InvalidProtocolName(
                    f"protocol '{self.protocol} does not match one of the allowed protocols: {allowed_protocols}"
                )

    @property
    def name(self):
        return (
            f"{self.environment}_{self.protocol}_{self.port}".upper()
            if self.port
            else f"{self.environment}_{self.protocol}".upper()
        )

    @property
    def app_port(self):
        app_port_list = [
            {
                "protocol": self.protocol,
            }
        ]
        if self.port:
            app_port_list[0]["port"] = [str(self.port)]
        return app_port_list


@run_once(parameter_match=["environment", "port", "protocol"])
class SbpVcdNsxtAppPortProfile(NsxtAppPortProfile):
    """SBP version of vcd.nsxt_app_port_profile"""

    def __init__(
            self,
            scope_: Construct,
            environment: str,
            protocol: str,
            scope: str = "TENANT",
            port: int = None,
            ns: str = None,
            **kwargs,
    ):
        """Enhances the original vcd.nsxt_app_port_profile

        Args:
            scope (Construct): Cdktf App
            id (str): uniq name of the resource
            result_cache (dict): cache of all collected resource outputs so far
            environment (str): environment to create the app_port_profile in

        Original:
            https://registry.terraform.io/providers/vmware/vcd/latest/docs/resources/nsxt_app_port_profile
        """

        app_port_profile = AppPortProfile(environment=environment, protocol=protocol, port=port, scope=scope)

        if not ns:
            ns = app_port_profile.name

        # call the original resource
        try:
            super().__init__(
                scope_=scope_,
                scope=app_port_profile.scope,
                id_=ns,
                name=app_port_profile.name,
                app_port=app_port_profile.app_port,
                **kwargs,
            )
        except Exception as e:
            raise Exception(
                f"error: {e} on app port profile with environment:{environment}, protocol:{protocol}, port: {port}")
