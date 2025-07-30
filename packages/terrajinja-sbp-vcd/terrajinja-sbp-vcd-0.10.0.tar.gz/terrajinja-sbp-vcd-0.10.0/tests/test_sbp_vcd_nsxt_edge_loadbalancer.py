import json
import pytest
from cdktf import Testing
from src.terrajinja.sbp.vcd.nsxt_edge_loadbalancer import SbpVcdNsxtEdgeLoadbalancer
from .helper import stack, has_resource, has_resource_count


class TestSbpVcdNsxtEdgeLoadbalancer:

    def test_resource(self, stack):
        rules = [
            {
                'vip_name': 'TLA-TST-SHR-DMZ-PROXY-VIP',
                'vip_ip': '10.0.0.1',
                'vip_port': 8080,
                'destination_address_name': 'TLA-TST-SHR-DMZ-PROXY-HOSTS',
                'destination_address': [
                    '10.0.0.2',
                    '10.0.0.3'
                ],
                'destination_port': 8080,
                'loadbalancer': {
                    'service_type': 'L4',
                    'preserve_client_ip': True,
                    'algorithm': 'Least connections',
                    'persistence': 'Client IP',
                    'health_monitor': 'TCP',
                }
            },
            {
                'vip_name': 'TEST1-TLA-TST-SHR-DMZ-PROXY-VIP',
                'vip_ip': '10.0.0.11',
                'vip_port': 8888,
                'destination_address_name': 'TEST1-TLA-TST-SHR-DMZ-PROXY-HOSTS',
                'destination_address': [
                    '10.0.0.12',
                    '10.0.0.13'
                ],
                'destination_port': 8888,
                'loadbalancer': {
                    'service_type': 'L4',
                    'preserve_client_ip': True,
                    'algorithm': 'Least connections',
                    'persistence': 'Client IP',
                    'health_monitor': 'TCP',
                }
            }
        ]

        SbpVcdNsxtEdgeLoadbalancer(
            scope=stack,
            ns="ns",
            rules=rules,
            edge_gateway_id="edge_gateway_id",
            service_engine_group_name="service_engine_group_name",
            org="org"
        )

        synthesized = Testing.synth(stack)
        # j = json.loads(synthesized)
        has_resource(synthesized, "vcd_nsxt_alb_pool")
        has_resource(synthesized, "vcd_nsxt_alb_virtual_service")
        has_resource(synthesized, "vcd_nsxt_ip_set")

        # We need 2 of each (as defined above in the json)
        has_resource_count(synthesized, "vcd_nsxt_alb_pool", 2)
        has_resource_count(synthesized, "vcd_nsxt_alb_virtual_service", 2)
        has_resource_count(synthesized, "vcd_nsxt_ip_set", 2)


if __name__ == "__main__":
    pytest.main()
