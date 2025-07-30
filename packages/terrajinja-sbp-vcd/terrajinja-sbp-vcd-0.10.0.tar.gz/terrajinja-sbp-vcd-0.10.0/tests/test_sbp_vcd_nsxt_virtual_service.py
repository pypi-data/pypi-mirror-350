import json
import pytest
from cdktf import Testing
from src.terrajinja.sbp.vcd.nsxt_alb_virtual_service import SbpVcdNsxtAlbVirtualService
from .helper import stack, has_resource, has_resource_count


class TestSbpVcdNsxtAlbVirtualService:

    def test_resource(self, stack):
        pool = SbpVcdNsxtAlbVirtualService(
            scope=stack,
            service_engine_group_id="service_engine_group_id",
            edge_gateway_id="edge_gateway_id",
            vip_name="TEST2-TLA-TST-SHR-DMZ-PROXY-VIP",
            pool_id="TF-token",
            virtual_ip_address="10.0.0.123",
            service_type="L4",
            vip_port=8081
        )
        # We should have gotten a formatted pool name
        assert pool.name_input == 'TEST2-TLA-TST-SHR-DMZ-PROXY-VIP-8081-SERVICE'

        synthesized = Testing.synth(stack)
        j = json.loads(synthesized)
        has_resource(synthesized, "vcd_nsxt_alb_virtual_service")


if __name__ == "__main__":
    pytest.main()
