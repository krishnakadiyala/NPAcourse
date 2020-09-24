# Lab 3 - Deploying Configs Using a Multi-Vendor Module

In the last lab, you deployed from a pre-built configuration file using the vendor specific core modules with two different plays to separate the vendors.  This would make it such that you need a play for every vendor (OS type) being used. 

In this lab the `cli_config` module will be used for both Cisco and Juniper devices. The goal is to show how `cli_config` can be used as a multi-vendor module.



##### Step 1


Navigate to the `ansible` directory and create a new playbook file called `snmp-config-03.yml`.

```bash
ntc@ntc-training:ansible$ touch snmp-config-03.yml
ntc@ntc-training:ansible$
```
##### Step 2

Open this file with a text editor and create a single play to deploy the changes.

Similar to the previous lab, SNMP commands will be used to make configuration changes. This time rather than using a configuration file, the `cli_config` module will take in as input the CLI commands.

```yaml

---

    - name: PLAY 1 - DEPLOYING SNMP CONFIGURATIONS ON IOS 
      hosts: iosxe
      connection: network_cli
      gather_facts: no

      tasks:

        - name: TASK 1 in PLAY 1 - ENSURE SNMP COMMANDS EXIST ON IOS DEVICES
          cli_config:
            config: | 
               snmp-server community ntc-team RO
               snmp-server location FL_HQ        
               snmp-server contact JAMES_CHARLES
```

Save this file.


##### Step 3

Run the playbook using the following command: `ansible-playbook -i inventory snmp-config-03.yml`

```bash
ntc@ntc-training:ansible$ ansible-playbook -i inventory snmp-config-03.yml

PLAY [PLAY 1 - DEPLOYING SNMP CONFIGURATIONS ON IOS] ***********************************************************************************************************************

TASK [TASK 1 in PLAY 1 - ENSURE SNMP COMMANDS EXIST ON IOS DEVICES] ***************************************************************************************************************
changed: [csr3]
changed: [csr2]
changed: [csr1]

PLAY RECAP *****************************************************************************************************************************************************************
csr1                       : ok=1    changed=1    unreachable=0    failed=0
csr2                       : ok=1    changed=1    unreachable=0    failed=0
csr3                       : ok=1    changed=1    unreachable=0    failed=0
```


##### Step 4

Add a second play to the playbook to target the Juniper devices using the same module.

> Note:  The `netconf` connection plugin is not being used since the `cli_config` module only supports the `network_cli`.


```yaml

---

    - name: PLAY 1 - DEPLOYING SNMP CONFIGURATIONS ON IOS 
      hosts: iosxe
      connection: network_cli
      gather_facts: no

      tasks:

        - name: TASK 1 in PLAY 1 - ENSURE SNMP COMMANDS EXIST ON IOS DEVICES
          cli_config:
            config: | 
              snmp-server community ntc-team RO
              snmp-server location FL_HQ        
              snmp-server contact JAMES_CHARLES

    - name: PLAY 2 - DEPLOYING SNMP CONFIGURATIONS ON JUNOS 
      hosts: vmx
      connection: network_cli
      gather_facts: no
         
      tasks:
         
        - name: TASK 1 in PLAY 2 - ENSURE SNMP COMMANDS EXIST ON VMX DEVICES
          cli_config:
            config: |
               set snmp location FL_HQ
               set snmp contact JAMES_CHARLES
               set snmp community public authorization read-only
```

Save this file.

##### Step 5


Run the Ansible playbook again. You should see changes on the VMX devices as these configs are new. On the Cisco devices the output should come back with no change since the configs already exist and the module is idempotent.


```bash
ntc@ntc-training:ansible$ ansible-playbook -i inventory snmp-config-03.yml

PLAY [PLAY 1 - DEPLOYING SNMP CONFIGURATIONS ON IOS] ***********************************************************************************************************************

TASK [TASK 1 in PLAY 1 - ENSURE SNMP COMMANDS EXIST ON IOS DEVICES] ********************************************************************************************************
ok: [csr3]
ok: [csr1]
ok: [csr2]

PLAY [PLAY 2 - DEPLOYING SNMP CONFIGURATIONS ON JUNOS] *********************************************************************************************************************

TASK [TASK 1 in PLAY 2 - ENSURE SNMP COMMANDS EXIST ON VMX DEVICES] ********************************************************************************************************
changed: [vmx1]
changed: [vmx2]
changed: [vmx3]

PLAY RECAP *****************************************************************************************************************************************************************
csr1                       : ok=1    changed=0    unreachable=0    failed=0
csr2                       : ok=1    changed=0    unreachable=0    failed=0
csr3                       : ok=1    changed=0    unreachable=0    failed=0
vmx1                       : ok=1    changed=1    unreachable=0    failed=0
vmx2                       : ok=1    changed=1    unreachable=0    failed=0
vmx3                       : ok=1    changed=1    unreachable=0    failed=0

```

##### Step 6

Add two more plays to the playbook that will make the same changes with the same modules, except this time rather than passing the commands on the task module, create a new variables inside the `vars` key for each vendor called `ios_commands` and `junos_commands` and add the same commands to them. In the task add the variable created and use `jinja2` syntax to give the module access to the commands stored in the variables.

> Note: The course will go into `jinja2` in more detail later.

```yaml

---

    - name: PLAY 1 - DEPLOYING SNMP CONFIGURATIONS ON IOS 
      hosts: iosxe
      connection: network_cli
      gather_facts: no

      tasks:

        - name: TASK 1 in PLAY 1 - ENSURE SNMP COMMANDS EXIST ON IOS DEVICES
          cli_config:
            config: | 
              snmp-server community ntc-team RO
              snmp-server location FL_HQ        
              snmp-server contact JAMES_CHARLES

    - name: PLAY 2 - DEPLOYING SNMP CONFIGURATIONS ON JUNOS 
      hosts: vmx
      connection: network_cli
      gather_facts: no
         
      tasks:
         
        - name: TASK 1 in PLAY 2 - ENSURE SNMP COMMANDS EXIST ON VMX DEVICES
          cli_config:
            config: |
               set snmp location FL_HQ
               set snmp contact JAMES_CHARLES
               set snmp community public authorization read-only
               
    - name: PLAY 3 - DEPLOYING SNMP CONFIGURATIONS ON IOS USING A VARIABLE
      hosts: iosxe
      connection: network_cli
      gather_facts: no
                
      vars:
        ios_commands: | 
             snmp-server community ntc-team RO
             snmp-server location FL_HQ        
             snmp-server contact JAMES_CHARLES

      tasks:
    
          - name: TASK 1 in PLAY 3 - ENSURE SNMP COMMANDS EXIST ON IOS DEVICES
            cli_config:
              config: "{{ ios_commands }}"
              
    - name: PLAY 4 - DEPLOYING SNMP CONFIGURATIONS ON JUNOS USING A VARIABLE
      hosts: vmx
      connection: network_cli
      gather_facts: no
                
      vars:
        junos_commands: |
             set snmp location FL_HQ
             set snmp contact JAMES_CHARLES
             set snmp community public authorization read-only
        
      tasks:
            
        - name: TASK 1 in PLAY 4 - ENSURE SNMP COMMANDS EXIST ON VMX DEVICES
          cli_config:
            config: "{{ junos_commands }}"
```

Save this file.


##### Step 7


Run the Ansible playbook again. There shouldn't be any changes to the configurations since the same commands are being used. The main difference here is that a variable is being used to pass in the configurations and it will not affect the changes to the devices unless the CLI configurations are changed. 


```bash
ntc@ntc-training:ansible$ ansible-playbook -i inventory snmp-config-03.yml

PLAY [PLAY 1 - DEPLOYING SNMP CONFIGURATIONS ON IOS] ***********************************************************************************************************************

TASK [TASK 1 in PLAY 1 - ENSURE SNMP COMMANDS EXIST ON IOS DEVICES] ********************************************************************************************************
ok: [csr2]
ok: [csr3]
ok: [csr1]

PLAY [PLAY 2 - DEPLOYING SNMP CONFIGURATIONS ON JUNOS] *********************************************************************************************************************

TASK [TASK 1 in PLAY 2 - ENSURE SNMP COMMANDS EXIST ON VMX DEVICES] ********************************************************************************************************
ok: [vmx1]
ok: [vmx3]
ok: [vmx2]

PLAY [PLAY 3 - DEPLOYING SNMP CONFIGURATIONS ON IOS USING A VARIABLE] ******************************************************************************************************

TASK [TASK 1 in PLAY 3 - ENSURE SNMP COMMANDS EXIST ON IOS DEVICES] ********************************************************************************************************
ok: [csr3]
ok: [csr2]
ok: [csr1]

PLAY [PLAY 4 - DEPLOYING SNMP CONFIGURATIONS ON JUNOS USING A VARIABLE] ****************************************************************************************************

TASK [TASK 1 in PLAY 4 - ENSURE SNMP COMMANDS EXIST ON VMX DEVICES] ********************************************************************************************************
ok: [vmx1]
ok: [vmx3]
ok: [vmx2]

PLAY RECAP *****************************************************************************************************************************************************************
csr1                       : ok=2    changed=0    unreachable=0    failed=0
csr2                       : ok=2    changed=0    unreachable=0    failed=0
csr3                       : ok=2    changed=0    unreachable=0    failed=0
vmx1                       : ok=2    changed=0    unreachable=0    failed=0
vmx2                       : ok=2    changed=0    unreachable=0    failed=0
vmx3                       : ok=2    changed=0    unreachable=0    failed=0

```

##### Step 8

Add one more play into the playbook. This last play will target both Juniper and Cisco devices in a single play. The variables also need to be modified so they can be accessed individually through a dictionary. In this task, rather than accessing an individual variable, the syntax will be `vendor_commands` for the parent key while the variables stored inside that key are `ios` and `junos`. Since `ansible_network_os` will return the OS of each vendor, the commands can be accessed through these variables. 

> Note: Later on this course will go into more detail on how to access data inside a dictionary. 



```yaml

---

    - name: PLAY 1 - DEPLOYING SNMP CONFIGURATIONS ON IOS 
      hosts: iosxe
      connection: network_cli
      gather_facts: no

      tasks:

        - name: TASK 1 in PLAY 1 - ENSURE SNMP COMMANDS EXIST ON IOS DEVICES
          cli_config:
            config: | 
              snmp-server community ntc-team RO
              snmp-server location FL_HQ        
              snmp-server contact JAMES_CHARLES

    - name: PLAY 2 - DEPLOYING SNMP CONFIGURATIONS ON JUNOS 
      hosts: vmx
      connection: network_cli
      gather_facts: no
         
      tasks:
         
        - name: TASK 1 in PLAY 2 - ENSURE SNMP COMMANDS EXIST ON VMX DEVICES
          cli_config:
            config: |
               set snmp location FL_HQ
               set snmp contact JAMES_CHARLES
               set snmp community public authorization read-only
               
    - name: PLAY 3 - DEPLOYING SNMP CONFIGURATIONS ON IOS USING A VARIABLE
      hosts: iosxe
      connection: network_cli
      gather_facts: no
                
      vars:
        ios_commands: | 
             snmp-server community ntc-team RO
             snmp-server location FL_HQ        
             snmp-server contact JAMES_CHARLES

      tasks:
    
          - name: TASK 1 in PLAY 3 - ENSURE SNMP COMMANDS EXIST ON IOS DEVICES
            cli_config:
              config: "{{ ios_commands }}"

    - name: PLAY 4 - DEPLOYING SNMP CONFIGURATIONS ON JUNOS USING A VARIABLE
      hosts: vmx
      connection: network_cli
      gather_facts: no
                
      vars:
        junos_commands: |
             set snmp location FL_HQ
             set snmp contact JAMES_CHARLES
             set snmp community public authorization read-only
        
      tasks:
            
        - name: TASK 1 in PLAY 4 - ENSURE SNMP COMMANDS EXIST ON VMX DEVICES
          cli_config:
            config: "{{ junos_commands }}"
          

    - name: PLAY 5 - DEPLOYING SNMP CONFIGURATIONS ON IOS AND JUNOS
      hosts: iosxe,vmx
      connection: network_cli
      gather_facts: no
                
      vars:
        vendor_commands:
          ios: |
            snmp-server community ntc-team RO
            snmp-server location FL_HQ        
            snmp-server contact JAMES_CHARLES
          junos: |
             set snmp location FL_HQ
             set snmp contact JAMES_CHARLES
             set snmp community public authorization read-only

      tasks:
    
          - name: TASK 1 in PLAY 5 - ENSURE SNMP COMMANDS EXIST ON IOS AND VMX DEVICES
            cli_config:
              config: "{{ vendor_commands[ansible_network_os] }}"
```
Save this file.

##### Step 9


Run the Ansible playbook again. There shouldn't be any changes to the configurations. The last play shows how the `cli_config` module can be used as a multi-vendor module in a single play.


```bash
ntc@ntc-training:ansible$ ansible-playbook -i inventory snmp-config-03.yml

PLAY [PLAY 1 - DEPLOYING SNMP CONFIGURATIONS ON IOS] ***********************************************************************************************************************

TASK [TASK 1 in PLAY 1 - ENSURE SNMP COMMANDS EXIST ON IOS DEVICES] ********************************************************************************************************
ok: [csr3]
ok: [csr2]
ok: [csr1]

PLAY [PLAY 2 - DEPLOYING SNMP CONFIGURATIONS ON JUNOS] *********************************************************************************************************************

TASK [TASK 1 in PLAY 2 - ENSURE SNMP COMMANDS EXIST ON VMX DEVICES] ********************************************************************************************************
ok: [vmx3]
ok: [vmx1]
ok: [vmx2]

PLAY [PLAY 3 - DEPLOYING SNMP CONFIGURATIONS ON IOS USING A VARIABLE] ******************************************************************************************************

TASK [TASK 1 in PLAY 3 - ENSURE SNMP COMMANDS EXIST ON IOS DEVICES] ********************************************************************************************************
ok: [csr1]
ok: [csr3]
ok: [csr2]

PLAY [PLAY 4 - DEPLOYING SNMP CONFIGURATIONS ON JUNOS USING A VARIABLE] ****************************************************************************************************

TASK [TASK 1 in PLAY 4 - ENSURE SNMP COMMANDS EXIST ON VMX DEVICES] ********************************************************************************************************
ok: [vmx1]
ok: [vmx3]
ok: [vmx2]

PLAY [PLAY 5 - DEPLOYING SNMP CONFIGURATIONS ON IOS AND JUNOS] *************************************************************************************************************

TASK [TASK 1 in PLAY 5 - ENSURE SNMP COMMANDS EXIST ON IOS AND VMX DEVICES] ************************************************************************************************
ok: [csr1]
ok: [csr3]
ok: [csr2]
ok: [vmx2]
ok: [vmx1]
ok: [vmx3]

PLAY RECAP *****************************************************************************************************************************************************************
csr1                       : ok=3    changed=0    unreachable=0    failed=0
csr2                       : ok=3    changed=0    unreachable=0    failed=0
csr3                       : ok=3    changed=0    unreachable=0    failed=0
vmx1                       : ok=3    changed=0    unreachable=0    failed=0
vmx2                       : ok=3    changed=0    unreachable=0    failed=0
vmx3                       : ok=3    changed=0    unreachable=0    failed=0

```