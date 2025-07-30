from dataclasses import dataclass

from constructs import Construct

from .nsxt_app_port_profile import SbpVcdNsxtAppPortProfile
from .nsxt_ip_set import SbpVcdNsxtIpSet


class FirewallRuleParserNoProtocolDefined(Exception):
    """No protocol was specified in firewall rule"""


@dataclass(frozen=True)
class SbpVcdNsxtFirewallRuleParser:
    scope: Construct
    ns: str
    edge_gateway_id: str  # required for ip_set
    vcd_org_vdc: str  # required for app_port_profile
    environment: str
    direction: str = "IN_OUT"
    action: str = "ALLOW"
    ip_protocol: str = "IPV4"
    logging: bool = False
    destination_port: list[dict] = None
    source_address_name: str = None
    source_address: list[str] = None
    destination_address_name: str = None
    destination_address: list[str] = None

    @property
    def name(self):
        source_name = "Any"
        if self.source_address_name:
            source_name = self.source_address_name
        destination_name = "Any"
        if self.destination_address_name:
            destination_name = self.destination_address_name

        return '_'.join([source_name, "to", destination_name]).upper().replace('-', '_')

    @property
    def parsed(self) -> dict:
        parsed = {
            'name': self.name,
            'direction': self.direction.upper(),
            'ipProtocol': self.ip_protocol.upper(),
            'action': self.action.upper(),
            'logging': self.logging,
        }
        if self.source_address_name:
            parsed['sourceIds'] = [SbpVcdNsxtIpSet(
                scope=self.scope,
                edge_gateway_id=self.edge_gateway_id,
                name=self.source_address_name,
                ip_addresses=self.source_address
            ).id]
        if self.destination_address_name:
            parsed['destinationIds'] = [SbpVcdNsxtIpSet(
                scope=self.scope,
                edge_gateway_id=self.edge_gateway_id,
                name=self.destination_address_name,
                ip_addresses=self.destination_address
            ).id]
        if self.destination_port:
            ports_with_no_protocol = [port for port in self.destination_port if not port.get('protocol')]
            if ports_with_no_protocol:
                raise FirewallRuleParserNoProtocolDefined(
                    f"no 'protocol' defined with destination_port in rule '{self.name}'"
                    "values:{ports_with_no_protocol}")
            parsed['appPortProfileIds'] = [SbpVcdNsxtAppPortProfile(
                scope_=self.scope,
                context_id=self.vcd_org_vdc,
                environment=self.environment,
                protocol=port.get('protocol'),
                port=port.get('port'),
            ).id
                                           for port in self.destination_port]
        return parsed
