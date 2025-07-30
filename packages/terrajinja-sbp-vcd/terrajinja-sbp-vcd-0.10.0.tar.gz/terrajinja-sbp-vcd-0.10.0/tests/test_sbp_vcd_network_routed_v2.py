from ipaddress import AddressValueError

import pytest
from cdktf import Testing

from src.terrajinja.sbp.vcd.network_routed_v2 import SbpVcdNetworkRoutedV2
from .helper import stack, has_resource, has_resource_with_properties


class TestSbpVcdNetworkRoutedV2:
    @pytest.mark.parametrize(
        "cidr, gateway, prefix_length, static_ip_pool",
        [
            ("30.30.30.0/23", "30.30.30.1", 23, [{"end_address": "30.30.31.254", "start_address": "30.30.30.2"}]),
            ("10.10.10.0/24", "10.10.10.1", 24, [{"end_address": "10.10.10.254", "start_address": "10.10.10.2"}]),
            ("25.25.25.0/25", "25.25.25.1", 25, [{"end_address": "25.25.25.126", "start_address": "25.25.25.2"}]),
        ],
    )
    def test_cidr_valid(self, stack, cidr, gateway, prefix_length, static_ip_pool):
        # stack = TerraformStack(Testing.app(), "stack")
        SbpVcdNetworkRoutedV2(stack, f"valid_cidr_{cidr}", cidr, ["", ""], name="name", edge_gateway_id="id")
        synthesized = Testing.synth(stack)

        has_resource(synthesized, "vcd_network_routed_v2")
        has_resource_with_properties(synthesized, "vcd_network_routed_v2", {"gateway": gateway})
        has_resource_with_properties(synthesized, "vcd_network_routed_v2", {"prefix_length": prefix_length})
        has_resource_with_properties(
            synthesized,
            "vcd_network_routed_v2",
            {"static_ip_pool": static_ip_pool},
        )

    def test_new_var(self, stack):
        # stack = TerraformStack(Testing.app(), "stack")
        SbpVcdNetworkRoutedV2(
            stack,
            f"route_new_var",
            cidr='40.40.0.0/16',
            name="name",
            edge_gateway_id="id",
            guest_vlan_allowed=True
        )
        synthesized = Testing.synth(stack)

        has_resource(synthesized, "vcd_network_routed_v2")
        has_resource_with_properties(synthesized, "vcd_network_routed_v2", {"gateway": "40.40.0.1"})
        has_resource_with_properties(synthesized, "vcd_network_routed_v2", {"guest_vlan_allowed": True})

    def test_override_gateway(self, stack):
        # stack = TerraformStack(Testing.app(), "stack")
        SbpVcdNetworkRoutedV2(
            stack,
            f"route_override_gateway",
            cidr='40.40.0.0/16',
            name="name",
            edge_gateway_id="id",
            gateway="10.10.10.10"
        )
        synthesized = Testing.synth(stack)
        print(synthesized)

        has_resource(synthesized, "vcd_network_routed_v2")
        has_resource_with_properties(synthesized, "vcd_network_routed_v2", {"gateway": "10.10.10.10"})


    def test_cidr_empty(self, stack):
        with pytest.raises(AddressValueError) as context:
            SbpVcdNetworkRoutedV2(stack, "empty_cidr", "", ["", ""], name="name", edge_gateway_id="id")

        assert "Address cannot be empty" == str(context.value)

    def test_cidr_invalid(self, stack):
        with pytest.raises(AddressValueError) as context:
            SbpVcdNetworkRoutedV2(stack, "invalid_cidr", "invalid_cidr", ["", ""], name="name", edge_gateway_id="id")

        assert "Expected 4 octets in 'invalid_cidr'" == str(context.value)


if __name__ == "__main__":
    pytest.main()
