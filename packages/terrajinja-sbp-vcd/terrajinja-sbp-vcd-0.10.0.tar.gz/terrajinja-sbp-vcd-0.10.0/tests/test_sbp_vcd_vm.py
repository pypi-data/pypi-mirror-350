import json
import pytest
from cdktf import Testing
from src.terrajinja.sbp.vcd.vm import SbpVcdVm
from .helper import stack, has_resource, has_resource_count, has_resource_path_value


class TestSbpVcdNsxtAlbVirtualService:

    def test_resource(self, stack):
        pool = SbpVcdVm(
            scope=stack,
            ns="vm",
            name="my-vm",
            count=2,
            template_name='template_name',
            cloud_config_file='file',
            ip_addresses=['10.0.0.1', '10.0.0.2'],
            network_name='my-network',
            dns_hosts=['10.0.0.1', '10.0.0.2'],
            memory="1GB",
            org='org',
        )

        synthesized = Testing.synth(stack)
        j = json.loads(synthesized)
        has_resource(synthesized, "vcd_vm")
        has_resource(synthesized, "vcd_vapp_access_control")
        has_resource(synthesized, "time_sleep")

    def test_resource_with_os_disk(self, stack):
        pool = SbpVcdVm(
            scope=stack,
            ns="vm",
            name="my-vm-with-os-disk",
            count=2,
            template_name='template_name',
            cloud_config_file='file',
            ip_addresses=['10.0.0.1', '10.0.0.2'],
            network_name='my-network',
            dns_hosts=['10.0.0.1', '10.0.0.2'],
            memory="1GB",
            org='org',
            os_disk_size="10GB",
        )

        synthesized = Testing.synth(stack)
        j = json.loads(synthesized)
        has_resource(synthesized, "vcd_vm")
        has_resource(synthesized, "vcd_vapp_access_control")
        has_resource(synthesized, "time_sleep")
        print(synthesized)
        assert j['resource']['vcd_vm']['vm_my-vm-with-os-disk100']['override_template_disk'][0]['size_in_mb'] == 10240


if __name__ == "__main__":
    pytest.main()
