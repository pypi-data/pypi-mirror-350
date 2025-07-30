from cdktf import Testing

from src.terrajinja.sbp.vcd.data_vcd_vm_placement_policy import SbpDataVcdVmPlacementPolicy
from .helper import stack, has_data_source, has_data_source_path_value


class TestSbpDataVcdVmTemplates:
    def test_vm_policy_one_per_zone_loop(self, stack):
        SbpDataVcdVmPlacementPolicy(
            stack,
            id_='id',
            name="policy_name",
            urn="urn",
        )
        synthesized = Testing.synth(stack)

        has_data_source(synthesized, "vcd_vm_placement_policy")
        has_data_source_path_value(synthesized, "vcd_vm_placement_policy", "sbp_vcd_catalog_vapp_template_policy_name",
                                   "name", "policy_name")
        has_data_source_path_value(synthesized, "vcd_vm_placement_policy", "sbp_vcd_catalog_vapp_template_policy_name",
                                   "provider_vdc_id", "urn")
