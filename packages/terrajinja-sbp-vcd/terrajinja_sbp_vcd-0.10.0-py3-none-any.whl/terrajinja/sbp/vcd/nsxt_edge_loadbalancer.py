from constructs import Construct
from .data_vcd_nsxt_alb_edgegateway_service_engine_group import SbpDataVcdNsxtAlbEdgegatewayServiceEngineGroup
from .nsxt_alb_pool import SbpVcdNsxtAlbPool
from .nsxt_alb_virtual_service import SbpVcdNsxtAlbVirtualService


# sbp.vcd.nsxt_edge_loadbalancer
class SbpVcdNsxtEdgeLoadbalancer:
    """SBP version of vcd.nsxt_alb_virtual_service"""

    def __init__(
            self,
            scope: Construct,
            ns: str,
            rules: list[dict],
            edge_gateway_id: str,  # required for ip_set
            service_engine_group_name: str,
            org: str,
            **kwargs,
    ):

        for rule in rules:
            loadbalancer = rule.get('loadbalancer')

            pool = SbpVcdNsxtAlbPool(
                scope=scope,
                destination_address_name=rule.get('destination_address_name'),
                destination_port=rule.get('destination_port'),
                algorithm=loadbalancer.get('algorithm'),
                persistence=loadbalancer.get('persistence'),
                health_monitor=loadbalancer.get('health_monitor', 'TCP'),
                vip_port=rule.get('vip_port'),
                destination_address=rule.get('destination_address'),
                edge_gateway_id=edge_gateway_id,
            )

            vcd_nsxt_alb_edgegateway_service_engine_group_id = SbpDataVcdNsxtAlbEdgegatewayServiceEngineGroup(
                id_=service_engine_group_name,
                edge_gateway_id=edge_gateway_id,
                org=org,
                scope=scope,
                service_engine_group_name=service_engine_group_name).service_engine_group_id

            SbpVcdNsxtAlbVirtualService(
                scope=scope,
                service_engine_group_id=vcd_nsxt_alb_edgegateway_service_engine_group_id,
                edge_gateway_id=edge_gateway_id,
                vip_name=rule.get('vip_name'),
                pool_id=pool.id,
                virtual_ip_address=rule.get('vip_ip'),
                service_type=loadbalancer.get('service_type', 'TCP_PROXY'),
                application_profile_type=loadbalancer.get('application_profile_type', 'L4'),
                vip_port=rule.get('vip_port'),
                is_transparent_mode_enabled=loadbalancer.get('is_transparent_mode_enabled'),
            )
