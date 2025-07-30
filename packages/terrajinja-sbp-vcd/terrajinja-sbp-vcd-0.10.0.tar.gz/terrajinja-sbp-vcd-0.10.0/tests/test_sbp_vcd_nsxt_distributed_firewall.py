import json

import pytest
from cdktf import Testing

from src.terrajinja.sbp.vcd.nsxt_distributed_firewall import SbpVcdNsxtDistributedFirewall, \
    DuplicateDistributedFirewallRuleName, EmptyDistributedFirewallRule
from .helper import stack, has_resource, has_resource_count


class TestSbpVcdNsxtDistributedFirewall:

    def test_resource_valid_source_dest(self, stack):
        rules = [
            {
                'source_address_name': 'source_distributed1',
                'source_address': "127.0.0.1",
                'destination_address_name': 'source_distributed1',
                'destination_address': "127.0.0.1",
            },
            {
                'source_address_name': 'source_distributed2',
                'source_address': ["127.0.0.1"],
                'destination_address_name': 'source_distributed2',
                'destination_address': ["127.0.0.1"],
            },
        ]
        SbpVcdNsxtDistributedFirewall(
            scope=stack,
            ns="firewall_rule",
            edge_gateway_id="id",
            vcd_org_vdc="id",
            vdc_group_id="id",
            environment="env",
            rules=rules,
        )
        synthesized = Testing.synth(stack)
        j = json.loads(synthesized)

        has_resource(synthesized, "vcd_nsxt_distributed_firewall")
        has_resource(synthesized, "vcd_nsxt_ip_set")
        # we should have 2 rules
        has_resource_count(synthesized, "vcd_nsxt_ip_set", 2)
        # we should have 2 ip sets from us + 1 deny
        assert len(j['resource']['vcd_nsxt_distributed_firewall']['firewall_rule']['rule']) == 3
        # first rule should have destination id formatted
        assert j['resource']['vcd_nsxt_distributed_firewall']['firewall_rule']['rule'][0]['destination_ids'][
                   0] == "${vcd_nsxt_ip_set.SOURCE_DISTRIBUTED1.id}"
        # first rule should have source id formatted
        assert j['resource']['vcd_nsxt_distributed_firewall']['firewall_rule']['rule'][0]['source_ids'][
                   0] == "${vcd_nsxt_ip_set.SOURCE_DISTRIBUTED1.id}"
        # must be True in order to force update of firewall before removing ip_sets or app_profile
        assert j['resource']['vcd_nsxt_distributed_firewall']['firewall_rule']['lifecycle'][
            'create_before_destroy']
        # TODO: check for default deny

    def test_resource_duplicate_source_dest(self, stack):
        # stack = TerraformStack(Testing.app(), "stack")

        rules = [
            {
                'source_address_name': 'source_distributed_duplicate1',
                'source_address': "127.0.0.1",
                'destination_address_name': 'source_distributed_duplicate1',
                'destination_address': "127.0.0.1",
            },
            {
                'source_address_name': 'source_distributed_duplicate1',
                'source_address': ["127.0.0.1"],
                'destination_address_name': 'source_distributed_duplicate1',
                'destination_address': ["127.0.0.1"],
            },
        ]
        with pytest.raises(DuplicateDistributedFirewallRuleName) as context:
            SbpVcdNsxtDistributedFirewall(
                scope=stack,
                ns="firewall_rule",
                edge_gateway_id="id",
                vcd_org_vdc="id",
                vdc_group_id="id",
                environment="env",
                rules=rules,
            )
        assert "the following rule(s) have been defined twice" in str(context.value)

    def test_resource_empty_rule(self, stack):
        rules = [
            {
                'source_address_name': 'source_distributed_empty',
                'source_address': "127.0.0.1",
                'destination_address_name': 'source_distributed_empty',
                'destination_address': "127.0.0.1",
            },
            {},
        ]
        with pytest.raises(EmptyDistributedFirewallRule) as context:
            SbpVcdNsxtDistributedFirewall(
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
