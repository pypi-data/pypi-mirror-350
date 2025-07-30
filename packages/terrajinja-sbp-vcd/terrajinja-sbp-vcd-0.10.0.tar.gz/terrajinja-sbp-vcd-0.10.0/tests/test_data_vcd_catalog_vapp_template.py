from cdktf import Testing

from src.terrajinja.sbp.vcd.data_vcd_catalog_vapp_template import SbpDataVcdVmTemplates
from .helper import stack, has_data_source, has_data_source_path_value


class TestSbpDataVcdVmTemplates:
    def test_vm_policy_one_per_zone_loop(self, stack):
        SbpDataVcdVmTemplates(
            stack,
            id_='id',
            template_name="template_name",
            catalog_organization="catalog_organization",
            catalog_name="catalog_name",
        )
        synthesized = Testing.synth(stack)

        has_data_source(synthesized, "vcd_catalog")
        has_data_source(synthesized, "vcd_catalog_vapp_template")
        has_data_source_path_value(synthesized, "vcd_catalog", "sbp_vcd_catalog_template_name", "name", "catalog_name")
        has_data_source_path_value(synthesized, "vcd_catalog", "sbp_vcd_catalog_template_name", "org",
                                   "catalog_organization")
        has_data_source_path_value(synthesized, "vcd_catalog_vapp_template",
                                   "sbp_vcd_catalog_vapp_template_template_name", "name",
                                   "template_name")
        has_data_source_path_value(synthesized, "vcd_catalog_vapp_template",
                                   "sbp_vcd_catalog_vapp_template_template_name", "catalog_id",
                                   "${data.vcd_catalog.sbp_vcd_catalog_template_name.id}")
