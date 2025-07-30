from cdktf import Fn
from constructs import Construct

from terrajinja.imports.vcd.data_vcd_rde_type import DataVcdRdeType
from terrajinja.imports.vcd.rde import Rde

import base64


class SbpVcdRde(Rde):
    """SBP version of vcd.nsxt_ip_set"""

    def __init__(
            self,
            scope: Construct,
            ns: str,
            name: str,
            config_file_json: str,
            config_file_yaml: str,
            bearer: str,
            vcd_org: str,
            vcd_org_vdc: str,
            network_name: str,
            loadbalancer_subnet: str,
            kubernetes_api_ip: str,
            ssh_public_key: str = "",
            disk_size: str = "200Gi",
            vendor: str = "vmware",
            nss: str = "capvcdCluster",
            resolve: bool = True,
            cap_vcd_cluster_version: str = "1.2.0",
            tkg_version: str = "v2.2.0",
            tanzu_kubernetes_release: str = "v1.25.7---vmware.2-tkg.1",
            bootstrap_version: str = "v1.25.7+vmware.2",
            bootstrap_template: str = "Ubuntu 20.04 and Kubernetes v1.25.7+vmware.2",
            **kwargs,
    ):
        """Enhances the original vcd.nsxt_ip_set
            Ensures that only one ip set is created, and validates its use across the deployment

        Args:
            scope (Construct): Cdktf App
            id (str): uniq name of the resource

        Original:
            https://registry.terraform.io/providers/vmware/vcd/latest/docs/resources/nsxt_app_port_profile
        """

        rde_type = DataVcdRdeType(
            scope=scope,
            id_=f'{ns}_type',
            vendor=vendor,
            nss=nss,
            version=cap_vcd_cluster_version,
        )

        yaml_template = Fn.templatefile(
            config_file_yaml, {
                'bearer': base64.b64encode(bearer.encode("ascii")).decode("ascii"),
                'cluster_name': name,
                'tkg_version': tkg_version,
                'tanzu_kubernetes_release': tanzu_kubernetes_release,
                'org_name': vcd_org,
                'vdc_name': vcd_org_vdc,
                'network_name': network_name,
                'disk_size': disk_size,
                'bootstrap_version': bootstrap_version,
                'bootstrap_template': bootstrap_template,
                'loadbalancer_subnet': loadbalancer_subnet,
                'ssh_public_key': ssh_public_key,
                'kubernetes_api_ip': kubernetes_api_ip,
            }
        )
        json_template = Fn.templatefile(
            config_file_json, {
                'yaml': Fn.jsonencode(yaml_template),
                'org_name': vcd_org,
                'vdc_name': vcd_org_vdc,
                'cluster_name': name,
            }
        )

        super().__init__(
            scope=scope,
            id_=ns,
            resolve=resolve,
            name=name,
            rde_type_id=rde_type.id,
            input_entity=json_template,
            **kwargs,
        )
