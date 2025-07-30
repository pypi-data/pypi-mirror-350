from constructs import Construct
from terrajinja.imports.vcd.data_vcd_nsxt_alb_edgegateway_service_engine_group import DataVcdNsxtAlbEdgegatewayServiceEngineGroup
from .decorators import run_once


@run_once(parameter_match=["service_engine_group_name"])
class SbpDataVcdNsxtAlbEdgegatewayServiceEngineGroup(DataVcdNsxtAlbEdgegatewayServiceEngineGroup):

    def __init__(self, scope: Construct, service_engine_group_name: str, edge_gateway_id: str,
                 org: str, **kwargs):

        super().__init__(
            scope=scope,
            edge_gateway_id=edge_gateway_id,
            org=org,
            service_engine_group_name=service_engine_group_name,
            **kwargs
        )
