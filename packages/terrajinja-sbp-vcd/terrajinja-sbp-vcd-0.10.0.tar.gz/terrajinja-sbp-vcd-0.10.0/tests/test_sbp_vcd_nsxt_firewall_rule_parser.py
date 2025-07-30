import pytest

from src.terrajinja.sbp.vcd.nsxt_firewall_rule_parser import SbpVcdNsxtFirewallRuleParser
from .helper import stack


class TestSbpVcdNsxtFirewallRuleParser:
    def test_name(self, stack):
        result = SbpVcdNsxtFirewallRuleParser(
            scope=stack,
            ns="firewall_rule",
            edge_gateway_id="id",
            vcd_org_vdc="id",
            environment="env",
            source_address_name="source",
            source_address=["127.0.0.1"],
            destination_address_name="destination",
            destination_address=["127.0.0.1"]
        )
        assert result.name == "SOURCE_TO_DESTINATION"

    def test_parser(self, stack):
        result = SbpVcdNsxtFirewallRuleParser(
            scope=stack,
            ns="firewall_rule",
            edge_gateway_id="id",
            vcd_org_vdc="id",
            environment="env",
            destination_port=[{'protocol': 'tcp', 'port': 80}],
            source_address_name="source",
            source_address=["127.0.0.1"],
            destination_address_name="destination",
            destination_address=["127.0.0.1"]
        )
        parsed = result.parsed
        assert parsed['name'] == "SOURCE_TO_DESTINATION"
        assert parsed['direction'] == "IN_OUT"
        assert parsed['ipProtocol'] == "IPV4"
        assert parsed['action'] == "ALLOW"
        assert len(parsed['sourceIds']) == 1
        assert len(parsed['destinationIds']) == 1
        assert len(parsed['appPortProfileIds']) == 1


if __name__ == "__main__":
    pytest.main()
