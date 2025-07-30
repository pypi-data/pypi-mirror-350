import json
import pytest
from cdktf import Testing
from src.terrajinja.sbp.vcd.nsxt_alb_pool import SbpVcdNsxtAlbPool, SbpVcdNsxtAlbPoolHealthMonitorTypeNotDefined
from .helper import stack, has_resource, has_resource_count


class TestSbpVcdNsxtAlbPool:

    def test_resource(self, stack):
        pool = SbpVcdNsxtAlbPool(
            scope=stack,
            destination_address_name="name1",
            destination_port=8080,
            algorithm="Least connections",
            persistence="Client IP",
            destination_address=["10.0.0.1", "10.0.0.2", "10.0.0.3"],
            edge_gateway_id="edge_gateway_id",
            health_monitor="TCP",
            vip_port=8080
        )
        # We should have gotten a formatted pool name
        assert pool.name_input == 'NAME1-8080-TCP-POOL'

        synthesized = Testing.synth(stack)
        j = json.loads(synthesized)

        has_resource(synthesized, "vcd_nsxt_alb_pool")
        has_resource(synthesized, "vcd_nsxt_ip_set")
        # we should have 1 ip sets
        has_resource_count(synthesized, "vcd_nsxt_ip_set", 1)
        # containing 3 addresses
        assert len(j['resource']['vcd_nsxt_ip_set']['NAME1']['ip_addresses']) == 3

    def test_health_monitor_type_wrongly_defined(self, stack):
        with pytest.raises(SbpVcdNsxtAlbPoolHealthMonitorTypeNotDefined) as context:
            result = SbpVcdNsxtAlbPool(
                scope=stack,
                destination_address_name="name_wrongly_defined",
                destination_port=8080,
                algorithm="Least connections",
                persistence="Client IP",
                destination_address=["10.0.0.1", "10.0.0.2", "10.0.0.3"],
                edge_gateway_id="edge_gateway_id",
                health_monitor="UNKNOWN",
                vip_port=8080
            )

            _ = result

        assert ("Type is 'UNKNOWN' expected one of ['HTTP', 'HTTPS', 'TCP', 'UDP', 'PING']  "
                "in health_monitor") in str(context.value)


if __name__ == "__main__":
    pytest.main()
