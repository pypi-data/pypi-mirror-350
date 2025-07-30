from constructs import Construct

from terrajinja.imports.vcd.data_vcd_catalog import DataVcdCatalog
from terrajinja.imports.vcd.data_vcd_catalog_vapp_template import DataVcdCatalogVappTemplate
from .decorators import run_once


@run_once(parameter_match=["template_name", "catalog_organization", "catalog_name"])
class SbpDataVcdVmTemplates(DataVcdCatalogVappTemplate):
    """Extends the original vcd.data_vcd_catalog_vapp class
       """

    def __init__(self, scope: Construct, id_: str, template_name: str, catalog_organization: str, catalog_name: str):
        catalog_id = DataVcdCatalog(scope=scope,
                                    id_=f'sbp_vcd_catalog_{template_name}',
                                    org=catalog_organization,
                                    name=catalog_name,
                                    ).id
        """Enhances the original vcd.data_vcd_catalog_vapp
           this combines the original vcd catalog + catalog_vapp for simplicity
           and to ensure that it only gets called once

        Args:
            scope (Construct): Cdktf App
            id (str): uniq name of the resource
            catalog_organization (str): name of the organization the catalog belongs to
            catalog_name (str): name of the catalog

        Original:
            https://registry.terraform.io/providers/vmware/vcd/3.10.0/docs/data-sources/catalog_vapp_template
        """
        super().__init__(
            scope=scope,
            id_=f'sbp_vcd_catalog_vapp_template_{template_name}',
            catalog_id=catalog_id,
            name=template_name
        )
