from dataclasses import dataclass, asdict, field

from cdktf import Fn
from cdktf_cdktf_provider_time.sleep import Sleep
from cdktf_cdktf_provider_vault.token import Token
from cdktf_cdktf_provider_vault.token_auth_backend_role import TokenAuthBackendRole
from constructs import Construct

from terrajinja.imports.vcd.data_vcd_vapp import DataVcdVapp
from terrajinja.imports.vcd.vapp_access_control import VappAccessControl
from terrajinja.imports.vcd.vm import Vm
from terrajinja.sbp.generic.calculation import human_read_to_megabyte
from terrajinja.sbp.generic.vm import SbpGenericVm
from terrajinja.sbp.generic.vm import SbpGenericVmPlacementPolicy
from .data_vcd_catalog_vapp_template import SbpDataVcdVmTemplates
from .data_vcd_vm_placement_policy import SbpDataVcdVmPlacementPolicy
from .vm_internal_disk import SbpVcdVmInternalDisk


class EmptyIpAddressesList(Exception):
    """Ip addresses list is empty"""


class InvalidNumberOfIpAddresses(Exception):
    """Count does not match"""


class MissingChefArguments(Exception):
    """Missing required chef arguments"""


def reindent(offset: int, text: str) -> str:
    """
    indents a multiline-string based on the offset.

    Args:
        offset: number of spaces to indent
        text: original string or multiline string

    Returns:
        space indented string

    """
    text = text.split('\n')
    text = [(offset * ' ') + line.lstrip() for line in text]
    text = "\n".join(text)
    return text


@dataclass
class SbpVcdVmDefaultLifecycle:
    ignore_changes: list = field(default_factory=lambda: ['vapp_template_id', 'power_on', 'guest_properties',
                                                          'override_template_disk', 'consolidate_disks_on_create'])

    @property
    def settings(self) -> dict:
        return asdict(self)


@dataclass
class SbpVcdVmNetwork:
    name: str
    ip: str = None
    type: str = 'org'
    ipAllocationMode: str = 'MANUAL'
    isPrimary: bool = True
    connected: bool = True

    @property
    def settings(self) -> dict:
        return asdict(self)


class SbpVcdVm:
    """SBP version of vcd.nsxt_ip_set"""

    def __init__(
            self,
            scope: Construct,
            ns: str,
            name: str,
            count: int,
            template_name: str,
            cloud_config_file: str,
            ip_addresses: list[str],
            network_name: str,
            dns_hosts: list[str],
            memory: [str, int],
            vdc_urn: str = None,  # required for template
            org: str = None,  # required for template
            memory_hot_add_enabled: bool = True,
            cpu_hot_add_enabled: bool = True,
            power_on: bool = True,
            placement_strategy: str = "one_per_zone",
            placements: list[dict] = None,
            first_digit: int = 0,
            catalog_organization: str = "NLCP-Templates",
            catalog_name: str = "NLCP-Templates",
            naming_format: list = None,
            vault_policies: list = None,
            vault_token_period: int = 604800,
            vault_orphan: bool = True,
            vault_renewable: bool = True,
            vault_renew_min_lease: int = 86400,
            vault_renew_increment: int = 604800,
            proxy_url: str = "''",
            chef_run_list: list = None,
            chef_client_version: int = None,
            chef_client_url: str = None,
            chef_encrypted_databag_secret: str = None,
            chef_server_url: str = None,
            chef_environment: str = None,
            chef_validator_name: str = None,
            chef_validator_pem: str = None,
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
            lifecycle = SbpVcdVmDefaultLifecycle().settings

        print(f' chef_run_list : {chef_run_list}')
        if chef_run_list:
            chef_required_parameters = [
                'chef_client_version',
                'chef_client_url',
                'chef_encrypted_databag_secret',
                'chef_server_url',
                'chef_environment',
                'chef_validator_name',
                'chef_validator_pem'
            ]
            # check for missing attributes
            f_locals = locals()
            chef_missing_parameters = [param for param in chef_required_parameters if not f_locals.get(param)]
            if any(chef_missing_parameters):
                raise MissingChefArguments(f"missing chef config parameters: {chef_missing_parameters}")

        #
        if isinstance(memory, str):
            memory = human_read_to_megabyte(memory)

        # validate that we have ips
        if not ip_addresses:
            raise EmptyIpAddressesList(f"vm named '{name}' contains no ip addresses")

        if len(ip_addresses) != count:
            raise InvalidNumberOfIpAddresses(
                f"vm named '{name}' has a different number of ip_addresses compared to the count")

        vm_template = SbpDataVcdVmTemplates(scope=scope, id_=ns, template_name=template_name,
                                            catalog_organization=catalog_organization,
                                            catalog_name=catalog_name)

        vault_backend_role = None
        if vault_policies:
            vault_backend_role = TokenAuthBackendRole(scope=scope,
                                                      id_=f'vm_token_auth_backend_role_{name}',
                                                      role_name=name,
                                                      allowed_policies=vault_policies,
                                                      orphan=vault_orphan,
                                                      token_period=vault_token_period,
                                                      renewable=vault_renewable,
                                                      )

        placement_policy = SbpGenericVmPlacementPolicy(strategy=placement_strategy, placements=placements)
        vms = SbpGenericVm(placement_policy=placement_policy, name=name, count=count, first_digit=first_digit,
                           formatting=naming_format, ip_addresses=ip_addresses)

        primary_vm = None
        for vm in vms:
            print(f'- host: {vm.name} in zone: {vm.zone_name} ip: {vm.ip}')

            placement_policy_id = SbpDataVcdVmPlacementPolicy(scope=scope, id_='', name=vms.placement_policy.name,
                                                              urn=vdc_urn, org=org).id
            vault_token_client_token = None
            if vault_backend_role:
                # create client role if requested
                vault_token_client_token = Token(scope=scope,
                                                 id_=f'vm_vault_token_{vm.name}',
                                                 role_name=name,
                                                 ttl=str(vault_token_period),
                                                 renewable=vault_renewable,
                                                 renew_min_lease=vault_renew_min_lease,
                                                 renew_increment=vault_renew_increment,
                                                 lifecycle={'ignore_changes': "all"},
                                                 depends_on=[vault_backend_role]
                                                 ).client_token

            # get vars and pass them to template
            ignore_vars = ['depends_on', 'modified_depends_on']
            template_vars = {key: item for key, item in locals().items() if
                             type(item) in [str, int, float, list, bool] and not (
                                     key.startswith('__') or key in ignore_vars)}
            template_vars['chef_run_list'] = str(chef_run_list)
            if template_vars.get('chef_validator_pem'):
                template_vars['chef_validator_pem'] = reindent(6, chef_validator_pem)
            for key, value in vars(vm).items():
                template_vars[f'vm_{key}'] = value
            template_vars['vm'] = vars(vm)
            template_vars['zone'] = vm.zone_name.split(' ')[0]
            if template_variables:
                for template_variable_key, template_variable_value in template_variables.items():
                    template_vars[template_variable_key] = template_variable_value
            template_file = Fn.templatefile(cloud_config_file, template_vars)

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

            new_vm = Vm(
                scope=scope,
                id_=f'vm_{vm.name}',
                name=vm.name,
                computer_name=vm.name,
                vapp_template_id=vm_template.id,
                memory=memory,
                memory_hot_add_enabled=memory_hot_add_enabled,
                cpu_hot_add_enabled=cpu_hot_add_enabled,
                power_on=power_on,
                placement_policy_id=placement_policy_id,
                network=kwargs.get('network', [SbpVcdVmNetwork(name=network_name, ip=vm.ip).settings]),
                guest_properties={
                    'user-data': Fn.sensitive(Fn.base64encode(template_file)),
                },
                lifecycle=lifecycle,
                depends_on=[time_sleep_destroy_vm],
                **kwargs
            )

            time_sleep = Sleep(
                scope=scope,
                id=f'vm_{vm.name}_ac_sleep',
                create_duration="60s",
                depends_on=[new_vm]
            )

            vapp_vm = DataVcdVapp(
                scope=scope,
                id_=f'vm_{vm.name}_vapp',
                vdc=new_vm.vdc,
                name=new_vm.vapp_name,
                depends_on=[time_sleep]
            )

            VappAccessControl(
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

            new_disk = None
            depends_on = [new_vm]
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
                        depends_on=depends_on,
                        delay_in_seconds="60s",
                    )
                    depends_on = [new_vm, new_disk]

            # primary to depend on is the last object created (vm or disk if any additionally attached)
            if not primary_vm:
                if new_disk:
                    primary_vm = new_disk
                else:
                    primary_vm = new_vm
