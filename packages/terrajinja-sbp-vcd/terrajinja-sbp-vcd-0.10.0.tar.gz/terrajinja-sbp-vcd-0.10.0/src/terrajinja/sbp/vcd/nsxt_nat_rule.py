from dataclasses import dataclass, asdict

from constructs import Construct

from terrajinja.imports.vcd.nsxt_nat_rule import NsxtNatRule
from .nsxt_app_port_profile import SbpVcdNsxtAppPortProfile


class SbpVcdNsxtNatRuleEmptyRule(Exception):
    """rules was empty where it should not"""


class SbpVcdNsxtNatRuleTypeNotDefined(Exception):
    """type was empty where it should not"""


class SbpVcdNsxtNatRuleRequiredParameterIsMissing(Exception):
    """required parameter is missing were it should not"""


@dataclass(frozen=True)
class SbpVcdNsxtNatRuleType:
    @property
    def allowed_types(self) -> list[str]:
        return ['NO_SNAT', 'SNAT', 'DNAT']


@dataclass(frozen=True)
class SbpVcdNsxtNatRuleDefaultPriority:
    nosnat: int = 1000
    snat: int = 2000
    dnat: int = 3000


@dataclass(frozen=True)
class SbpVcdNsxtNatRuleDefaultLifecycle:
    create_before_destroy: bool = True

    @property
    def settings(self) -> dict:
        return asdict(self)


@dataclass(frozen=True)
class SbpVcdNsxtNatRuleParser:
    scope: Construct
    ns: str
    edge_gateway_id: str  # required for app_port_profile, nat_rule
    vcd_org_vdc: str  # required for app_port_profile
    environment: str
    nat_rules: list[dict]

    @staticmethod
    def rule_name(priority: int, prefix: str, source: str, destination: str, port: int = None) -> str:
        name = f'P{priority}_{prefix}_{source}_to_{destination}'
        if port:
            name = name + f'_{port}'
        return name.upper().replace('-', '_')

    @staticmethod
    def validate_required_params(rule: dict, required_params: list):
        for param in required_params:
            result = rule.get(param)
            if not result:
                raise SbpVcdNsxtNatRuleRequiredParameterIsMissing(f"{param} is not defined in rule: {rule}")

    @property
    def nosnat_rules(self) -> list[dict]:
        nosnat_rules_list = []
        for rule in self.nat_rules:
            if rule['type'].upper() == 'NO_SNAT':

                self.validate_required_params(rule,
                                              ['internal_address_name', 'internal_address',
                                               'destination_address_name', 'destination_address'])

                priority = rule.get('priority')
                if not priority:
                    priority = SbpVcdNsxtNatRuleDefaultPriority.nosnat

                rule_name = self.rule_name(
                    priority=priority,
                    prefix=rule['type'],
                    source=rule.get('internal_address_name'),
                    destination=rule.get('destination_address_name')
                )

                lifecycle = rule.get('lifecycle', SbpVcdNsxtNatRuleDefaultLifecycle().settings)

                new_rule = {
                    'id_': rule_name,
                    'name': rule_name,
                    'snat_destination_address': rule.get('destination_address'),
                    'internal_address': rule.get('internal_address'),
                    'rule_type': rule.get('type'),
                    'priority': priority,
                    'lifecycle': lifecycle
                }
                nosnat_rules_list.append(new_rule)

        return nosnat_rules_list

    @property
    def snat_rules(self) -> list[dict]:
        snat_rules_list = []
        for rule in self.nat_rules:
            if rule['type'].upper() == 'SNAT':

                self.validate_required_params(rule,
                                              ['internal_address_name', 'internal_address',
                                               'firewall_address_name', 'firewall_address'])

                priority = rule.get('priority')
                if not priority:
                    priority = SbpVcdNsxtNatRuleDefaultPriority.snat

                rule_name = self.rule_name(
                    priority=priority,
                    prefix='OUT',
                    source=rule.get('internal_address_name'),
                    destination=rule.get('destination_address_name', rule.get('firewall_address_name'))
                )

                lifecycle = rule.get('lifecycle', SbpVcdNsxtNatRuleDefaultLifecycle().settings)

                new_rule = {
                    'id_': rule_name,
                    'name': rule_name,
                    'external_address': rule.get('firewall_address'),
                    'snat_destination_address': rule.get('destination_address'),
                    'internal_address': rule.get('internal_address'),
                    'rule_type': rule.get('type'),
                    'priority': priority,
                    'lifecycle': lifecycle
                }
                # print(f"DEBUG: internal_address {new_rule}")
                snat_rules_list.append(new_rule)

        return snat_rules_list

    @property
    def dnat_rules(self) -> list[dict]:
        dnat_rules_list = []
        for rule in self.nat_rules:
            if rule['type'].upper() == 'DNAT':

                self.validate_required_params(rule,
                                              ['firewall_address_name', 'firewall_address',
                                               'firewall_port', 'destination_address_name', 'destination_address'])

                priority = rule.get('priority')
                if not priority:
                    priority = SbpVcdNsxtNatRuleDefaultPriority.dnat

                rule_name = self.rule_name(
                    priority=priority,
                    prefix='IN',
                    source=rule.get('firewall_address_name'),
                    destination=rule.get('destination_address_name'),
                    port=rule.get('firewall_port')
                )

                lifecycle = rule.get('lifecycle', SbpVcdNsxtNatRuleDefaultLifecycle().settings)

                new_rule = {
                    'id_': rule_name,
                    'name': rule_name,
                    'external_address': rule.get('firewall_address'),
                    'dnat_external_port': str(rule['firewall_port']),
                    'internal_address': rule.get('destination_address'),
                    'rule_type': rule.get('type'),
                    'priority': priority,
                    'lifecycle': lifecycle
                }

                destination_port = rule.get('destination_port')
                if destination_port:
                    new_rule['app_port_profile_id'] = SbpVcdNsxtAppPortProfile(
                        scope_=self.scope,
                        context_id=self.vcd_org_vdc,
                        environment=self.environment,
                        protocol=destination_port[0].get('protocol'),
                        port=destination_port[0].get('port')
                    ).id
                dnat_rules_list.append(new_rule)

        return dnat_rules_list


class SbpVcdNsxtNatRule:
    """SBP version of vcd.nsxt_nat_rule"""

    def __init__(
            self,
            scope: Construct,
            ns: str,
            edge_gateway_id: str,  # required for ip_set
            vcd_org_vdc: str,  # required for app_port_profile
            environment: str,
            rules: list[dict],
            **kwargs,
    ):
        """Enhances the original vcd.nsxt_nat_rule
            Ensures that only one ip set is created before creating nat rules where applicable

        Args:
            scope (Construct): Cdktf App
            id (str): uniq name of the resource

        Original:
            https://registry.terraform.io/providers/vmware/vcd/latest/docs/resources/nsxt_nat_rule
        """

        parsed = SbpVcdNsxtNatRuleParser(
            scope=scope,
            ns=ns,
            edge_gateway_id=edge_gateway_id,
            vcd_org_vdc=vcd_org_vdc,
            environment=environment,
            nat_rules=rules,
        )

        if not all(r for r in rules):
            raise SbpVcdNsxtNatRuleEmptyRule("an empty rule is defined (null)")

        allowed_types = SbpVcdNsxtNatRuleType().allowed_types

        for rule in rules:
            rule_type = rule.get('type')
            if rule_type not in allowed_types:
                raise SbpVcdNsxtNatRuleTypeNotDefined(
                    f"Type is '{rule_type}' expected one off {allowed_types}  in rule {rule}")

        for nosnat_rule in parsed.nosnat_rules:
            # call the original resource
            NsxtNatRule(scope=scope,
                        edge_gateway_id=edge_gateway_id,
                        **nosnat_rule)

        for snat_rule in parsed.snat_rules:
            # call the original resource
            NsxtNatRule(scope=scope,
                        edge_gateway_id=edge_gateway_id,
                        **snat_rule)

        for dnat_rule in parsed.dnat_rules:
            # call the original resource
            NsxtNatRule(scope=scope,
                        edge_gateway_id=edge_gateway_id,
                        **dnat_rule)
