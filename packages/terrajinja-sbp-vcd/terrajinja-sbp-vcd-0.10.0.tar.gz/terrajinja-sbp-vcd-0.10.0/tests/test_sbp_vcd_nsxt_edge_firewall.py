import json

import pytest
from cdktf import Testing

from src.terrajinja.sbp.vcd.nsxt_edge_firewall import SbpVcdNsxtEdgeFirewall, \
    DuplicateEdgeFirewallRuleName, EmptyEdgeFirewallRule
from .helper import stack, has_resource, has_resource_count


class TestSbpVcdNsxtEdgeFirewall:

    def test_resource_valid_source_dest(self, stack):
        rules = [
            {
                'source_address_name': 'source_edge1',
                'source_address': "127.0.0.1",
                'destination_address_name': 'source_edge1',
                'destination_address': "127.0.0.1",
            },
            {
                'source_address_name': 'source_edge2',
                'source_address': ["127.0.0.1"],
                'destination_address_name': 'source_edge2',
                'destination_address': ["127.0.0.1"],
            },
        ]
        SbpVcdNsxtEdgeFirewall(
            scope=stack,
            ns="firewall_rule",
            edge_gateway_id="id",
            vcd_org_vdc="id",
            environment="env",
            rules=rules,
        )
        synthesized = Testing.synth(stack)
        j = json.loads(synthesized)

        has_resource(synthesized, "vcd_nsxt_firewall")
        has_resource(synthesized, "vcd_nsxt_ip_set")
        # we should have 2 ip sets
        has_resource_count(synthesized, "vcd_nsxt_ip_set", 2)
        # we should have 3 rules (default deny included)
        assert len(j['resource']['vcd_nsxt_firewall']['firewall_rule']['rule']) == 3
        # first rule should have destination id formatted
        assert j['resource']['vcd_nsxt_firewall']['firewall_rule']['rule'][0]['destination_ids'][
                   0] == "${vcd_nsxt_ip_set.SOURCE_EDGE1.id}"
        # first rule should have source id formatted
        assert j['resource']['vcd_nsxt_firewall']['firewall_rule']['rule'][0]['source_ids'][
                   0] == "${vcd_nsxt_ip_set.SOURCE_EDGE1.id}"
        # must be True in order to force update of firewall before removing ip_sets or app_profile
        assert j['resource']['vcd_nsxt_firewall']['firewall_rule']['lifecycle'][
            'create_before_destroy']

    def test_resource_duplicate_source_dest(self, stack):
        # stack = TerraformStack(Testing.app(), "stack")

        rules = [
            {
                'source_address_name': 'source_edge_duplicate1',
                'source_address': "127.0.0.1",
                'destination_address_name': 'source_edge_duplicate1',
                'destination_address': "127.0.0.1",
            },
            {
                'source_address_name': 'source_edge_duplicate1',
                'source_address': ["127.0.0.1"],
                'destination_address_name': 'source_edge_duplicate1',
                'destination_address': ["127.0.0.1"],
            },
        ]
        with pytest.raises(DuplicateEdgeFirewallRuleName) as context:
            SbpVcdNsxtEdgeFirewall(
                scope=stack,
                ns="firewall_rule",
                edge_gateway_id="id",
                vcd_org_vdc="id",
                environment="env",
                rules=rules,
            )
        assert "the following rule(s) have been defined twice" in str(context.value)

    def test_resource_empty_rule(self, stack):
        rules = [
            {
                'source_address_name': 'source_edge_empty',
                'source_address': "127.0.0.1",
                'destination_address_name': 'source1',
                'destination_address': "127.0.0.1",
            },
            {},
        ]
        with pytest.raises(EmptyEdgeFirewallRule) as context:
            SbpVcdNsxtEdgeFirewall(
                scope=stack,
                ns="firewall_rule",
                edge_gateway_id="id",
                vcd_org_vdc="id",
                vdc_group_id="id",
                environment="env",
                rules=rules,
            )
        assert "an empty rule was defined" in str(context.value)


if __name__ == "__main__":
    pytest.main()
