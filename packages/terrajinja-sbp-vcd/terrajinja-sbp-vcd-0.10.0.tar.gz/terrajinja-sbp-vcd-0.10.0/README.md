# terrajinja-sbp-vcd

This is an extension to the vault provider for the following modules.
The original documentation can be found [here](https://registry.terraform.io/providers/vmware/vcd/latest/docs)

# SBP Specific implementations
Here is a list of supported resources and their modifications


- [sbp.vcd.network_routed_v2](#sbpvcdnetwork-routed-v2)
- [sbp.vcd.vm_internal_disk](#sbpvcdvm-internal-disk)
- [sbp.vcd.vm](#sbpvcdvm)
- [sbp.vcd.rde](#sbpvcdrde)
- [sbp.vcd.nsxt_nat_rule](#sbpvcdnsxt-nat-rule)
- [sbp.vcd.nsxt_ip_set](#sbpvcdnsxt-ip-set)
- [sbp.vcd.nsxt_firewall](#sbpvcdnsxt-firewall)
- [sbp.vcd.nsxt_distributed_firewall](#sbpvcdnsxt-distributed-firewall)
- [sbp.vcd.nsxt_app_port_profile](#sbpvcdnsxt-app-port-profile)
- [sbp.vcd.nsxt_alb_virtual_service](#sbpvcdnsxt-alb-virtual-service)
- [sbp.vcd.nsxt_alb_pool](#sbpvcdnsxt-alb-pool)
- [sbp.vcd.data_vcd_vm_placement_policy](#sbpvcddata-vcd-vm-placement-policy)
- [sbp.vcd.data_vcd_nsxt_alb_edgegateway_service_engine_group](#sbpvcddata-vcd-nsxt-alb-edgegateway-service-engine-group)
- [sbp.vcd.data_vcd_catalog_vapp_template](#sbpvcddata-vcd-catalog-vapp-template)

## sbp.vcd.network_routed_v2
Original provider: [vcd.network_routed_v2](https://registry.terraform.io/providers/vmware/vcd/latest/docs/resources/network_routed_v2)

This custom provider adds the following:
- simplified and generic input for a network subnet

| old parameter | new parameter | description |
| ------ | ------ | ------ |
| static_ip_pool<br>gateway<br>prefix_length | cidr | the cidr parameter calculates and fills in the 3 replaced values. |
| dns1<br>dns2 | dns | dns is an array of dns servers, and automticly fills dns1 and dns2 |

### terrajinja-cli example
<details>

<summary>Click to expand</summary>

the following is a code snipet you can used in a terrajinja-cli template file.
This reads the `VCD group` and `Edge name` and creates a network named `mynetwork` with the given parameters.
```
terraform:
  resources:
    - task: read-virtual-datacenter-group
      module: vcd.data_vcd_vdc_group
      parameters:
        name: my_vdc

    - task: read-edge-gateway
      module: vcd.data_vcd_nsxt_edgegateway
      parameters:
        name: my_vdc_edge
        owner_id: $read-virtual-datacenter-group.id

    - task: my-network-backend
      module: sbp.vcd.network_routed_v2
      parameters:
        edge_gateway_id: $read-edge-gateway.id
        name: mynetwork
        cidr: 10.10.10.0/28
        dns: ["10.10.20.2", "10.10.20.3"]
        dns_suffix: my_domain.local
```

</details>

## sbp.vcd.vm_internal_disk
Original provider: [vcd.vm_internal_disk](https://registry.terraform.io/providers/vmware/vcd/latest/docs/resources/vm_internal_disk)

This custom provider adds the following:
- human readable input for size
- defaults for sbp.cloud disk settings
- optional delay in provisioning (required for vm boot delay)

| old parameter | new parameter | description |
| ------ | ------ | ------ |
| - | delay_in_seconds(int) | the delay in seconds before attaching the disk |
| bus_type | bus_type | default is set to "paravirtual" |
| storage_profile | storage_profile | default is set to "generic" |
| iops | iops | default is set to "5000" |
| size(int) | size(str) | input of size is no longer in mb, but in human readable format.<br>e.g. 1GB / 5TB / 3500MB |

### terrajinja-cli example
<details>

<summary>Click to expand</summary>

the following is a code snipet you can used in a terrajinja-cli template file.
```
terraform:
  resources:
    - task: vm-internal-disk
      module: sbp.vcd.vm_internal_disk
      parameters:
        vapp_name: "my_vapp_name"
        vm_name: "my_vm"
        vdc: "my_vdc
        size: "120GB"
        delay_in_seconds: 60
```

</details>

## sbp.vcd.vm
Original provider: [vcd.vm](https://registry.terraform.io/providers/vmware/vcd/latest/docs/resources/vm)

This custom provider adds the following:
- optional chef support, by bootstrapping and adding a run list
- optional vault support, automatic token generation for host
- optional automatic disk attachment
- automatic vm access control
- create multiple vm's based on count and naming scheme
- support for vm naming scheme (free format)
- support for vm distributuin scheme (which zone)

**main changes:**
| old parameter | new parameter | description |
| ------ | ------ | ------ |
| - | name(str) | main name of the vm's to be created |
| - | count(int) | the amount of vm's to create |
| memory(int) | memory(int\|str) | now accepts human readable input e.g. 1GB, 4GB, 1,5TB |
| network_name(dict) | network_name(str) | now network only requires a name, the rest is pre-filled |
| - | ip_addresses(list) | one IP for each vm |
| - | disks(list[dict]) | [internal disks](#internal-disks) adds additional internal disks (default: None) |
| - | template_name(str) | name of the template (e.g. "Debian_12-latest") |
| - | catalog_organization(str) | location of the template (default: NLCP-Templates) |
| - | catalog_name(str) | location of the template (default: NLCP-Templates) |
| - | placement_strategy(str) | [placement strategy](#placement-strategies), see below (default: one_per_zone) |
| - | placements(list) | zones where a vm can be placed |
| - | naming_format(str) | [naming format](#naming-format) of the vm name and numbering |
| - | first_digit(int) | number to start the vm name counter |
| - | depends_on_primary(bool) | the remaining nodes are created once the first node has been deployed (used for cluster creation) |
| - | shared_with_everyone(bool) | sets the default permission in vcloud for the vm's (default: True) |
| - | everyone_access_level(str) | sets the default permission in vcloud for the vm's (default: "Change") |

**optional for cloud-init:**
| old parameter | new parameter | description |
| ------ | ------ | ------ |
| - | cloud_config_file(str) | path to the cloud-init file for the vm |
| - | vcd_urn(str) | required for cloud-init template |
| - | dns_hosts(list) | required for cloud-init template, default name servers for the vm |
| - | proxy_url(str) | required for cloud-init template, default proxy to configure for a vm (default: '' e.g. no proxy) |

**optional for chef:**
| old parameter | new parameter | description |
| ------ | ------ | ------ |
| - | chef_run_list(list) | required for cloud-init template, vm's initial chef run list |
| - | chef_client_version | required for cloud-init template, chef client version to install |
| - | chef_encrypted_databag_secret(str) | required for cloud-init template, (default: None) |
| - | chef_server_url(str) | required for cloud-init template, (default: None) |
| - | chef_environment(str) | required for cloud-init template, (default: None) |
| - | chef_validator_name(str) | required for cloud-init template, (default: None) |
| - | chef_validator_pem(str) | required for cloud-init template, (default: None) |

**optional for vault:**
| old parameter | new parameter | description |
| ------ | ------ | ------ |
| - | vault_policies(list) | vault policy to attach to vm set |
| - | vault_token_period(int) | how long the vm's vault token is valid (default: 604800,) |
| - | vault_orphan(bool) | vault setting (default: True) |
| - | vault_renewable(bool) | vault setting (default: True |
| - | vault_renew_min_lease(int) | vault setting (default: 86400) |
| - | vault_renew_increment(int) | vault setting (default:604800) |

#### placement strategies
A placement strategy defines on which zones the vm's are deployed.

optional strategies:
- one_per_zone: spread vm's evenly across the provided zones
- tbd: more strategies to be added in the future

#### naming format
The format in which to generate the name for each vm in count
the details consist of an array that consists of a printf string, followed by its values. e.g.:
```
  naming_format: ["%s%d%02d", "name", "zone_id", "nr_per_zone"]
```
the first entry must be a string that supports printf
the remaining items are the values applied to the string

available options are:
- name (name of the vm)
- zone_id (numeric id of the zone)
- nr_per_zone (the number of the vm in the perticular zone)
- nr (the number of the vm)
- zone_name (name of the zone)


#### internal disks
to add additional disks, provide an array of disks in the following format:
```
  disk:
    - size: 10GB
      unit: 1
    - size: 10GB
      unit: 2
```

### terrajinja-cli example
<details>

<summary>Click to expand</summary>

the following is a code snipet you can used in a terrajinja-cli template file.
```
terraform:
  resources:
    - task: privoxy-vm
      module: sbp.vcd.vm
      parameters:
        name: tla-env-prx
        count: 2
        ip_addresses: [10.10.10.5, 10.10.10.6]
        cpus: 2
        memory: 4096
        network_name: dmz
        placement_strategy: one_per_zone
        first_digit: 1
        template_name: "Debian_12-latest"
        catalog_organization: NLCP-Templates
        catalog_name: NLCP-Templates
        cloud_config_file: "{{ config_directory }}/templates/cloud-config/debian_12.yaml"
        naming_format: [ "%s%d%02d", "name", "zone_id", "nr_per_zone" ]
        chef_server_url: http://chef.io/org
        chef_encrypted_databag_secret: {{ env['CHEF_ENCRYPTED_DATABAG_SECRET']  }}
        chef_validator_name: ofd-validator
        chef_validator_pem: |
{{ env['CHEF_VALIDATOR_PEM'] | indent( width=8, first=True) }}
        chef_client_version: 18
        dns_hosts: [ "8.8.8.8", "1.1.1.1" ]
        chef_environment: tlat
        chef_run_list: [ baseline_role, proxy_role ]
        vault_policies: [ proxy-policy ]
        vdc_urn: urn://1234:5678:9101
        vdc: my_vcd
        placements:
          - zone: 1
            name: "NLCP1 Non-Windows"
          - zone: 2
            name: "NLCP2 Non-Windows"        
        depends_on:
          - '$network-dmz'
```

</details>


## sbp.vcd.rde
Original provider: [vcd.rde](https://registry.terraform.io/providers/vmware/vcd/latest/docs/resources/rde)

This custom provider adds the following:
- simplified and generic input for a tanzu

| old parameter | new parameter | description |
| ------ | ------ | ------ |
| input_entity | - | generated inside the resource based on the new parameters |
| rde_type_id | - | generaeted inside the resource based on the new parameters |
| - | config_file_json | main json config file to provision tanzu |
| - | config_file_yaml | kubernetes template file embedded in json config |
| - | bearer | base64 encoded credentials, used inside the yaml for access to vcloud |
| - | vendor | default: vmware |
| - | nss | default: capvcdCluster |
| - | resolve | default: true |
| - | cap_vcd_cluster_version | default: 1.2.0 |

### terrajinja-cli example
<details>

<summary>Click to expand</summary>

the following is a code snipet you can used in a terrajinja-cli template file.
This creates a tanzu kubernetes deployment with the given parameters.
```
    - task: create-tanzu
      module: sbp.vcd.rde
      parameters:
        org: tla
        cap_vcd_cluster_version: "1.2.0"
        name: my-cluster-001
        config_file_json: "{{ config_directory }}/templates/kubernetes/tanzu.json"
        config_file_yaml: "{{ config_directory }}/templates/kubernetes/tanzu.yaml"
        bearer: {{ env['BEARER_B64'] }}
```

</details>

## sbp.vcd.nsxt_nat_rule
Original provider: [vcd.nsxt_nat_rule](https://registry.terraform.io/providers/vmware/vcd/latest/docs/resources/nsxt_nat_rule)

TODO: write doc

## sbp.vcd.nsxt_ip_set
Original provider: [vcd.nsxt_ip_set](https://registry.terraform.io/providers/vmware/vcd/latest/docs/resources/nsxt_ip_set)

TODO: write doc

## sbp.vcd.nsxt_firewall
Original provider: [vcd.nsxt_firewall](https://registry.terraform.io/providers/vmware/vcd/latest/docs/resources/nsxt_firewall)

TODO: write doc

## sbp.vcd.nsxt_distributed_firewall
Original provider: [vcd.nsxt_distributed_firewall](https://registry.terraform.io/providers/vmware/vcd/latest/docs/resources/nsxt_distributed_firewall)

TODO: write doc

## sbp.vcd.nsxt_app_port_profile
Original provider: [vcd.nsxt_app_port_profile](https://registry.terraform.io/providers/vmware/vcd/latest/docs/resources/nsxt_app_port_profile)

TODO: write doc

## sbp.vcd.nsxt_alb_virtual_service
Original provider: [vcd.nsxt_alb_virtual_service](https://registry.terraform.io/providers/vmware/vcd/latest/docs/resources/nsxt_alb_virtual_service)

TODO: write doc

## sbp.vcd.nsxt_alb_pool
Original provider: [vcd.nsxt_alb_pool](https://registry.terraform.io/providers/vmware/vcd/latest/docs/resources/nsxt_alb_pool)

TODO: write doc

## sbp.vcd.data_vcd_vm_placement_policy
Original provider: [vcd.data_vcd_vm_placement_policy](https://registry.terraform.io/providers/vmware/vcd/latest/docs/resources/data_vcd_vm_placement_policy)

TODO: write doc

## sbp.vcd.data_vcd_nsxt_alb_edgegateway_service_engine_group
Original provider: [vcd.data_vcd_nsxt_alb_edgegateway_service_engine_group](https://registry.terraform.io/providers/vmware/vcd/latest/docs/resources/data_vcd_nsxt_alb_edgegateway_service_engine_group)

TODO: write doc

## sbp.vcd.data_vcd_catalog_vapp_template
Original provider: [vcd.data_vcd_catalog_vapp_template](https://registry.terraform.io/providers/vmware/vcd/latest/docs/resources/data_vcd_catalog_vapp_template)

TODO: write doc
