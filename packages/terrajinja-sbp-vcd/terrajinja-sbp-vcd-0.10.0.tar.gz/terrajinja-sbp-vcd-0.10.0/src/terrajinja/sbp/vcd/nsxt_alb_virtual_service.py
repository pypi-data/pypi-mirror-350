from dataclasses import dataclass
from constructs import Construct
from terrajinja.imports.vcd.nsxt_alb_virtual_service import NsxtAlbVirtualService
from .decorators import run_once


@dataclass
class SbpLoadbalancerService:
    scope: Construct
    vip_name: str
    pool_id: str
    virtual_ip_address: str
    vip_port: int
    service_type: str

    @property
    def name(self):
        return f"{self.vip_name}-{self.vip_port}-service".upper()

    @property
    def service_port(self):
        return [
            {
                'startPort': self.vip_port,
                'type': self.service_type.upper().replace(' ', '_'),
                # 'ssl_enabled': False,
            }
        ]


@run_once(parameter_match=["vip_port", "service_type", "application_profile_type", "virtual_ip_address"])
class SbpVcdNsxtAlbVirtualService(NsxtAlbVirtualService):
    """Extends the original class to ensure that it only gets called once"""

    def __init__(self, scope: Construct, vip_name: str, pool_id: str, virtual_ip_address: str,
                 service_type: str, vip_port: int, application_profile_type: str = 'L4', **kwargs):

        service = SbpLoadbalancerService(
            scope=scope,
            vip_name=vip_name,
            pool_id=pool_id,
            virtual_ip_address=virtual_ip_address,
            service_type=service_type,
            vip_port=vip_port
        )

        super().__init__(
            scope=scope,
            id_=service.name,
            name=service.name,
            application_profile_type=application_profile_type,
            pool_id=pool_id,
            virtual_ip_address=virtual_ip_address,
            service_port=service.service_port,
            lifecycle={'create_before_destroy': True},
            **kwargs
        )
