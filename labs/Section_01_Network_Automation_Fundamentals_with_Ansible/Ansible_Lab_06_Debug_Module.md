# Lab 6 - Improving Troubleshooting with the debug module

### Task 1 - Debugging Variables

This lab highlights the use of the `debug` module.  It offers you the ability to "print" variables to the terminal, which is often very helpful for verifying what a variable is set to.  As you can see from the last lab, you can see that variables can be defined in many locations in the inventory file, e.g. same variable for different groups.

Let's review a few ways the `debug` module helps with troubleshooting.

##### Step 1

Navigate to the `ansible` directory.

```
ntc@ntc-training:~$ cd ansible/
ntc@ntc-training:ansible$
```

##### Step 2

Create a playbook file called `debug.yml`.

```
ntc@ntc-training:ansible$ touch debug.yml
ntc@ntc-training:ansible$
```

Open the file in your text editor.

The playbook will consist of a single play and a single task.


##### Step 3

Use the following for the starting point of the playbook.  This will execute for all devices in the _iosxe_ group.

The task will simply print the variable `ntc_vendor` for each device in the group.

```yaml

---

  - name: USING THE DEBUG MODULE
    hosts: iosxe
    connection: local
    gather_facts: no


    tasks:
      - name: DEBUG AND PRINT TO TERMINAL
        debug: 
          var: ntc_vendor
```

Remember the `ntc_vendor` variable is simply a variable we created in the last lab for each group of devices and now we are going to print it for the **iosxe** group.

##### Step 4

Save and execute the playbook.

You should see the following output.

```
ntc@ntc-training:ansible$ ansible-playbook -i inventory debug.yml

PLAY [USING THE DEBUG MODULE] ***************************************************

TASK [DEBUG AND PRINT TO TERMINAL] **********************************************
ok: [csr1] => {
    "ntc_vendor": "cisco"
}
ok: [csr2] => {
    "ntc_vendor": "cisco"
}
ok: [csr3] => {
    "ntc_vendor": "cisco"
}

PLAY RECAP **********************************************************************
csr1                       : ok=1    changed=0    unreachable=0    failed=0
csr2                       : ok=1    changed=0    unreachable=0    failed=0
csr3                       : ok=1    changed=0    unreachable=0    failed=0

ntc@ntc-training:ansible$
```

Note, this just printed the variable to the terminal.

##### Step 5

Change the `hosts:` in the play definition to automate "all" devices in the inventory file.

```
    hosts: all
```

##### Step 6

Save and execute the playbook.

You should see the following output.

```
ntc@ntc-training:ansible$ ansible-playbook -i inventory debug.yml


PLAY [USING THE DEBUG MODULE] ***************************************************

TASK [DEBUG AND PRINT TO TERMINAL] **********************************************
ok: [eos-spine1] => {
    "ntc_vendor": "arista"
}
ok: [vmx1] => {
    "ntc_vendor": "juniper"
}
ok: [nxos-spine1] => {
    "ntc_vendor": "cisco"
}
ok: [nxos-spine2] => {
    "ntc_vendor": "cisco"
}
ok: [eos-spine2] => {
    "ntc_vendor": "arista"
}
ok: [vmx3] => {
    "ntc_vendor": "juniper"
}
ok: [csr1] => {
    "ntc_vendor": "cisco"
}
ok: [csr3] => {
    "ntc_vendor": "cisco"
}
ok: [csr2] => {
    "ntc_vendor": "cisco"
}
ok: [vmx2] => {
    "ntc_vendor": "juniper"
}
ok: [eos-leaf1] => {
    "ntc_vendor": "arista"
}
ok: [eos-leaf2] => {
    "ntc_vendor": "arista"
}

PLAY RECAP **********************************************************************
csr1                       : ok=1    changed=0    unreachable=0    failed=0
csr2                       : ok=1    changed=0    unreachable=0    failed=0
csr3                       : ok=1    changed=0    unreachable=0    failed=0
eos-leaf1                  : ok=1    changed=0    unreachable=0    failed=0
eos-leaf2                  : ok=1    changed=0    unreachable=0    failed=0
eos-spine1                 : ok=1    changed=0    unreachable=0    failed=0
eos-spine2                 : ok=1    changed=0    unreachable=0    failed=0
nxos-spine1                : ok=1    changed=0    unreachable=0    failed=0
nxos-spine2                : ok=1    changed=0    unreachable=0    failed=0
vmx1                       : ok=1    changed=0    unreachable=0    failed=0
vmx2                       : ok=1    changed=0    unreachable=0    failed=0
vmx3                       : ok=1    changed=0    unreachable=0    failed=0

ntc@ntc-training:ansible$
```

See how we can quickly view the same variable for all devices quite easily?

### Task 2 - Adding & Printing More Group Variables

##### Step 1

Add a variable called `ntc_device_type` to the `[all:vars]` section of the inventory file.

The updated section should look like this:

```
[all:vars]
ansible_user=ntc
ansible_ssh_pass=ntc123
ntc_device_type=unknown
```

##### Step 2

Add a task to the playbook to debug the `device_type` variable so the playbook reflects the following:

```yaml

---

  - name: USING THE DEBUG MODULE
    hosts: all
    connection: local
    gather_facts: no


    tasks:
      - name: DEBUG AND PRINT TO TERMINAL
        debug:
          var: ntc_vendor

      - name: DEBUG AND PRINT DEVICE TYPE TO TERMINAL
        debug:
          var: ntc_device_type
```

##### Step 3

Save and execute the following:

```
ntc@ntc-training:ansible$ ansible-playbook -i inventory debug.yml
```

You should see the following output for the new task:

```
TASK [DEBUG AND PRINT DEVICE TYPE TO TERMINAL] **********************************
ok: [eos-spine1] => {
    "ntc_device_type": "unknown"
}
ok: [eos-spine2] => {
    "ntc_device_type": "unknown"
}
ok: [eos-leaf1] => {
    "ntc_device_type": "unknown"
}
ok: [eos-leaf2] => {
    "ntc_device_type": "unknown"
}
ok: [vmx1] => {
    "ntc_device_type": "unknown"
}
ok: [vmx2] => {
    "ntc_device_type": "unknown"
}
ok: [vmx3] => {
    "ntc_device_type": "unknown"
}
ok: [csr1] => {
    "ntc_device_type": "unknown"
}
ok: [csr2] => {
    "ntc_device_type": "unknown"
}
ok: [csr3] => {
    "ntc_device_type": "unknown"
}
ok: [nxos-spine1] => {
    "ntc_device_type": "unknown"
}
ok: [nxos-spine2] => {
    "ntc_device_type": "unknown"
}
```

##### Step 4

Update the inventory file so it includes a group-based variable called `ntc_device_type`
 for the `nxos` group and for the `iosxe` group.  Set them to be "n9kv" and "csr1000v" respectively.

Those two groups should now look like this:

```
[iosxe:vars]
ansible_network_os=ios
ntc_api=ssh
ntc_vendor=cisco
ntc_device_type=csr1000v

[nxos:vars]
ansible_network_os=nxos
ntc_api=nxapi
ntc_vendor=cisco
ntc_device_type=n9kv
```

##### Step 5

Save and execute the following:

```
ntc@ntc-training:ansible$ ansible-playbook -i inventory debug.yml
```

You should see the following output for the new task:

```
TASK [DEBUG AND PRINT DEVICE TYPE TO TERMINAL] **********************************
ok: [eos-spine1] => {
    "ntc_device_type": "unknown"
}
ok: [eos-spine2] => {
    "ntc_device_type": "unknown"
}
ok: [eos-leaf1] => {
    "ntc_device_type": "unknown"
}
ok: [eos-leaf2] => {
    "ntc_device_type": "unknown"
}
ok: [vmx1] => {
    "ntc_device_type": "unknown"
}
ok: [vmx2] => {
    "ntc_device_type": "unknown"
}
ok: [vmx3] => {
    "ntc_device_type": "unknown"
}
ok: [csr1] => {
    "ntc_device_type": "csr1000v"
}
ok: [csr2] => {
    "ntc_device_type": "csr1000v"
}
ok: [csr3] => {
    "ntc_device_type": "csr1000v"
}
ok: [nxos-spine1] => {
    "ntc_device_type": "n9kv"
}
ok: [nxos-spine2] => {
    "ntc_device_type": "n9kv"
}
```

See how the more specific group variables are taking priority over the _all_ group?


### Task 3 - Adding & Printing Host Variables

In this task, you'll add "host based variables" to two hosts and print them to the terminal using the same playbook as the previous task.

##### Step 1

Add two host variables.  For **csr1**, set the value to "csr1000v-ng" and for **nxos-spine1**, set the value to "n9k":

```

[iosxe]
csr1    ntc_device_type=csr1000v-ng
csr2
csr3

[nxos-spines]
nxos-spine1  ntc_device_type=n9k
nxos-spine2
```

##### Step 2

Save the inventory file.

##### Step 3

Execute the playbook.  You should see the following relevant output:

```
TASK [DEBUG AND PRINT DEVICE TYPE TO TERMINAL] *****************************************************
ok: [eos-spine1] => {
    "ntc_device_type": "unknown"
}
ok: [eos-spine2] => {
    "ntc_device_type": "unknown"
}
ok: [eos-leaf1] => {
    "ntc_device_type": "unknown"
}
ok: [eos-leaf2] => {
    "ntc_device_type": "unknown"
}
ok: [vmx1] => {
    "ntc_device_type": "unknown"
}
ok: [vmx2] => {
    "ntc_device_type": "unknown"
}
ok: [vmx3] => {
    "ntc_device_type": "unknown"
}
ok: [csr1] => {
    "ntc_device_type": "csr1000v-ng"
}
ok: [csr2] => {
    "ntc_device_type": "csr1000v"
}
ok: [csr3] => {
    "ntc_device_type": "csr1000v"
}
ok: [nxos-spine1] => {
    "ntc_device_type": "n9k"
}
ok: [nxos-spine2] => {
    "ntc_device_type": "n9kv"
}
```

Take a minute to think about the variable priority occurring.  The **all** group is serving as the default, then specific group variables take priority over the **all** group, and then host variables take priority over the specific group variables.


### Task 4 - Using the msg Parameter

This task will introduce the `msg` parameter for the `debug` module.  Using `msg` is mutually exclusive with the `var` parameter.

When you just want to print a single variable, you use the `var` parameter.  If you want to add context (add a full sentence), you should use the `msg` parameter.

##### Step 1

Add a new task to the playbook to debug the `inventory_hostname` and `ansible_network_os` variables.

**IMPORTANT**: The `inventory_hostname` variable is a built-in variable that's equal to the hostname of the device as you've defined it in the inventory file.

```yaml
---

  - name: USING THE DEBUG MODULE
    hosts: all
    connection: local
    gather_facts: no


    tasks:
      - name: DEBUG AND PRINT TO TERMINAL
        debug: 
          var: ntc_vendor

      - name: DEBUG AND PRINT DEVICE TYPE TO TERMINAL
        debug:
          var: ntc_device_type

      - name: DEBUG AND PRINT THE OS
        debug: 
          msg: "The OS for {{ inventory_hostname }} is {{ ansible_network_os }}."
```

##### Step 2

Save and execute the playbook.

You'll see the relevant output for the 3rd task in the playbook:

```
TASK [DEBUG AND PRINT THE OS] ***************************************************
ok: [eos-spine1] => {
    "msg": "The OS for eos-spine1 is eos."
}
ok: [eos-spine2] => {
    "msg": "The OS for eos-spine2 is eos."
}
ok: [eos-leaf1] => {
    "msg": "The OS for eos-leaf1 is eos."
}
ok: [eos-leaf2] => {
    "msg": "The OS for eos-leaf2 is eos."
}
ok: [vmx1] => {
    "msg": "The OS for vmx1 is junos."
}
ok: [vmx2] => {
    "msg": "The OS for vmx2 is junos."
}
ok: [vmx3] => {
    "msg": "The OS for vmx3 is junos."
}
ok: [csr1] => {
    "msg": "The OS for csr1 is ios."
}
ok: [csr2] => {
    "msg": "The OS for csr2 is ios."
}
ok: [csr3] => {
    "msg": "The OS for csr3 is ios."
}
ok: [nxos-spine1] => {
    "msg": "The OS for nxos-spine1 is nxos."
}
ok: [nxos-spine2] => {
    "msg": "The OS for nxos-spine2 is nxos."
}
```



### Task 5 - Using the YAML Syntax for Tasks

Your playbook should look like this:

```yaml

---

  - name: USING THE DEBUG MODULE
    hosts: all
    connection: local
    gather_facts: no


    tasks:
      - name: DEBUG AND PRINT TO TERMINAL
        debug:
          var: ntc_vendor

      - name: DEBUG AND PRINT DEVICE TYPE TO TERMINAL
        debug:
          var: ntc_device_type

      - name: DEBUG AND PRINT THE OS
        debug:
          msg: "The OS for {{ inventory_hostname }} is {{ ansible_network_os }}."

```

This is using one type of syntax supported within the playbook in which it is `parameter=value`, e.g. `var=ntc_vendor` and `var=ntc_device_type`.

However, Ansible also supports a more native YAML syntax using colons in which it becomes `parameter: value` indented as a key under the module name. For example, this is what the first task would look like:

```yaml
      - name: DEBUG AND PRINT TO TERMINAL
        debug:
          var: ntc_vendor
```

##### Step 1

Convert this playbook to using the YAML syntax.

```yaml

---

  - name: USING THE DEBUG MODULE
    hosts: all
    connection: local
    gather_facts: no


    tasks:
      - name: DEBUG AND PRINT TO TERMINAL
        debug:
          var: ntc_vendor

      - name: DEBUG AND PRINT DEVICE TYPE TO TERMINAL
        debug:
          var: ntc_device_type

      - name: DEBUG AND PRINT THE OS
        debug:
          msg: "The OS for {{ inventory_hostname }} is {{ ansible_network_os }}."
```

##### Step 2

Re-run the playbook ensuring there are no indentation issues.

### Task 6 - Exploring built-in Variables

This task will introduce built-in variables or another way to call them are __magic__ variables. These variables are built-in to Ansible to reflect internal state. 


##### Step 1

In the __inventory__ file add `ansible_host=10.1.1.1` as a host variable to `csr2`. The `ansible_host` variable is helpful if the inventory hostname is not in DNS or `/etc/hosts`. You can set it to the IP address of the host and use it instead of `inventory_hostname` to access IP/FQDN.  This was also covered briefly in the last lab.


```text
[iosxe]
csr1    ntc_device_type=csr1000v-ng
csr2    ansible_host=10.1.1.1
csr3
```


##### Step 2

Add a new task to the existing playbook to see the difference between `inventory_hostname` and `ansible_host`.

```yaml

      - name: DEBUG AND PRINT INVENTORY_HOSTNAME VS ANSIBLE_HOST
        debug: 
           msg: "Devices defined in inventory_hostname: {{ inventory_hostname }} and ansible_host: {{ ansible_host }}"
```

##### Step 3

Save and execute the playbook.

You'll see the relevant output for the 4th task in the playbook:


```

TASK [DEBUG AND PRINT INVENTORY_HOSTNAME VS ANSIBLE_HOST] *******************************************************
ok: [eos-spine1] => {
    "msg": "Devices defined in inventory_hostname: eos-spine1 and ansible_host: eos-spine1"
}
ok: [eos-spine2] => {
    "msg": "Devices defined in inventory_hostname: eos-spine2 and ansible_host: eos-spine2"
}
ok: [csr1] => {
    "msg": "Devices defined in inventory_hostname: csr1 and ansible_host: csr1"
}
ok: [csr2] => {
    "msg": "Devices defined in inventory_hostname: csr2 and ansible_host: 10.1.1.1"
}
ok: [csr3] => {
    "msg": "Devices defined in inventory_hostname: csr3 and ansible_host: csr3"
}
ok: [vmx1] => {
    "msg": "Devices defined in inventory_hostname: vmx1 and ansible_host: vmx1"
}
ok: [vmx2] => {
    "msg": "Devices defined in inventory_hostname: vmx2 and ansible_host: vmx2"
}
ok: [vmx3] => {
    "msg": "Devices defined in inventory_hostname: vmx3 and ansible_host: vmx3"
}
ok: [nxos-spine1] => {
    "msg": "Devices defined in inventory_hostname: nxos-spine1 and ansible_host: nxos-spine1"
}
ok: [nxos-spine2] => {
    "msg": "Devices defined in inventory_hostname: nxos-spine2 and ansible_host: nxos-spine2"
}
ok: [eos-leaf1] => {
    "msg": "Devices defined in inventory_hostname: eos-leaf1 and ansible_host: eos-leaf1"
}
ok: [eos-leaf2] => {
    "msg": "Devices defined in inventory_hostname: eos-leaf2 and ansible_host: eos-leaf2"
}
```


**IMPORTANT**

**Remove ansible_host=10.1.1.1 from the inventory or it will cause problems in later labs.**


##### Step 4

Add a new task to the playbook to debug a variable called `play_hosts`.  It will return a list of inventory hostnames that are in scope for the current play:

```yaml
      - name: DEBUG AND PRINT LIST OF PLAY_HOSTS
        debug: 
          var: play_hosts
```

##### Step 5

Save and execute the playbook.

You'll see the relevant output for the 5th task in the playbook:

```commandline
TASK [DEBUG AND PRINT LIST OF PLAY_HOSTS] *****************************************************************
ok: [eos-spine1] => {
    "play_hosts": [
        "eos-spine1",
        "eos-spine2",
        "nxos-spine1",
        "nxos-spine2",
        "csr1",
        "csr2",
        "csr3",
        "vmx1",
        "vmx2",
        "vmx3",
        "eos-leaf1",
        "eos-leaf2"
    ]
}
ok: [eos-spine2] => {
    "play_hosts": [
        "eos-spine1",
        "eos-spine2",
        "nxos-spine1",
        "nxos-spine2",
        "csr1",
        "csr2",
        "csr3",
        "vmx1",
        "vmx2",
        "vmx3",
        "eos-leaf1",
        "eos-leaf2"
    ]
}
ok: [nxos-spine1] => {
    "play_hosts": [
        "eos-spine1",
        "eos-spine2",
        "nxos-spine1",
        "nxos-spine2",
        "csr1",
        "csr2",
        "csr3",
        "vmx1",
        "vmx2",
        "vmx3",
        "eos-leaf1",
        "eos-leaf2"
    ]
}
ok: [nxos-spine2] => {
    "play_hosts": [
        "eos-spine1",
        "eos-spine2",
        "nxos-spine1",
        "nxos-spine2",
        "csr1",
        "csr2",
        "csr3",
        "vmx1",
        "vmx2",
        "vmx3",
        "eos-leaf1",
        "eos-leaf2"
    ]
}

..... output ommited

```

You'll also note that EVERY device actually has a `play_hosts` variable. 

##### Step 6

Add a new task to the existing playbook. To debug `group_names` which will return a list of all groups that the **current host** is a member of.

```yaml
      - name: DEBUG AND PRINT GROUP_NAMES
        debug: 
          var: group_names
```

##### Step 7

Save and execute the playbook.
You'll see the relevant output for the 6th task in the playbook:

```commandline

TASK [DEBUG AND PRINT GROUP_NAMES] ****************************************************

ok: [eos-spine1] => {
    "group_names": [
        "eos",
        "eos-spines"
    ]
}
ok: [eos-spine2] => {
    "group_names": [
        "eos",
        "eos-spines"
    ]
}
ok: [csr1] => {
    "group_names": [
        "AMER",
        "iosxe"
    ]
}
ok: [csr2] => {
    "group_names": [
        "AMER",
        "iosxe"
    ]
}
ok: [csr3] => {
    "group_names": [
        "AMER",
        "iosxe"
    ]
}
ok: [vmx1] => {
    "group_names": [
        "EMEA",
        "vmx"
    ]
}
ok: [vmx2] => {
    "group_names": [
        "EMEA",
        "vmx"
    ]
}
ok: [vmx3] => {
    "group_names": [
        "EMEA",
        "vmx"
    ]
}
ok: [nxos-spine1] => {
    "group_names": [
        "nxos",
        "nxos-spines"
    ]
}
ok: [nxos-spine2] => {
    "group_names": [
        "nxos",
        "nxos-spines"
    ]
}
ok: [eos-leaf1] => {
    "group_names": [
        "eos",
        "eos-leaves"
    ]
}
ok: [eos-leaf2] => {
    "group_names": [
        "eos",
        "eos-leaves"
    ]
}

..... output ommited
```

##### Step 8

In the play definition change `hosts: all` to `hosts: csr1` so we only target one device. 

```yaml

---

  - name: USING THE DEBUG MODULE
    hosts: csr1
    connection: local
    gather_facts: no

```


##### Step 9

Add a new task to the existing playbook. Now we'll debug a variable called `groups` which will return a dictionary (or hash) in which all the keys are all group names defined in the inventory file and values are list of hosts that are members of the group.

```yaml
      - name: DEBUG AND PRINT GROUPS
        debug: 
          var: groups
```

##### Step 10

Save and execute the playbook.
You'll see the relevant output for the 7th task in the playbook:

```commandline

TASK [DEBUG AND PRINT GROUPS] ******************************************************************************************************************************************************************************
ok: [csr1] => {
    "groups": {
        "AMER": [
            "csr1",
            "csr2",
            "csr3"
        ],
        "EMEA": [
            "vmx1",
            "vmx2",
            "vmx3"
        ],
        "all": [
            "eos-spine1",
            "eos-spine2",
            "csr1",
            "csr2",
            "csr3",
            "vmx1",
            "vmx2",
            "vmx3",
            "nxos-spine1",
            "nxos-spine2",
            "eos-leaf1",
            "eos-leaf2"
        ],
        "eos": [
            "eos-spine1",
            "eos-spine2",
            "eos-leaf1",
            "eos-leaf2"
        ],
        "eos-leaves": [
            "eos-leaf1",
            "eos-leaf2"
        ],
        "eos-spines": [
            "eos-spine1",
            "eos-spine2"
        ],
        "iosxe": [
            "csr1",
            "csr2",
            "csr3"
        ],
        "nxos": [
            "nxos-spine1",
            "nxos-spine2"
        ],
        "nxos-spines": [
            "nxos-spine1",
            "nxos-spine2"
        ],
        "ungrouped": [],
        "vmx": [
            "vmx1",
            "vmx2",
            "vmx3"
        ]
    }
}

```

##### Step 11

Add a new task to the existing playbook so we can verify and see what version of Ansible is being used to execute the playbook.  The variable `ansible_version` will return a dictionary representing the Ansible major, minor, revision of the release.

```yaml

      - name: DEBUG AND PRINT ANSIBLE_VERSION
        debug: 
           msg: "Ansible Version: '{{ ansible_version }}'"
```

##### Step 12

Save and execute the playbook.
You'll see the relevant output for the 8th task in the playbook:


```commandline
TASK [DEBUG AND PRINT ANSIBLE_VERSION] *********************************************************************
ok: [csr1] => {
    "msg": "Ansible Version: '{'string': '2.8.5', 'full': '2.8.5', 'major': 2, 'minor': 8, 'revision': 5}'"
}
```

There are several more built-in variables, but this is a good start to understand what's possible while printing different variables with the `debug` module.
