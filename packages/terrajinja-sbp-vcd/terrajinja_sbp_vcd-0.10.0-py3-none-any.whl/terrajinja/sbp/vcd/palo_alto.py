from dataclasses import dataclass, asdict, field

from cdktf_cdktf_provider_time.sleep import Sleep
from constructs import Construct

from terrajinja.imports.vcd.data_vcd_vapp import DataVcdVapp
from terrajinja.imports.vcd.data_vcd_catalog import DataVcdCatalog
from terrajinja.imports.vcd.catalog_media import CatalogMedia
from terrajinja.imports.vcd.inserted_media import InsertedMedia
from terrajinja.imports.vcd.vapp_access_control import VappAccessControl
from terrajinja.imports.vcd.vm import Vm
from terrajinja.sbp.generic.calculation import human_read_to_megabyte
from terrajinja.sbp.generic.vm import SbpGenericVm
from terrajinja.sbp.generic.vm import SbpGenericVmPlacementPolicy
from .data_vcd_catalog_vapp_template import SbpDataVcdVmTemplates
from .data_vcd_vm_placement_policy import SbpDataVcdVmPlacementPolicy
from .vm_internal_disk import SbpVcdVmInternalDisk
from .palo_alto_iso_builder import PaloAltoIsoBuilder
from terrajinja.sbp.vcd.vm import SbpVcdVmNetwork
from ipaddress import IPv4Network
import re


def sanitize_identifier(name: str) -> str:
    """
    Convert a string into a valid Python identifier:
    - Replaces dashes with underscores
    - Prefixes with 'v_' if it starts with a digit
    - Raises ValueError if result is not a valid identifier
    """
    original = name
    name = name.replace("-", "_")
    if re.match(r'^\d', name):
        name = f'v_{name}'
    if not name.isidentifier():
        raise ValueError(f"Cannot convert key '{original}' to a safe attribute name")
    return name


class EmptyIpAddressesList(Exception):
    """Ip addresses list is empty"""


class InvalidNumberOfIpAddresses(Exception):
    """Count does not match"""


@dataclass
class SbpVcdPaloAltoDefaultLifecycle:
    ignore_changes: list = field(default_factory=lambda: ['vapp_template_id', 'power_on', 'guest_properties',
                                                          'override_template_disk', 'consolidate_disks_on_create',
                                                          'network'])

    @property
    def settings(self) -> dict:
        return asdict(self)


class DotAccessDict:
    def __init__(self, items: dict):
        self._original_to_safe = {}
        self._safe_to_original = {}
        self._safe_to_value = {}

        for original_key, value in items.items():
            safe_key = sanitize_identifier(original_key)
            self._original_to_safe[original_key] = safe_key
            self._safe_to_original[safe_key] = original_key
            self._safe_to_value[safe_key] = value

            setattr(self, safe_key, value)

    def __getitem__(self, key: str):
        """
        Allow access via original key: obj['web-server']
        """
        safe_key = self._original_to_safe.get(key)
        if safe_key is None:
            raise KeyError(f"Key '{key}' not found (original key)")
        return self._safe_to_value[safe_key]

    def get_original_name(self, safe_key: str) -> str:
        """
        Allow lookup of original name if needed
        """
        return self._safe_to_original.get(safe_key, None)

    def keys(self):
        return self._original_to_safe.keys()

    def items(self):
        return [(k, self[k]) for k in self.keys()]


class SbpVcdPaloAlto(Construct):
    """SBP version of vcd.nsxt_ip_set"""

    def __init__(
            self,
            scope: Construct,
            ns: str,
            name: str,
            count: int,
            template_name: str,
            memory: [str, int],
            bootstrap_network: str,
            bootstrap_template_path: str,
            bootstrap_catalog: str,
            networks: list[dict],
            dns_hosts: str = None,  # dns hosts
            vdc_urn: str = None,  # required for template
            org: str = None,  # required for template
            memory_hot_add_enabled: bool = True,
            cpu_hot_add_enabled: bool = True,
            placement_strategy: str = "one_per_zone",
            placements: list[dict] = None,
            first_digit: int = 0,
            catalog_organization: str = "NLCP-Templates",
            catalog_name: str = "NLCP-Templates",
            naming_format: list = None,
            depends_on_primary: bool = False,
            depends_on: list = None,
            os_disk_size: str = None,
            os_disk_iops: int = 5000,
            os_disk_storage_profile: str = "generic",
            disks: list[dict] = None,
            shared_with_everyone: bool = True,
            everyone_access_level: str = "Change",
            template_variables: dict = None,
            lifecycle=None,
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

        super().__init__(scope, ns)
        self._resources = {}

        if not vdc_urn and not org:
            raise ValueError("missing both vcd_urn or org parameter, you must supply one")

        # set defaults for mutable arguments
        if not depends_on:
            depends_on = []
        if naming_format is None:
            naming_format = ["%s%d%02d", "name", "zone_id", "nr_per_zone"]
        if placements is None:
            placements = [
                {'zone': 1, 'name': "NLCP1 Non-Windows"},
                {'zone': 2, 'name': "NLCP2 Non-Windows"},
                {'zone': 3, 'name': "NLCP3 Non-Windows"},
            ]
        if not lifecycle:
            lifecycle = SbpVcdPaloAltoDefaultLifecycle().settings

        if isinstance(memory, str):
            memory = human_read_to_megabyte(memory)

        # validate that we have ips
        if not networks:
            raise EmptyIpAddressesList(f"vm named '{name}' contains no networks and ip addresses")

        for network in networks:
            ip_addresses = network.get('ip_addresses')
            if len(ip_addresses) != count:
                raise InvalidNumberOfIpAddresses(
                    f"vm named '{name}' has a different number of ip_addresses compared to the count")

        # primary_network = next((network for network in networks if network.get('name') == bootstrap_network), None)
        # if not primary_network:
        #     raise ValueError(f"Bootstrap network '{bootstrap_network}' not found in networks")

        vm_template = SbpDataVcdVmTemplates(scope=scope, id_=ns, template_name=template_name,
                                            catalog_organization=catalog_organization,
                                            catalog_name=catalog_name)

        placement_policy = SbpGenericVmPlacementPolicy(strategy=placement_strategy, placements=placements)
        vms = SbpGenericVm(placement_policy=placement_policy, name=name, count=count, first_digit=first_digit,
                           formatting=naming_format, ip_addresses=ip_addresses)

        primary_vm = None
        last_depends_on = None
        for vm_id, vm in enumerate(vms):
            print(f'- host: {vm.name} in zone: {vm.zone_name} ip: {vm.ip}')

            placement_policy_id = SbpDataVcdVmPlacementPolicy(scope=scope, id_='', name=vms.placement_policy.name,
                                                              urn=vdc_urn, org=org).id

            # get vars and pass them to template
            ignore_vars = ['depends_on', 'modified_depends_on', '_vms']
            template_vars = {key: item for key, item in locals().items() if
                             type(item) in [str, int, float, list, bool] and not (
                                     key.startswith('__') or key in ignore_vars)}
            for key, value in vars(vm).items():
                template_vars[f'vm_{key}'] = value
            template_vars['vm'] = vars(vm)
            template_vars['network'] = {}
            for network in networks:
                template_vars['network'][network.get("name")] = {}
                template_vars['network'][network.get("name")]['name'] = network.get('name')
                template_vars['network'][network.get("name")]['ip_address'] = network.get('ip_addresses')[vm_id]
                if network.get('cidr'):
                    cidr = IPv4Network(network.get('cidr'))
                    template_vars['network'][network.get("name")]['netmask'] = cidr.netmask
                    template_vars['network'][network.get("name")]['gateway'] = cidr.network_address + 1

            template_vars['zone'] = vm.zone_name.split(' ')[0]
            if template_variables:
                for template_variable_key, template_variable_value in template_variables.items():
                    template_vars[template_variable_key] = template_variable_value

            # build iso based on templates
            builder = PaloAltoIsoBuilder(bootstrap_template_path, template_vars)
            iso_path = builder.build()
            vcd_bootstrap_catalog = DataVcdCatalog(
                scope=scope,
                id_=f'vm_{vm.name}_catalog_data',
                org=org,
                name=bootstrap_catalog[vm_id])

            iso_name = f'{vm.name}-bootstrap.iso'
            catalog_media = CatalogMedia(scope=scope,
                                         id_=f'vm_{vm.name}_catalog_media',
                                         org=org,
                                         catalog_id=vcd_bootstrap_catalog.id,
                                         name=iso_name,
                                         media_path=iso_path,
                                         lifecycle={
                                             'ignore_changes': ['media_path'],
                                         }
                                         )
            self._sub(f'vm_{vm.name}_catalog_media', catalog_media)

            modified_depends_on = depends_on.copy()
            if depends_on_primary and primary_vm:
                modified_depends_on.append(primary_vm)

            # destroy sleep due to delayed vcloud on vm destruction
            time_sleep_destroy_vm = Sleep(
                scope=scope,
                id=f'vm_{vm.name}_destroy_sleep',
                destroy_duration="30s",
                depends_on=modified_depends_on,
            )

            if os_disk_size:
                kwargs['override_template_disk'] = [{
                    'busType': "paravirtual",
                    'sizeInMb': human_read_to_megabyte(os_disk_size),
                    'busNumber': 0,
                    'unitNumber': 0,
                    'iops': os_disk_iops,
                    'storageProfile': os_disk_storage_profile,
                }]

            new_networks = [SbpVcdVmNetwork(name=network.get('name'), ip=network.get('ip_addresses')[vm_id]).settings
                            for network in networks]

            new_vm = Vm(
                scope=scope,
                id_=f'vm_{vm.name}',
                name=vm.name,
                computer_name=vm.name,
                vapp_template_id=vm_template.id,
                memory=memory,
                memory_hot_add_enabled=memory_hot_add_enabled,
                cpu_hot_add_enabled=cpu_hot_add_enabled,
                power_on=False,
                placement_policy_id=placement_policy_id,
                network=new_networks,
                lifecycle=lifecycle,
                depends_on=[time_sleep_destroy_vm],
                **kwargs
            )
            self._sub(f'vm_{vm.name}', new_vm)

            time_sleep = Sleep(
                scope=scope,
                id=f'vm_{vm.name}_ac_sleep',
                create_duration="60s",
                depends_on=[new_vm]
            )

            inserted_media = InsertedMedia(
                scope=scope,
                id_=f'vm_{vm.name}_inserted_media',
                org=org,
                vdc=new_vm.vdc,
                catalog=bootstrap_catalog[vm_id],
                name=iso_name,
                vapp_name=new_vm.vapp_name,
                vm_name=new_vm.name,
                eject_force=True,
                depends_on=[catalog_media, time_sleep]
            )
            self._sub(f'vm_{vm.name}_inserted_media', inserted_media)

            # TerraformOutput(
            #     scope=scope,
            #     id=f'vm_out_catalog',
            #     value=vcd_bootstrap_catalog.id
            # )
            # TerraformOutput(
            #     scope=scope,
            #     id=f'vm_out_vdc',
            #     value=new_vm.vdc
            # )
            # TerraformOutput(
            #     scope=scope,
            #     id=f'vm_out_vapp_name',
            #     value=new_vm.vapp_name
            # )
            # TerraformOutput(
            #     scope=scope,
            #     id=f'vm_out_vm_name',
            #     value=new_vm.name
            # )

            vapp_vm = DataVcdVapp(
                scope=scope,
                id_=f'vm_{vm.name}_vapp',
                vdc=new_vm.vdc,
                name=new_vm.vapp_name,
                depends_on=[time_sleep]
            )

            last_depends_on = VappAccessControl(
                scope=scope,
                id_=f'vm_{vm.name}_vapp_access_control',
                vapp_id=vapp_vm.id,
                vdc=new_vm.vdc,
                shared_with_everyone=shared_with_everyone,
                everyone_access_level=everyone_access_level,
                lifecycle={
                    'ignore_changes': ['vapp_id'],
                }
            )
            self._sub(f'vm_{vm.name}_vapp_access_control', last_depends_on)

            new_disk = None
            if disks:
                for disk_nr, disk in enumerate(disks):
                    new_disk = SbpVcdVmInternalDisk(
                        scope=scope,
                        vdc=new_vm.vdc,
                        ns=f'vm_{vm.name}_disk_{disk_nr}',
                        vm_name=new_vm.name,
                        vapp_name=new_vm.vapp_name,
                        bus_type=disk.get('bus_type', "paravirtual"),
                        size=disk['size'],
                        bus_number=2,
                        unit_number=disk_nr,
                        storage_profile=disk.get('storage_profile', "generic"),
                        iops=disk.get('iops', 5000),
                        depends_on=[new_vm],
                        delay_in_seconds="60s",
                    )
                    last_depends_on = new_disk

            # primary to depend on is the last object created (vm or disk if any additionally attached)
            if not primary_vm:
                if new_disk:
                    primary_vm = new_disk
                else:
                    primary_vm = new_vm

        self._sub('completed', last_depends_on)

    def _sub(self, name: str, value: str):
        """Set the value of a property"""
        print(f' sub: {name}')
        self._resources[name] = value

    @property
    def sub(self):
        # Only for user access — never pass this whole object to Terraform
        return DotAccessDict(self._resources)
