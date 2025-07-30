import pytest
from cdktf import Testing

from src.terrajinja.sbp.vcd.nsxt_app_port_profile import SbpVcdNsxtAppPortProfile, InvalidProtocolName
from .helper import stack, has_resource, has_resource_with_properties


class TestSbpVcdNsxtIpSet:
    @pytest.mark.parametrize(
        "environment, protocol, port",
        [
            ("env", "tcp", 80),
            ("env", "udp", 53),
            ("env", "icmpv4", 8),
        ],
    )
    def test_nsxt_app_port_profile_valid(self, stack, environment, protocol, port):
        SbpVcdNsxtAppPortProfile(
            scope_=stack,
            context_id='id',
            ns=f"test_nsxt_app_port_profile_valid_{environment}_{protocol}_{port}",
            environment=environment,
            protocol=protocol,
            port=port,
        )
        synthesized = Testing.synth(stack)

        has_resource(synthesized, "vcd_nsxt_app_port_profile")
        has_resource_with_properties(
            synthesized, "vcd_nsxt_app_port_profile", {"name": f"{environment}_{protocol}_{port}".upper()}
        )
        has_resource_with_properties(
            synthesized,
            "vcd_nsxt_app_port_profile",
            {"app_port": [{"port": [f"{port}"], "protocol": protocol.upper().replace("ICMPV", "ICMPv")}]},
        )

    @pytest.mark.parametrize(
        "environment, protocol",
        [
            ("env", "tcp"),
            ("env", "udp"),
            ("env", "icmpv4"),
        ],
    )
    def test_nsxt_app_port_profile_valid_no_port(self, stack, environment, protocol):
        SbpVcdNsxtAppPortProfile(
            scope_=stack,
            ns=f"test_nsxt_app_port_profile_valid_{environment}_{protocol}_None",
            context_id='id',
            environment=environment,
            protocol=protocol,
        )
        synthesized = Testing.synth(stack)

        has_resource(synthesized, "vcd_nsxt_app_port_profile")
        has_resource_with_properties(
            synthesized, "vcd_nsxt_app_port_profile", {"name": f"{environment}_{protocol}".upper()}
        )
        has_resource_with_properties(
            synthesized,
            "vcd_nsxt_app_port_profile",
            {"app_port": [{"protocol": protocol.upper().replace("ICMPV", "ICMPv")}]},
        )

    def test_nsxt_app_port_profile_invalid_protocol(self, stack):
        with pytest.raises(InvalidProtocolName) as context:
            SbpVcdNsxtAppPortProfile(
                scope_=stack,
                ns="test_nsxt_app_port_profile_invalid_protocol",
                context_id='id',
                environment="env",
                protocol="bla",
            )
        assert "does not match one of the allowed protocols" in str(context.value)


if __name__ == "__main__":
    pytest.main()