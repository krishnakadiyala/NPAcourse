# Lab 4 - Using Check Mode and Verbosity

This lab builds on the first lab you did with sending SNMP configurations to network devices.

### Task 1 - Using Verbosity

##### Step 1

Copy your original playbook called `snmp-config-01.yml` to `snmp-config-04.yml`

```
ntc@ntc-training:ansible$ cp snmp-config-01.yml snmp-config-04.yml
ntc@ntc-training:ansible$
```

> Note: the `cp` command copies a file in Linux.


##### Step 2

Open the playbook, and add a new SNMP command to the `ios_config` `commands`  and `junos_config` `lines` parameter so that you have the following 4 commands in each list:

```yaml

      - name: TASK 1 in PLAY 1 - ENSURE SNMP COMMANDS EXIST ON IOS DEVICES
        ios_config:
          commands:
            - snmp-server community ntc-course RO
            - snmp-server community supersecret RW
            - snmp-server location NYC_HQ
            - snmp-server contact JOHN_SMITH
  
  
      - name: TASK 1 in PLAY 2 - ENSURE SNMP COMMANDS EXIST ON JUNOS DEVICES
        junos_config:
          lines:
            - set snmp community public authorization read-only
            - set snmp community supersecret authorization read-write
            - set snmp location NYC_HQ
            - set snmp contact JOHN_SMITH
```

Save the playbook.

##### Step 3

Execute the playbook, but this time use the `-v` flag.  This will run the playbook in verbose mode showing JSON data that is returned by every module.

> Note: every module returns JSON data and you can view that data by running the playbook in verbose mode.  You can add more levels of verbosity using doing `-vv`, `-vvv`, etc. up to 5 v's.


The core `<os>_config` modules will return the commands being sent to the device when running the playbook in verbose mode.

Let's take a look:

```
ntc@ntc-training:ansible$ ansible-playbook -i inventory snmp-config-04.yml -v
Using /etc/ansible/ansible.cfg as config file

PLAY [PLAY 1 - DEPLOYING SNMP CONFIGURATIONS ON IOS] ******************************************************************************************************************

TASK [TASK 1 in PLAY 1 - ENSURE SNMP COMMANDS EXIST ON IOS DEVICES] ***************************************************************************************************
changed: [csr1] => {"banners": {}, "changed": true, "commands": ["snmp-server community supersecret RW"], "updates": ["snmp-server community supersecret RW"]}
changed: [csr3] => {"banners": {}, "changed": true, "commands": ["snmp-server community supersecret RW"], "updates": ["snmp-server community supersecret RW"]}
changed: [csr2] => {"banners": {}, "changed": true, "commands": ["snmp-server community supersecret RW"], "updates": ["snmp-server community supersecret RW"]}

PLAY [PLAY 2 - DEPLOYING SNMP CONFIGURATIONS ON JUNOS] ****************************************************************************************************************

TASK [TASK 1 in PLAY 2 - ENSURE SNMP COMMANDS EXIST ON JUNOS DEVICES] *************************************************************************************************
changed: [vmx2] => {"changed": true}
changed: [vmx1] => {"changed": true}
changed: [vmx3] => {"changed": true}

PLAY RECAP ************************************************************************************************************************************************************
csr1                       : ok=1    changed=1    unreachable=0    failed=0   
csr2                       : ok=1    changed=1    unreachable=0    failed=0   
csr3                       : ok=1    changed=1    unreachable=0    failed=0   
vmx1                       : ok=1    changed=1    unreachable=0    failed=0   
vmx2                       : ok=1    changed=1    unreachable=0    failed=0   
vmx3                       : ok=1    changed=1    unreachable=0    failed=0 

ntc@ntc-training:ansible$

```

This is telling us that Ansible is only sending ONE command to the device -- Ansible is NOT sending every command in the playbook because by default, the _config modules are comparing the commands against a "show run" on the device.


>Note: Notice the __junos_config__  module does not return the one command that is being changed on the device. Not all modules are built the same, that's not necessarily a bad thing but it's always good to be aware of it and make sure to test all available modules for specific features based on a particular use case.  You will see that the modules that do not use network_cli may not return commands being sent in the JSON return data.


##### Step 4

Re-run the playbook once more verifying idempotency, e.g. no changes should be made.

```
ntc@ntc-training:ansible$ ansible-playbook -i inventory snmp-config-04.yml -v
Using /etc/ansible/ansible.cfg as config file

PLAY [PLAY 1 - DEPLOYING SNMP CONFIGURATIONS ON IOS] **********************************************************

TASK [TASK 1 in PLAY 1 - ENSURE SNMP COMMANDS EXIST ON IOS DEVICES] *******************************************
ok: [csr2] => {"changed": false}
ok: [csr3] => {"changed": false}
ok: [csr1] => {"changed": false}

PLAY [PLAY 2 - DEPLOYING SNMP CONFIGURATIONS ON JUNOS] ********************************************************

TASK [TASK 1 in PLAY 2 - ENSURE SNMP COMMANDS EXIST ON JUNOS DEVICES] *****************************************
ok: [vmx2] => {"changed": false}
ok: [vmx1] => {"changed": false}
ok: [vmx3] => {"changed": false}

PLAY RECAP ****************************************************************************************************
csr1                       : ok=1    changed=0    unreachable=0    failed=0
csr2                       : ok=1    changed=0    unreachable=0    failed=0
csr3                       : ok=1    changed=0    unreachable=0    failed=0
vmx1                       : ok=1    changed=0    unreachable=0    failed=0
vmx2                       : ok=1    changed=0    unreachable=0    failed=0
vmx3                       : ok=1    changed=0    unreachable=0    failed=0
```

As you can see no commands were sent to the devices.

### Task 2 - Using Check Mode with Verbosity

You've now seen how to see what commands Ansible is sending to the devices.  What if you want to see what Ansible _will do_? Luckily, Ansible supports a "dry run" or "check mode" to see what commands _would_ get sent if the playbook is run.  This is called **check mode** and you use the `-C` or `--check` flags on the command line to use check mode.

##### Step 1

Change the SNMP command for location to be "NYC_HQ_COLO"

On the IOS:
```yaml
- snmp-server location NYC_HQ_COLO
```

On the Junos:

```yaml
- set snmp location NYC_HQ_COLO
```

So that the complete playbook looks like this:

```yaml

---

  - name: PLAY 1 - DEPLOYING SNMP CONFIGURATIONS ON IOS
    hosts: iosxe
    connection: network_cli
    gather_facts: no

    tasks:

      - name: TASK 1 in PLAY 1 - ENSURE SNMP COMMANDS EXIST ON IOS DEVICES
        ios_config:
          commands:
            - snmp-server community ntc-course RO
            - snmp-server community supersecret RW
            - snmp-server location NYC_HQ_COLO
            - snmp-server contact JOHN_SMITH
            
  - name: PLAY 2 - DEPLOYING SNMP CONFIGURATIONS ON JUNOS
    hosts: vmx
    connection: netconf
    gather_facts: no

    tasks:

      - name: TASK 1 in PLAY 2 - ENSURE SNMP COMMANDS EXIST ON JUNOS DEVICES
        junos_config:
          lines:
            - set snmp community public authorization read-only
            - set snmp community supersecret authorization read-write
            - set snmp location NYC_HQ_COLO
            - set snmp contact JOHN_SMITH      
```


##### Step 2

Execute the playbook just with the "check mode" flag set:

```
ntc@ntc-training:ansible$ ansible-playbook -i inventory snmp-config-04.yml --check

PLAY [PLAY 1 - DEPLOYING SNMP CONFIGURATIONS ON IOS] **********************************************************

TASK [TASK 1 in PLAY 1 - ENSURE SNMP COMMANDS EXIST ON IOS DEVICES] *******************************************
changed: [csr3]
changed: [csr1]
changed: [csr2]

PLAY [PLAY 2 - DEPLOYING SNMP CONFIGURATIONS ON JUNOS] *********************************************************

TASK [TASK 1 in PLAY 2 - ENSURE SNMP COMMANDS EXIST ON JUNOS DEVICES] ******************************************
changed: [vmx1]
changed: [vmx2]
changed: [vmx3]

PLAY RECAP ****************************************************************************************************
csr1                       : ok=1    changed=1    unreachable=0    failed=0
csr2                       : ok=1    changed=1    unreachable=0    failed=0
csr3                       : ok=1    changed=1    unreachable=0    failed=0
vmx1                       : ok=1    changed=1    unreachable=0    failed=0
vmx2                       : ok=1    changed=1    unreachable=0    failed=0
vmx3                       : ok=1    changed=1    unreachable=0    failed=0


ntc@ntc-training:ansible$
```

Notice that this says "changed" for each device, but no change actually took place!

##### Step 3

Verify the "old" configuration is still there by SSH'ing into CSR1 and VMX1:

```commandline
ssh ntc@csr1
Warning: Permanently added 'csr1,172.24.0.17' (RSA) to the list of known hosts.
Password:
csr1#
csr1#show run | inc snmp-server location
snmp-server location NYC_HQ
csr1#
```

```commandline
ntc@ntc-training:ansible$ ssh ntc@vmx1
Warning: Permanently added 'vmx1,172.24.0.14' (ECDSA) to the list of known hosts.
Password:
vmx1>
vmx1> show configuration | match location | display set
set snmp location NYC_HQ
vmx1>
```
> The password is: ntc123

##### Step 4

**READ-ONLY STEP**

When you see "changed" when you run a playbook in check mode, it's telling you a change _will_ occur when you don't run it in check mode.  Check mode is often used at the beginning of change windows to see if a change would occur.

Note that you saw verbose mode returns what commands are sent to the device and check mode returns if a change will be made. If you combine check mode **and** verbose mode while executing a playbook, you will see the commands that will get sent!

>Note: Viewing what commands are being sent to the device will only be displayed on the IOS devices in this test. 

Let's try it.

##### Step 5

Run the playbook with check mode and verbose mode.

```
ntc@ntc-training:ansible$ ansible-playbook -i inventory snmp-config-04.yml --check -v
Using /etc/ansible/ansible.cfg as config file

PLAY [PLAY 1 - DEPLOYING SNMP CONFIGURATIONS ON IOS] **********************************************************

TASK [TASK 1 in PLAY 1 - ENSURE SNMP COMMANDS EXIST ON IOS DEVICES] *******************************************
changed: [csr3] => {"banners": {}, "changed": true, "commands": ["snmp-server location NYC_HQ_COLO"], "failed": false, "updates": ["snmp-server location NYC_HQ_COLO"]}
changed: [csr2] => {"banners": {}, "changed": true, "commands": ["snmp-server location NYC_HQ_COLO"], "failed": false, "updates": ["snmp-server location NYC_HQ_COLO"]}
changed: [csr1] => {"banners": {}, "changed": true, "commands": ["snmp-server location NYC_HQ_COLO"], "failed": false, "updates": ["snmp-server location NYC_HQ_COLO"]}

PLAY [PLAY 2 - DEPLOYING SNMP CONFIGURATIONS ON JUNOS] ****************************************************************************************************************

TASK [TASK 1 in PLAY 2 - ENSURE SNMP COMMANDS EXIST ON JUNOS DEVICES] *************************************************************************************************
changed: [vmx2] => {"changed": true}
changed: [vmx1] => {"changed": true}
changed: [vmx3] => {"changed": true}

PLAY RECAP ************************************************************************************************************************************************************
csr1                       : ok=1    changed=1    unreachable=0    failed=0   
csr2                       : ok=1    changed=1    unreachable=0    failed=0   
csr3                       : ok=1    changed=1    unreachable=0    failed=0   
vmx1                       : ok=1    changed=1    unreachable=0    failed=0   
vmx2                       : ok=1    changed=1    unreachable=0    failed=0   
vmx3                       : ok=1    changed=1    unreachable=0    failed=0 

ntc@ntc-training:ansible$
```

You now know which commands are going to get sent to the device.  This is super-handy when troubleshooting syntax issues, typos, and bad commands.

##### Step 6

Now that you, as a network engineer, "approved" the commands that will get sent to the device. You can remove check mode (feel free to keep verbose mode).

```
ntc@ntc-training:ansible$ ansible-playbook -i inventory snmp-config-04.yml -v
Using /etc/ansible/ansible.cfg as config file

PLAY [PLAY 1 - DEPLOYING SNMP CONFIGURATIONS ON IOS] **********************************************************

TASK [TASK 1 in PLAY 1 - ENSURE SNMP COMMANDS EXIST ON IOS DEVICES] *******************************************
changed: [csr1] => {"banners": {}, "changed": true, "commands": ["snmp-server location NYC_HQ_COLO"], "failed": false, "updates": ["snmp-server location NYC_HQ_COLO"]}
changed: [csr3] => {"banners": {}, "changed": true, "commands": ["snmp-server location NYC_HQ_COLO"], "failed": false, "updates": ["snmp-server location NYC_HQ_COLO"]}
changed: [csr2] => {"banners": {}, "changed": true, "commands": ["snmp-server location NYC_HQ_COLO"], "failed": false, "updates": ["snmp-server location NYC_HQ_COLO"]}

PLAY [PLAY 2 - DEPLOYING SNMP CONFIGURATIONS ON JUNOS] ******************************************************

TASK [TASK 1 in PLAY 2 - ENSURE SNMP COMMANDS EXIST ON JUNOS DEVICES] ****************************************
changed: [vmx1] => {"changed": true}
changed: [vmx2] => {"changed": true}
changed: [vmx3] => {"changed": true}

PLAY RECAP ****************************************************************************************************
csr1                       : ok=1    changed=1    unreachable=0    failed=0
csr2                       : ok=1    changed=1    unreachable=0    failed=0
csr3                       : ok=1    changed=1    unreachable=0    failed=0
vmx1                       : ok=1    changed=1    unreachable=0    failed=0
vmx2                       : ok=1    changed=1    unreachable=0    failed=0
vmx3                       : ok=1    changed=1    unreachable=0    failed=0

ntc@ntc-training:ansible$
```

##### Step 7

Finally, run the playbook one more time to verify idempotency.

```
ntc@ntc-training:ansible$ ansible-playbook -i inventory snmp-config-04.yml -v
Using /etc/ansible/ansible.cfg as config file

PLAY [PLAY 1 - DEPLOYING SNMP CONFIGURATIONS ON IOS] **********************************************************

TASK [TASK 1 in PLAY 1 - ENSURE SNMP COMMANDS EXIST ON IOS DEVICES] *******************************************
ok: [csr3] => {"changed": false, "failed": false}
ok: [csr1] => {"changed": false, "failed": false}
ok: [csr2] => {"changed": false, "failed": false}

PLAY [PLAY 2 - DEPLOYING SNMP CONFIGURATIONS ON JUNOS] ******************************************************

TASK [TASK 1 in PLAY 2 - ENSURE SNMP COMMANDS EXIST ON JUNOS DEVICES] ****************************************
ok: [vmx3] => {"changed": false}
ok: [vmx2] => {"changed": false}
ok: [vmx1] => {"changed": false}

PLAY RECAP ****************************************************************************************************
csr1                       : ok=1    changed=0    unreachable=0    failed=0
csr2                       : ok=1    changed=0    unreachable=0    failed=0
csr3                       : ok=1    changed=0    unreachable=0    failed=0
vmx1                       : ok=1    changed=0    unreachable=0    failed=0
vmx2                       : ok=1    changed=0    unreachable=0    failed=0
vmx3                       : ok=1    changed=0    unreachable=0    failed=0

ntc@ntc-training:ansible$
```

Nice work.

