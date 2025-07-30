import collections

from constructs import Construct

from terrajinja.imports.vcd.nsxt_distributed_firewall import NsxtDistributedFirewall
from .nsxt_firewall_rule_parser import SbpVcdNsxtFirewallRuleParser


class DuplicateDistributedFirewallRuleName(Exception):
    """rules with the same name has already been defined"""


class EmptyDistributedFirewallRule(Exception):
    """rules was empty where it should not"""


class SbpVcdNsxtDistributedFirewall(NsxtDistributedFirewall):
    """SBP version of vcd.nsxt_distributed_firewall"""

    def __init__(
            self,
            scope: Construct,
            ns: str,
            rules: list[dict],
            environment: str,  # required for ip_set
            edge_gateway_id: str,  # required for ip_set
            vcd_org_vdc: str,  # required for app_port_profile
            **kwargs,
    ):
        """Enhances the original vcd.nsxt_distributed_firewall
            Ensures that only one ip set/app port profile is created before creating firewall rules

        Args:
            scope (Construct): Cdktf App
            id (str): uniq name of the resource

        Original:
            https://registry.terraform.io/providers/vmware/vcd/latest/docs/resources/nsxt_distributed_firewall
        """

        # check for empty rules
        if not all(r for r in rules):
            raise EmptyDistributedFirewallRule("an empty rule was defined (null)")

        rule_set = []
        for rule in rules:
            try:
                rule_set.append(
                    SbpVcdNsxtFirewallRuleParser(
                        scope=scope,
                        ns=ns,
                        edge_gateway_id=edge_gateway_id,
                        vcd_org_vdc=vcd_org_vdc,
                        environment=environment,
                        **rule)
                )
            except Exception as e:
                raise Exception(f"error: {e} in rule: {rule}")

        # check for duplicate names
        names = [rule.name for rule in rule_set]
        duplicates = [item for item, count in collections.Counter(names).items() if count > 1]
        if duplicates:
            raise DuplicateDistributedFirewallRuleName(f"the following rule(s) have been defined twice: {duplicates}")

        # add a drop any at the end of the firewall rules
        rule_set.append(SbpVcdNsxtFirewallRuleParser(
            scope=scope,
            ns=ns,
            edge_gateway_id=edge_gateway_id,
            vcd_org_vdc=vcd_org_vdc,
            environment=environment,
            direction='IN_OUT',
            action="DROP",
            logging=True
        ))

        # call the original resource
        super().__init__(
            scope=scope,
            id_=ns,
            rule=[rule.parsed for rule in rule_set],
            lifecycle={'create_before_destroy': True},
            **kwargs,
        )
