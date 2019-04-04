## Lab 4 - Deploying Configs From a File

In the last lab, you deployed configurations while hard-coding commands in a playbook.  In this lab, you will deploy from a pre-built configuration file.

##### Step 1

Create a sub-directory called `configs` **inside** the `ansible` directory.  After creating it, navigate inside it:

```
ntc@jump-host:ansible$ mkdir junos
ntc@jump-host:ansible$ mkdir ios
ntc@jump-host:ansible$

```

##### Step 2

Create two files that will contain the SNMP configuration - one for Cisco and one for Juniper respectively.

```
ntc@jump-host:ansible$ touch junos/snmp.cfg
ntc@jump-host:ansible$ touch ios/snmp.cfg
ntc@jump-host:ansible$
```

##### Step 3

Open the `ios-snmp.cfg` file in your text editor and copy the following configuration into it:

```
snmp-server community ntc-team RO
snmp-server location FL_HQ        
snmp-server contact JAMES_CHARLES 

``` 

Save this file.


##### Step 4

Now open `junos-snmp.cfg` in a text editor and copy the following `junos` snmp configuration commands into it.

```
set snmp location FL_HQ
set snmp contact JAMES_CHARLES
set snmp community public authorization read-only
```

Save this file.

##### Step 5

Navigate back to the `ansible` directory and create a new playbook file.

```
ntc@jump-host:ansible$ touch snmp-config-03.yml
ntc@jump-host:ansible$
```

##### Step 6

Open this file with a text editor and create two plays similar to **Lab 1** to deploy the changes.
This time, however, we will use the source file to deploy the configuration instead of using commands inside the playbook.


```yaml

---

  - name: PLAY 1 - DEPLOYING SNMP CONFIGURATIONS ON IOS
    hosts: iosxe, vmx
    connection: network_cli
    gather_facts: no
  

    tasks:

      - name: TASK 1 in PLAY 1 - ENSURE SNMP COMMANDS EXIST ON IOS and JUNOS DEVICES
        cli_config:
          config: "{{ lookup('file', './{{ ansible_network_os }}/snmp.cfg') }}"


```

##### Step 7

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