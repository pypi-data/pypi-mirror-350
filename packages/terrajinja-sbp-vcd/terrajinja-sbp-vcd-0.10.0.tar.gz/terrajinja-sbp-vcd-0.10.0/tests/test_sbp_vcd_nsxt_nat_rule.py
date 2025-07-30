# import json

import pytest

from src.terrajinja.sbp.vcd.nsxt_nat_rule import SbpVcdNsxtNatRuleParser, SbpVcdNsxtNatRule, SbpVcdNsxtNatRuleTypeNotDefined, \
    SbpVcdNsxtNatRuleEmptyRule, SbpVcdNsxtNatRuleRequiredParameterIsMissing
from .helper import stack, has_resource, has_resource_count, has_resource_path_value

from cdktf import Testing

class TestSbpVcdNsxtNatRule:
    def test_nat_rule_empty_rule(self, stack):
        with pytest.raises(SbpVcdNsxtNatRuleEmptyRule) as context:
            new_rule = [
                {
                }
            ]
            result = SbpVcdNsxtNatRule(
                scope=stack,
                ns="nat_rule",
                edge_gateway_id="id",
                vcd_org_vdc="id",
                environment="env",
                rules=new_rule
            )
            _ = result
        # print(context.value)
        assert "an empty rule is defined (null)" in str(context.value)

    def test_nat_rule_type_not_defined(self, stack):
        with pytest.raises(SbpVcdNsxtNatRuleTypeNotDefined) as context:
            new_rule = [
                {
                    'internal_address_name': 'tla-env-source-dummy-hosts',
                    'internal_address': "192.168.1.10/31",
                    'firewall_address_name': 'tla-env-source',
                    'firewall_address': "203.0.113.0",
                    #'type': "SNAT"
                    #'type': "DNAT"
                    #'type': "NO_NAT"
                }
            ]
            result = SbpVcdNsxtNatRule(
                scope=stack,
                ns="nat_rule",
                edge_gateway_id="id",
                vcd_org_vdc="id",
                environment="env",
                rules=new_rule
            )
            _ = result
        # print(context.value)
        assert "Type is 'None' expected one off ['NO_SNAT', 'SNAT', 'DNAT']  in rule {" in str(context.value)

    def test_nat_rule_type_wrongly_defined(self, stack):
        with pytest.raises(SbpVcdNsxtNatRuleTypeNotDefined) as context:
            new_rule = [
                {
                    'internal_address_name': 'tla-env-source-dummy-hosts',
                    'internal_address': "192.168.1.10/31",
                    'firewall_address_name': 'tla-env-source',
                    'firewall_address': "203.0.113.0",
                    'type': "WRONG"
                }
            ]
            result = SbpVcdNsxtNatRule(
                scope=stack,
                ns="nat_rule",
                edge_gateway_id="id",
                vcd_org_vdc="id",
                environment="env",
                rules=new_rule
            )
            _ = result
        # print(context.value)
        assert "Type is 'WRONG' expected one off ['NO_SNAT', 'SNAT', 'DNAT']  in rule {" in str(context.value)

class TestSbpVcdNsxtNatRuleParserNoSnat:

    def test_nosnat_rule_cdktf_synthesized(self, stack):
        new_rule = [
            {
                'internal_address_name': 'tla-env1',
                'internal_address': "192.168.211.0/24",
                'destination_address_name': 'tla-env2',
                'destination_address': "192.168.212.0/24",
                'type': "NO_SNAT"
            }
        ]

        SbpVcdNsxtNatRule(
            scope=stack,
            ns="nat_rule",
            edge_gateway_id="id",
            vcd_org_vdc="id",
            environment="env",
            rules=new_rule
        )
        synthesized = Testing.synth(stack)
        # j = json.loads(synthesized)

        has_resource(synthesized, "vcd_nsxt_nat_rule")
        has_resource_count(synthesized, "vcd_nsxt_nat_rule", 1)
        has_resource_path_value(synthesized, "vcd_nsxt_nat_rule", "P1000_NO_SNAT_TLA_ENV1_TO_TLA_ENV2", "name",
                                "P1000_NO_SNAT_TLA_ENV1_TO_TLA_ENV2")
        has_resource_path_value(synthesized, "vcd_nsxt_nat_rule", "P1000_NO_SNAT_TLA_ENV1_TO_TLA_ENV2", "internal_address",
                                "192.168.211.0/24")
        has_resource_path_value(synthesized, "vcd_nsxt_nat_rule", "P1000_NO_SNAT_TLA_ENV1_TO_TLA_ENV2", "snat_destination_address",
                                "192.168.212.0/24")
        has_resource_path_value(synthesized, "vcd_nsxt_nat_rule", "P1000_NO_SNAT_TLA_ENV1_TO_TLA_ENV2", "rule_type",
                                "NO_SNAT")
        has_resource_path_value(synthesized, "vcd_nsxt_nat_rule", "P1000_NO_SNAT_TLA_ENV1_TO_TLA_ENV2", "priority",
                                1000) # default function results
        has_resource_path_value(synthesized, "vcd_nsxt_nat_rule", "P1000_NO_SNAT_TLA_ENV1_TO_TLA_ENV2", "lifecycle",
                                {'create_before_destroy': True}) # default function results

    @pytest.mark.parametrize(
        "internal_address_name, internal_address, destination_address_name, destination_address",
        [
            # ('tla-env1', "192.168.211.0/24", 'tla-env2', "192.168.212.0/24"),
            (None, "192.168.211.0/24", 'tla-env2', "192.168.212.0/24"),
            ('tla-env1', None, 'tla-env2', "192.168.212.0/24"),
            ('tla-env1', "192.168.211.0/24", None, "192.168.212.0/24"),
            ('tla-env1', "192.168.211.0/24", 'tla-env2', None),
        ],
    )
    def test_nosnat_rule_missing_required_parameters(self, stack, internal_address_name, internal_address, destination_address_name, destination_address):
        new_rule = [
            {
                'internal_address_name': internal_address_name,
                'internal_address': internal_address,
                'destination_address_name': destination_address_name,
                'destination_address': destination_address,
                'type': "NO_SNAT"
            }
        ]
        with pytest.raises(SbpVcdNsxtNatRuleRequiredParameterIsMissing) as context:
            result = SbpVcdNsxtNatRuleParser(
                scope=stack,
                ns="nat_rule",
                edge_gateway_id="id",
                vcd_org_vdc="id",
                environment="env",
                nat_rules=new_rule
            )
            _ = result.nosnat_rules
        # retrieve parameter with none
        required_parameter = ', '.join(param for param, value in locals().items() if value is None)
        assert f"{required_parameter} is not defined in rule: {new_rule[0]}" in str(context.value)
        # assert "is not defined in rule: " in str(context.value)
        # assert internal_address_name == "internal_address_name is not defined in rule: {'internal_address_name': None" in str(context.value)
        # assert "internal_address_name is not defined in rule: {'internal_address_name': None" in str(context.value)
        # assert "internal_address is not defined in rule: {'internal_address': None" in str(context.value)
        # assert "destination_address_name is not defined in rule: {'destination_address_name': None" in str(context.value)
        # assert "destination_address is not defined in rule: {'destination_address': None" in str(context.value)

    def test_nosnat_rule(self, stack):
        new_rule = [
            {
                'internal_address_name': 'tla-env1',
                'internal_address': "192.168.211.0/24",
                'destination_address_name': 'tla-env2',
                'destination_address': "192.168.212.0/24",
                'type': "NO_SNAT"
            }
        ]
        result = SbpVcdNsxtNatRuleParser(
            scope=stack,
            ns="nat_rule",
            edge_gateway_id="id",
            vcd_org_vdc="id",
            environment="env",
            nat_rules=new_rule
        )
        # print(f"DEBUG: {result.nosnat_rules}")
        assert result.nosnat_rules[0].get('name') == "P1000_NO_SNAT_TLA_ENV1_TO_TLA_ENV2"
        assert result.nosnat_rules[0].get('internal_address') == "192.168.211.0/24"
        assert result.nosnat_rules[0].get('snat_destination_address') == "192.168.212.0/24"
        assert result.nosnat_rules[0].get('rule_type') == "NO_SNAT"
        assert result.nosnat_rules[0].get('priority') == 1000 # default function results
        assert result.nosnat_rules[0].get('lifecycle') == {'create_before_destroy': True} # default function results

    def test_nosnat_rule_overwrite_priority(self, stack):
        new_rule = [
            {
                'internal_address_name': 'tla-env1',
                'internal_address': "192.168.211.0/24",
                'destination_address_name': 'tla-env2',
                'destination_address': "192.168.212.0/24",
                'type': "NO_SNAT",
                'priority': 1001
            }
        ]
        result = SbpVcdNsxtNatRuleParser(
            scope=stack,
            ns="nat_rule",
            edge_gateway_id="id",
            vcd_org_vdc="id",
            environment="env",
            nat_rules=new_rule
        )
        # print(f"DEBUG: {result.nosnat_rules[0].get('priority')}")
        assert result.nosnat_rules[0].get('priority') == 1001

    def test_nosnat_rule_overwrite_default_lifecycle(self, stack):
        new_rule = [
            {
                'internal_address_name': 'tla-env1',
                'internal_address': "192.168.211.0/24",
                'destination_address_name': 'tla-env2',
                'destination_address': "192.168.212.0/24",
                'type': "NO_SNAT",
                'priority': 1001,
                'lifecycle': {'create_before_destroy': False}
            }
        ]
        result = SbpVcdNsxtNatRuleParser(
            scope=stack,
            ns="nat_rule",
            edge_gateway_id="id",
            vcd_org_vdc="id",
            environment="env",
            nat_rules=new_rule
        )
        # print(f"DEBUG: {result.nosnat_rules[0].get('lifecycle')}")
        assert result.nosnat_rules[0].get('lifecycle') == {'create_before_destroy': False}

class TestSbpVcdNsxtNatRuleParserSnat:

    def test_snat_rule_cdktf_synthesized(self, stack):
        new_rule = [
            {
                'internal_address_name': 'tla-env-source-dummy-hosts',
                'internal_address': "192.168.1.10/31",
                'firewall_address_name': 'tla-env-source',
                'firewall_address': "203.0.113.0",
                'destination_address': "192.168.1.15/32",
                'type': "SNAT"
            }
        ]

        SbpVcdNsxtNatRule(
            scope=stack,
            ns="nat_rule",
            edge_gateway_id="id",
            vcd_org_vdc="id",
            environment="env",
            rules=new_rule
        )
        synthesized = Testing.synth(stack)
        # j = json.loads(synthesized)
        # print(f"DEBUG: synthesized {synthesized}")

        has_resource(synthesized, "vcd_nsxt_nat_rule")
        has_resource_count(synthesized, "vcd_nsxt_nat_rule", 1)
        has_resource(synthesized, "vcd_nsxt_nat_rule")
        has_resource_count(synthesized, "vcd_nsxt_nat_rule", 1)
        has_resource_path_value(synthesized, "vcd_nsxt_nat_rule", "P2000_OUT_TLA_ENV_SOURCE_DUMMY_HOSTS_TO_TLA_ENV_SOURCE", "name",
                                 "P2000_OUT_TLA_ENV_SOURCE_DUMMY_HOSTS_TO_TLA_ENV_SOURCE")
        has_resource_path_value(synthesized, "vcd_nsxt_nat_rule", "P2000_OUT_TLA_ENV_SOURCE_DUMMY_HOSTS_TO_TLA_ENV_SOURCE", "internal_address",
                                "192.168.1.10/31")
        has_resource_path_value(synthesized, "vcd_nsxt_nat_rule", "P2000_OUT_TLA_ENV_SOURCE_DUMMY_HOSTS_TO_TLA_ENV_SOURCE", "snat_destination_address",
                                "192.168.1.15/32")
        has_resource_path_value(synthesized, "vcd_nsxt_nat_rule", "P2000_OUT_TLA_ENV_SOURCE_DUMMY_HOSTS_TO_TLA_ENV_SOURCE", "rule_type",
                                "SNAT")
        has_resource_path_value(synthesized, "vcd_nsxt_nat_rule", "P2000_OUT_TLA_ENV_SOURCE_DUMMY_HOSTS_TO_TLA_ENV_SOURCE", "priority",
                                2000) # default function results
        has_resource_path_value(synthesized, "vcd_nsxt_nat_rule", "P2000_OUT_TLA_ENV_SOURCE_DUMMY_HOSTS_TO_TLA_ENV_SOURCE", "lifecycle",
                                {'create_before_destroy': True} ) # default function results

    @pytest.mark.parametrize(
        "internal_address_name, internal_address, firewall_address_name, firewall_address",
        [
            # ('tla-env-source-dummy-hosts', "192.168.1.10/31", 'tla-env-source', "203.0.113.0"),
            (None, "192.168.1.10/31", 'tla-env-source', "203.0.113.0"),
            ('tla-env-source-dummy-hosts', None, 'tla-env-source', "203.0.113.0"),
            ('tla-env-source-dummy-hosts', "192.168.1.10/31", None, "203.0.113.0"),
            ('tla-env-source-dummy-hosts', "192.168.1.10/31", 'tla-env-source', None),
        ],
    )
    def test_snat_rule_missing_required_parameters(self, stack, internal_address_name, internal_address, firewall_address_name, firewall_address):
        new_rule = [
            {
                'internal_address_name': internal_address_name,
                'internal_address': internal_address,
                'firewall_address_name': firewall_address_name,
                'firewall_address': firewall_address,
                'destination_address': "192.168.1.15/32",
                'type': "SNAT"
            }
        ]
        with pytest.raises(SbpVcdNsxtNatRuleRequiredParameterIsMissing) as context:
            result = SbpVcdNsxtNatRuleParser(
                scope=stack,
                ns="nat_rule",
                edge_gateway_id="id",
                vcd_org_vdc="id",
                environment="env",
                nat_rules=new_rule
            )
            _ = result.snat_rules
        # retrieve parameter with none
        required_parameter = ', '.join(param for param, value in locals().items() if value is None)
        assert f"{required_parameter} is not defined in rule: {new_rule[0]}" in str(context.value)
        # assert "is not defined in rule: " in str(context.value)
        # assert "internal_address_name is not defined in rule: {'internal_address_name': None" in str(context.value)
        # assert "internal_address is not defined in rule: {'internal_address': None" in str(context.value)
        # assert "firewall_address_name is not defined in rule: {'firewall_address_name': None" in str(context.value)
        # assert "firewall_address is not defined in rule: {'firewall_address': None" in str(context.value)

    def test_snat_rule(self, stack):
        new_rule = [
            {
                'internal_address_name': 'tla-env-source-dummy-hosts',
                'internal_address': "192.168.1.10/31",
                'firewall_address_name': 'tla-env-source',
                'firewall_address': "203.0.113.0",
                'type': "SNAT"
            }
        ]
        result = SbpVcdNsxtNatRuleParser(
            scope=stack,
            ns="nat_rule",
            edge_gateway_id="id",
            vcd_org_vdc="id",
            environment="env",
            nat_rules=new_rule
        )
        # print(f"DEBUG: {result.snat_rules}")
        assert result.snat_rules[0].get('name') == "P2000_OUT_TLA_ENV_SOURCE_DUMMY_HOSTS_TO_TLA_ENV_SOURCE"
        assert result.snat_rules[0].get('internal_address') == "192.168.1.10/31"
        assert result.snat_rules[0].get('rule_type') == "SNAT"
        assert result.snat_rules[0].get('priority') == 2000 # default function results
        assert result.snat_rules[0].get('lifecycle') == {'create_before_destroy': True} # default function results

    def test_snat_rule_with_snat_destination_address(self, stack):
        new_rule = [
            {
                'internal_address_name': 'tla-env-source-dummy-hosts',
                'internal_address': "192.168.1.10/31",
                'firewall_address_name': 'tla-env-source',
                'firewall_address': "203.0.113.0",
                'destination_address': "192.168.1.15/32",
                'type': "SNAT"
            }
        ]
        result = SbpVcdNsxtNatRuleParser(
            scope=stack,
            ns="nat_rule",
            edge_gateway_id="id",
            vcd_org_vdc="id",
            environment="env",
            nat_rules=new_rule
        )
        # print(f"DEBUG: {result.snat_rules}")
        assert result.snat_rules[0].get('name') == "P2000_OUT_TLA_ENV_SOURCE_DUMMY_HOSTS_TO_TLA_ENV_SOURCE"
        assert result.snat_rules[0].get('internal_address') == "192.168.1.10/31"
        assert result.snat_rules[0].get('snat_destination_address') == "192.168.1.15/32"
        assert result.snat_rules[0].get('rule_type') == "SNAT"
        assert result.snat_rules[0].get('priority') == 2000
        assert result.snat_rules[0].get('lifecycle') == {'create_before_destroy': True}

    def test_snat_rule_with_overwrite_priority(self, stack):
        new_rule = [
            {
                'internal_address_name': 'tla-env-source-dummy-hosts',
                'internal_address': "192.168.1.10/31",
                'firewall_address_name': 'tla-env-source',
                'firewall_address': "203.0.113.0",
                'destination_address': "192.168.1.15/32",
                'type': "SNAT",
                'priority': 2001
            }
        ]
        result = SbpVcdNsxtNatRuleParser(
            scope=stack,
            ns="nat_rule",
            edge_gateway_id="id",
            vcd_org_vdc="id",
            environment="env",
            nat_rules=new_rule
        )
        # print(f"DEBUG: {result.snat_rules[0].get('priority')}")
        assert result.snat_rules[0].get('priority') == 2001

    def test_snat_rule_overwrite_default_lifecycle(self, stack):
        new_rule = [
            {
                'internal_address_name': 'tla-env-source-dummy-hosts',
                'internal_address': "192.168.1.10/31",
                'firewall_address_name': 'tla-env-source',
                'firewall_address': "203.0.113.0",
                'destination_address': "192.168.1.15/32",
                'type': "SNAT",
                'lifecycle': {'create_before_destroy': False}
            }
        ]
        result = SbpVcdNsxtNatRuleParser(
            scope=stack,
            ns="nat_rule",
            edge_gateway_id="id",
            vcd_org_vdc="id",
            environment="env",
            nat_rules=new_rule
        )
        # print(f"DEBUG: {result.snat_rules[0].get('lifecycle')}")
        assert result.snat_rules[0].get('lifecycle') == {'create_before_destroy': False}

class TestSbpVcdNsxtNatRuleParserDnat:
    # used another port in this test because of @run_once. Tests will fail if the same port for app_port profile is used in other cases
    def test_dnat_rule_cdktf_synthesized(self, stack):
        new_rule = [
            {
                'firewall_address_name': 'tla-env-source',
                'firewall_address': "203.0.113.0",
                'firewall_port': 443,
                'destination_address_name': 'tla-env-source-dummy-hosts',
                'destination_address': "192.168.1.15/32",
                'type': "DNAT",
                'destination_port': [{'protocol': 'tcp', 'port': 443 }]
            }
        ]

        SbpVcdNsxtNatRule(
            scope=stack,
            ns="nat_rule",
            edge_gateway_id="id",
            vcd_org_vdc="id",
            environment="env",
            rules=new_rule
        )
        synthesized = Testing.synth(stack)
        # j = json.loads(synthesized)
        # print(f"DEBUG: synthesized {synthesized}")

        # dynamically name via class
        has_resource(synthesized, "vcd_nsxt_app_port_profile")
        has_resource_count(synthesized, "vcd_nsxt_app_port_profile", 1)
        has_resource_path_value(synthesized, "vcd_nsxt_app_port_profile", "ENV_TCP_443", "app_port",
                                [{'port': ['443'], 'protocol': 'TCP'}])

        # dynamically name via class
        has_resource(synthesized, "vcd_nsxt_nat_rule")
        has_resource_count(synthesized, "vcd_nsxt_nat_rule", 1)
        has_resource_path_value(synthesized, "vcd_nsxt_nat_rule", "P3000_IN_TLA_ENV_SOURCE_TO_TLA_ENV_SOURCE_DUMMY_HOSTS_443", "name",
                                "P3000_IN_TLA_ENV_SOURCE_TO_TLA_ENV_SOURCE_DUMMY_HOSTS_443")
        has_resource_path_value(synthesized, "vcd_nsxt_nat_rule", "P3000_IN_TLA_ENV_SOURCE_TO_TLA_ENV_SOURCE_DUMMY_HOSTS_443", "app_port_profile_id",
                                 "${vcd_nsxt_app_port_profile.ENV_TCP_443.id}")
        has_resource_path_value(synthesized, "vcd_nsxt_nat_rule", "P3000_IN_TLA_ENV_SOURCE_TO_TLA_ENV_SOURCE_DUMMY_HOSTS_443", "dnat_external_port",
                                "443")
        has_resource_path_value(synthesized, "vcd_nsxt_nat_rule", "P3000_IN_TLA_ENV_SOURCE_TO_TLA_ENV_SOURCE_DUMMY_HOSTS_443", "external_address",
                                "203.0.113.0")
        has_resource_path_value(synthesized, "vcd_nsxt_nat_rule", "P3000_IN_TLA_ENV_SOURCE_TO_TLA_ENV_SOURCE_DUMMY_HOSTS_443", "internal_address",
                                "192.168.1.15/32")
        has_resource_path_value(synthesized, "vcd_nsxt_nat_rule", "P3000_IN_TLA_ENV_SOURCE_TO_TLA_ENV_SOURCE_DUMMY_HOSTS_443", "rule_type",
                                "DNAT")
        has_resource_path_value(synthesized, "vcd_nsxt_nat_rule", "P3000_IN_TLA_ENV_SOURCE_TO_TLA_ENV_SOURCE_DUMMY_HOSTS_443", "priority",
                                3000) # default function results
        has_resource_path_value(synthesized, "vcd_nsxt_nat_rule", "P3000_IN_TLA_ENV_SOURCE_TO_TLA_ENV_SOURCE_DUMMY_HOSTS_443", "lifecycle",
                                {'create_before_destroy': True}) # default function results


    @pytest.mark.parametrize(
        "firewall_address_name, firewall_address, firewall_port, destination_address_name, destination_address",
        [
            # ('tla-env-source', "203.0.113.0", 443, "tla-env-source-dummy-hosts", "192.168.1.15/32"),
            (None, "203.0.113.0", 443, "tla-env-source-dummy-hosts", "192.168.1.15/32"),
            ('tla-env-source', None, 443, "tla-env-source-dummy-hosts", "192.168.1.15/32"),
            ('tla-env-source', "203.0.113.0", None, "tla-env-source-dummy-hosts", "192.168.1.15/32"),
            ('tla-env-source', "203.0.113.0", 443, None, "192.168.1.15/32"),
            ('tla-env-source', "203.0.113.0", 443, "tla-env-source-dummy-hosts", None),
        ],
    )
    def test_dnat_rule_missing_required_parameters(self, stack, firewall_address_name, firewall_address, firewall_port, destination_address_name, destination_address):
        new_rule = [
            {
                'firewall_address_name': firewall_address_name,
                'firewall_address': firewall_address,
                'firewall_port': firewall_port,
                'destination_address_name': destination_address_name,
                'destination_address': destination_address,
                'type': "DNAT",
                'destination_port': [{'protocol': 'tcp', 'port': 443 }]
            }
        ]
        with pytest.raises(SbpVcdNsxtNatRuleRequiredParameterIsMissing) as context:
            result = SbpVcdNsxtNatRuleParser(
                scope=stack,
                ns="nat_rule",
                edge_gateway_id="id",
                vcd_org_vdc="id",
                environment="env",
                nat_rules=new_rule
            )
            _ = result.dnat_rules
        # retrieve parameter with none
        required_parameter = ', '.join(param for param, value in locals().items() if value is None)
        assert f"{required_parameter} is not defined in rule: {new_rule[0]}" in str(context.value)
        # print(f"DEBUG: {none_param_name}"
        # assert "firewall_address_name is not defined in rule: {'firewall_address_name': None" in str(context.value)
        # assert "firewall_address is not defined in rule: {'firewall_address': None" in str(context.value)
        # assert "firewall_port is not defined in rule: {'firewall_port': None" in str(context.value)
        # assert "destination_address_name is not defined in rule: {'destination_address_name': None" in str(context.value)
        # assert "destination_address is not defined in rule: {'destination_address': None" in str(context.value)

    def test_dnat_rule(self, stack):
        new_rule = [
            {
                'firewall_address_name': 'tla-env-source',
                'firewall_address': "203.0.113.0",
                'firewall_port': 80,
                'destination_address_name': 'tla-env-source-dummy-hosts',
                'destination_address': "192.168.1.15/32",
                'type': "DNAT"
            }
        ]
        result = SbpVcdNsxtNatRuleParser(
            scope=stack,
            ns="nat_rule",
            edge_gateway_id="id",
            vcd_org_vdc="id",
            environment="env",
            nat_rules=new_rule
        )
        # print(f"DEBUG: {result.dnat_rules}")
        assert result.dnat_rules[0].get('name') == "P3000_IN_TLA_ENV_SOURCE_TO_TLA_ENV_SOURCE_DUMMY_HOSTS_80"
        assert result.dnat_rules[0].get('external_address') == "203.0.113.0"
        assert result.dnat_rules[0].get('dnat_external_port') == "80"
        assert result.dnat_rules[0].get('internal_address') == "192.168.1.15/32"
        assert result.dnat_rules[0].get('rule_type') == "DNAT"
        assert result.dnat_rules[0].get('priority') == 3000 # default function results
        assert result.dnat_rules[0].get('lifecycle') == {'create_before_destroy': True} # default function results

    def test_dnat_rule_with_app_port_profile_id(self, stack):
        new_rule = [
            {
                'firewall_address_name': 'tla-env-source',
                'firewall_address': "203.0.113.0",
                'firewall_port': 80,
                'destination_address_name': 'tla-env-source-dummy-hosts',
                'destination_address': "192.168.1.15/32",
                'type': "DNAT",
                'destination_port': [{'protocol': 'tcp', 'port': 80 }]
            }
        ]
        result = SbpVcdNsxtNatRuleParser(
            scope=stack,
            ns="nat_rule",
            edge_gateway_id="id",
            vcd_org_vdc="id",
            environment="env",
            nat_rules=new_rule
        )
        # print(f"DEBUG: {result.dnat_rules[0].get('app_port_profile_id')}")
        assert result.dnat_rules[0].get('app_port_profile_id').startswith('${TfToken[TOKEN.')

    def test_dnat_rule_with_overwrite_priority(self, stack):
        new_rule = [
            {
                'firewall_address_name': 'tla-env-source',
                'firewall_address': "203.0.113.0",
                'firewall_port': 80,
                'destination_address_name': 'tla-env-source-dummy-hosts',
                'destination_address': "192.168.1.15/32",
                'type': "DNAT",
                'priority': 3001
            }
        ]
        result = SbpVcdNsxtNatRuleParser(
            scope=stack,
            ns="nat_rule",
            edge_gateway_id="id",
            vcd_org_vdc="id",
            environment="env",
            nat_rules=new_rule
        )
        # print(f"DEBUG: {result.dnat_rules[0].get('priority')}")
        assert result.dnat_rules[0].get('priority') == 3001

    def test_dnat_rule_overwrite_default_lifecycle(self, stack):
        new_rule = [
            {
                'firewall_address_name': 'tla-env-source',
                'firewall_address': "203.0.113.0",
                'firewall_port': 80,
                'destination_address_name': 'tla-env-source-dummy-hosts',
                'destination_address': "192.168.1.15/32",
                'type': "DNAT",
                'lifecycle': {'create_before_destroy': False}
            }
        ]
        result = SbpVcdNsxtNatRuleParser(
            scope=stack,
            ns="nat_rule",
            edge_gateway_id="id",
            vcd_org_vdc="id",
            environment="env",
            nat_rules=new_rule
        )
        # print(f"DEBUG: {result.dnat_rules[0].get('lifecycle')}")
        assert result.dnat_rules[0].get('lifecycle') == {'create_before_destroy': False}

if __name__ == "__main__":
    pytest.main()