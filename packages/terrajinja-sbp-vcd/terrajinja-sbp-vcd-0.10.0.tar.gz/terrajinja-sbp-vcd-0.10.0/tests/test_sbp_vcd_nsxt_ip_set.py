from ipaddress import AddressValueError

import pytest
from cdktf import Testing

from src.terrajinja.sbp.vcd.nsxt_ip_set import IpSet, SbpVcdNsxtIpSet, IpAddressSetMismatch, EmptyIpAddressesList
from .helper import stack, has_resource, has_resource_with_properties


class TestSbpVcdNsxtIpSet:
    @pytest.mark.parametrize(
        "name, ip_addresses",
        [
            ("valid-1afe", ["10.10.10.10", "10.10.10.20"]),
            ("1dnd9-sadf", ["20.10.10.10", "20.10.10.20"]),
            ("q2efn91dfD", ["30.10.10.10", "30.10.10.20"]),
        ],
    )
    def test_ip_set_name_is_upper(self, stack, name, ip_addresses):
        result = IpSet(name, ip_addresses)
        assert result.name == name.upper()

    @pytest.mark.parametrize(
        "name, ip_addresses",
        [
            ("valid1", ["10.10.10.10", "10.10.10.20"]),
            ("valid2", ["20.10.10.10", "20.10.10.20"]),
            ("valid3", ["30.10.10.10", "30.10.10.20"]),
        ],
    )
    def test_nsxt_ip_set_valid(self, stack, name, ip_addresses):
        SbpVcdNsxtIpSet(
            scope=stack,
            ns=f"test_nsxt_ip_set_valid_{name}",
            name=name,
            ip_addresses=ip_addresses,
            edge_gateway_id="id",
        )
        synthesized = Testing.synth(stack)

        has_resource(synthesized, "vcd_nsxt_ip_set")
        has_resource_with_properties(synthesized, "vcd_nsxt_ip_set", {"name": name.upper()})
        has_resource_with_properties(synthesized, "vcd_nsxt_ip_set", {"ip_addresses": ip_addresses})

    def test_nsxt_ip_set_valid_string(self, stack):
        SbpVcdNsxtIpSet(
            scope=stack,
            ns=f"test_nsxt_ip_set_valid_string",
            name="valid_string",
            ip_addresses="127.0.0.1",
            edge_gateway_id="id",
        )
        synthesized = Testing.synth(stack)

        has_resource(synthesized, "vcd_nsxt_ip_set")
        has_resource_with_properties(synthesized, "vcd_nsxt_ip_set", {"name": "valid_string".upper()})
        has_resource_with_properties(synthesized, "vcd_nsxt_ip_set", {"ip_addresses": ["127.0.0.1"]})

    # resource with the same name should only be written once
    @pytest.mark.parametrize(
        "name, ip_addresses",
        [
            ("valid_duplicate_should_exist_once", ["10.10.10.10", "10.10.10.20"]),
            (
                    "valid_duplicate_should_exist_once",
                    ["10.10.10.20", "10.10.10.10"],
            ),  # note the different order, in same list
            ("valid_duplicate_should_exist_once", ["10.10.10.10", "10.10.10.20"]),
        ],
    )
    def test_nsxt_ip_set_valid_duplicate_should_exist_once(self, stack, name, ip_addresses):
        SbpVcdNsxtIpSet(
            scope=stack,
            ns="test_nsxt_ip_set_valid_same",
            name=name,
            ip_addresses=ip_addresses,
            edge_gateway_id="id",
        )
        synthesized = Testing.synth(stack)

        has_resource(synthesized, "vcd_nsxt_ip_set")

    @pytest.mark.parametrize(
        "name, ip_addresses, ip_addresses2",
        [
            ("invalid_duplicate", ["10.10.10.10", "10.10.10.20"], ["20.20.20.20", "20.20.20.20"]),
        ],
    )
    def test_nsxt_ip_set_invalid_duplicate(self, stack, name, ip_addresses, ip_addresses2):
        # add ip set once
        SbpVcdNsxtIpSet(
            scope=stack,
            ns="test_nsxt_ip_set_valid",
            name=name,
            ip_addresses=ip_addresses,
            edge_gateway_id="id",
        )
        synthesized = Testing.synth(stack)

        has_resource(synthesized, "vcd_nsxt_ip_set")

        # add ip set again with different ip_addresses
        with pytest.raises(IpAddressSetMismatch) as context:
            SbpVcdNsxtIpSet(
                scope=stack,
                ns="test_nsxt_ip_set_valid",
                name=name,
                ip_addresses=ip_addresses2,
                edge_gateway_id="id",
            )

        assert "is defined twice with different ip_addresses" in str(context.value)

    def test_nsxt_ip_set_empty(self, stack):
        with pytest.raises(EmptyIpAddressesList) as context:
            SbpVcdNsxtIpSet(
                scope=stack,
                ns="empty_ip_addresses",
                name="empty_ip_addresses",
                ip_addresses=[],
                edge_gateway_id="id",
            )

        assert "contains no ip addresses" in str(context.value)

    def test_nsxt_ip_set_invalid(self, stack):
        with pytest.raises(AddressValueError) as context:
            SbpVcdNsxtIpSet(
                scope=stack,
                ns="invalid_ip_addresses",
                name="invalid_ip_addresses",
                ip_addresses=["not_an_ip"],
                edge_gateway_id="id",
            )

        assert f"ip address defined does not appear to be ipv4 or ipv6" in str(context.value)


if __name__ == "__main__":
    pytest.main()
