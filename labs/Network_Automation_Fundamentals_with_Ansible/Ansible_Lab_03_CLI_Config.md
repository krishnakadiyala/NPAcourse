## Lab 3 - Deploying Configs From a File Using cli_config


In the last lab, you deployed from a pre-built configuration file using the vendor specific core modules with two different plays to separate the vendors.
In this lab we are going to do the same but in a single play and a single module.


##### Step 1

We are going to use the same configuration files from the previous lab. This time we are just going to replace them with new configurations.

Open the `ios-snmp.cfg` inside the `configs` directory file in your text editor delete the old configs and copy the following configuration into it:

```
snmp-server community ntc-team RO
snmp-server location FL_HQ        
snmp-server contact JAMES_CHARLES 
``` 

Save this file.


##### Step 2

Now open `junos-snmp.cfg` in a text editor and copy the following `junos` snmp configuration commands into it.

```
set snmp location FL_HQ
set snmp contact JAMES_CHARLES
set snmp community public authorization read-only
```

Save this file.

##### Step 3

Navigate back to the `ansible` directory and create a new playbook file.

```
ntc@jump-host:ansible$ touch snmp-config-03.yml
ntc@jump-host:ansible$
```

##### Step 4

Open this file with a text editor and create a single play to deploy the changes.
This time, we will use the source file to deploy the configuration instead of using commands inside the playbook.


```yaml

---

  - name: PLAY 1 - DEPLOYING SNMP CONFIGURATIONS ON IOS
    hosts: iosxe, vmx
    connection: network_cli
    gather_facts: no
  

    tasks:

      - name: TASK 1 in PLAY 1 - ENSURE SNMP COMMANDS EXIST ON IOS and JUNOS DEVICES
        cli_config:
          config: "{{ lookup('file', './configs/{{ ansible_network_os }}-snmp.cfg') }}"
```
>Note: We are using a `lookup` plugin that will read the specified file as raw text and `cli_config` will push the configuration to the device.

##### Step 5

Run the playbook.


```
ntc@jump-host:ansible$ ansible-playbook -i inventory snmp-config-03.yml

PLAY [PLAY 1 - DEPLOYING SNMP CONFIGURATIONS ON IOS] ******************************************************************************************************************

TASK [TASK 1 in PLAY 1 - ENSURE SNMP COMMANDS EXIST ON IOS and JUNOS DEVICES] *****************************************************************************************
changed: [csr1]
changed: [csr2]
changed: [vmx1]
changed: [vmx2]
changed: [csr3]
changed: [vmx3]

PLAY RECAP ************************************************************************************************************************************************************
csr1                       : ok=1    changed=1    unreachable=0    failed=0
csr2                       : ok=1    changed=1    unreachable=0    failed=0
csr3                       : ok=1    changed=1    unreachable=0    failed=0
vmx1                       : ok=1    changed=1    unreachable=0    failed=0
vmx2                       : ok=1    changed=1    unreachable=0    failed=0
vmx3                       : ok=1    changed=1    unreachable=0    failed=0 

ntc@jump-host:ansible$
```

You should see changes as these configs are new.  Feel free to re-run the playbook and check again.