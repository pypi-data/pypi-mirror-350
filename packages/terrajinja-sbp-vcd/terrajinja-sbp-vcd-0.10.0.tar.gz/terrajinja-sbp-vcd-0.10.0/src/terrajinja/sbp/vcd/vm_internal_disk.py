from cdktf_cdktf_provider_time.sleep import Sleep
from constructs import Construct

from terrajinja.imports.vcd.vm_internal_disk import VmInternalDiskA
from terrajinja.sbp.generic.calculation import human_read_to_megabyte


class SbpVcdVmInternalDisk(VmInternalDiskA):
    """SBP version of vcd.nsxt_ip_set"""

    def __init__(
            self,
            scope: Construct,
            ns: str,
            vapp_name: str,
            vm_name: str,
            vdc: str,
            depends_on: list,
            size: str,
            delay_in_seconds: str = None,
            bus_type: str = "paravirtual",
            storage_profile: str = "generic",
            iops: int = 5000,
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

        time_sleep = None
        if delay_in_seconds:
            time_sleep = Sleep(
                scope=scope,
                id=f'{ns}_sleep',
                create_duration=delay_in_seconds,
                depends_on=depends_on
            )
            depends_on.append(time_sleep)

        super().__init__(
            scope=scope,
            id_=ns,
            vapp_name=vapp_name,
            vm_name=vm_name,
            bus_type=bus_type,
            storage_profile=storage_profile,
            size_in_mb=human_read_to_megabyte(size),
            iops=iops,
            depends_on=depends_on,
            vdc=vdc,
            **kwargs,
        )
