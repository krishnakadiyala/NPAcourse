# Lab 8 - Auto-Create Directories using the file module

This lab introduces the `file` module to help us auto-create files and directories. This is helpful because as you'll eventually see, you may need to dynamically create directories based on group name or even hostname of the device.  One use-case is you want to issue 10 show commands per device and have a directory that is the hostname and files per command in that directory.  This is something that would be impossible to do manually (or at least, it would be very silly to do manually).

##### Step 1

Let's use `ansible-doc` to learn more about `file` module.

Type in the command `ansible-doc file`, this will open up a description of the module and available parameters.

The two main parameters we are going to focus on are `path` and `state`. 

```

ntc@ntc-training:ansible$ ansible-doc file

```

```commandline

= path
        Path to the file being managed.
        (Aliases: dest, name)
        
        
.....
        

- state
        If `directory', all intermediate subdirectories will be created if they do not exist. Since Ansible 1.7 they will be created with the supplied permissions. If `file', the file will NOT be created if it does
        not exist; see the `touch' value or the [copy] or [template] module if you want that behavior.  If `link', the symbolic link will be created or changed. Use `hard' for hardlinks. If `absent', directories will
        be recursively deleted, and files or symlinks will be unlinked. Note that `absent' will not cause `file' to fail if the `path' does not exist as the state did not change. If `touch' (new in 1.4), an empty file
        will be created if the `path` does not exist, while an existing file or directory will receive updated file access and modification times (similar to the way `touch` works from the command line).
        (Choices: absent, directory, file, hard, link, touch)[Default: file]
        
 ....


```


##### Step 2


Create a file called `auto-create.yml` for your playbook. 

```
ntc@ntc-training:ansible$ touch auto-create.yml
ntc@ntc-training:ansible$
```




##### Step 3

Now open `auto-create.yml` with a text editor and create a play called `Auto Generate Files and Directories`

> **Note:**  The connection type we are using is local since we are not going to ssh into any devices for this lab. 


```yaml

---

  - name: Auto Generate Files and Directories
    hosts: all
    connection: local
    gather_facts: no

```

##### Step 4

Add the first task using the `file` module and call it `CREATE DIRECTORIES BASED ON OS`. The `path` parameter will specify the location of where the file will be created and the `state` parameter will indicate what type of file will be created. 


```yaml

---

  - name: Auto Generate Files and Directories
    hosts: all
    connection: local
    gather_facts: no

    tasks:

      - name: CREATE DIRECTORIES BASED ON OS
        file:
          path: ./tmp/{{ ansible_network_os }}/
          state: directory
          
          
          
```

##### Step 5

Save and execute the playbook.

You should see the following output. 


```commandline

ntc@ntc-training:ansible$ ansible-playbook -i inventory auto-create.yml

PLAY [Auto Generate Files and Directories] ***************************************

TASK [CREATE DIRECTORIES BASED ON OS] ********************************************
ok: [vmx3]
ok: [vmx2]
changed: [nxos-spine1]
changed: [vmx1]
ok: [nxos-spine2]
ok: [csr2]
changed: [csr1]
ok: [csr3]
changed: [eos-leaf1]
ok: [eos-leaf2]
ok: [eos-spine1]
ok: [eos-spine2]

PLAY RECAP ***********************************************************************
csr1                       : ok=1    changed=1    unreachable=0    failed=0
csr2                       : ok=1    changed=0    unreachable=0    failed=0
csr3                       : ok=1    changed=0    unreachable=0    failed=0
eos-leaf1                  : ok=1    changed=1    unreachable=0    failed=0
eos-leaf2                  : ok=1    changed=0    unreachable=0    failed=0
eos-spine1                 : ok=1    changed=0    unreachable=0    failed=0
eos-spine2                 : ok=1    changed=0    unreachable=0    failed=0
nxos-spine1                : ok=1    changed=1    unreachable=0    failed=0
nxos-spine2                : ok=1    changed=0    unreachable=0    failed=0
vmx1                       : ok=1    changed=1    unreachable=0    failed=0
vmx2                       : ok=1    changed=0    unreachable=0    failed=0
vmx3                       : ok=1    changed=0    unreachable=0    failed=0
ntc@ntc-training:ansible$
```

You'll also note that not every device has a _changed_ task.  This is because the OS name is being used as a directory name and only the first device in that group actually makes the change.  The subsequent devices have only "changed ok" without a "change" because the module is idempotent.

##### Step 6

Type the command `tree` in the terminal to see the directory structure.

```
ntc@ntc-training:ansible$ tree
.
├── auto-create.yml
├── configs
│   ├── ios-snmp.cfg
│   └── junos-snmp.cfg
├── debug.yml
├── inventory
├── snmp-config-01.yml
├── snmp-config-02.yml
├── snmp-config-03.yml
├── snmp-config-04.yml
├── tmp
│   ├── eos
│   ├── ios
│   ├── junos
│   └── nxos
└── user_input.yml

6 directories, 10 files
```

##### Step 7

Add a new task to create a config file inside the new directories


> **Note:** The difference in the parameter here is that we are using `touch` to create an empty file. 
We are also using the Ansible magic variable of `inventory_hostname` to create unique files based on each device name.



```yaml

---

  - name: Auto Generate Files and Directories
    hosts: all
    connection: local
    gather_facts: no

    tasks:

      - name: CREATE DIRECTORIES BASED ON OS
        file:
          path: ./tmp/{{ ansible_network_os }}/
          state: directory

      - name: CREATE SNMP.CONF FILE
        file:
          path: ./tmp/{{ ansible_network_os }}/{{ inventory_hostname }}-snmp.conf
          state: touch 
            
```

##### Step 8

Save and execute the playbook. 

You should see the following output. 

```commandline

ntc@ntc-training:ansible$ ansible-playbook -i inventory auto-create.yml

PLAY [Auto Generate Files and Directories] *******************************

TASK [CREATE DIRECTORIES BASED ON OS] *************************************
ok: [nxos-spine1]
ok: [eos-leaf2]
ok: [csr1]
ok: [eos-leaf1]
ok: [nxos-spine2]
ok: [csr2]
ok: [csr3]
ok: [vmx1]
ok: [vmx2]
ok: [vmx3]
ok: [eos-spine1]
ok: [eos-spine2]
TASK [CREATE SNMP.CONF FILE] ***********************************************
changed: [eos-leaf1]
changed: [eos-leaf2]
changed: [nxos-spine1]
changed: [nxos-spine2]
changed: [csr1]
changed: [csr2]
changed: [csr3]
changed: [vmx1]
changed: [vmx2]
changed: [vmx3]
changed: [eos-spine1]
changed: [eos-spine2]

PLAY RECAP ******************************************************************
csr1                       : ok=2    changed=1    unreachable=0    failed=0
csr2                       : ok=2    changed=1    unreachable=0    failed=0
csr3                       : ok=2    changed=1    unreachable=0    failed=0
eos-leaf1                  : ok=2    changed=1    unreachable=0    failed=0
eos-leaf2                  : ok=2    changed=1    unreachable=0    failed=0
eos-spine1                 : ok=2    changed=1    unreachable=0    failed=0
eos-spine2                 : ok=2    changed=1    unreachable=0    failed=0
nxos-spine1                : ok=2    changed=1    unreachable=0    failed=0
nxos-spine2                : ok=2    changed=1    unreachable=0    failed=0
vmx1                       : ok=2    changed=1    unreachable=0    failed=0
vmx2                       : ok=2    changed=1    unreachable=0    failed=0
vmx3                       : ok=2    changed=1    unreachable=0    failed=0


```


##### Step 9

Type the command `tree` in the terminal again to see the new files in the directories.


```commandline
ntc@ntc-training:ansible$ tree
.
├── auto-create.yml
├── configs
│   ├── ios-snmp.cfg
│   └── junos-snmp.cfg
├── debug.yml
├── inventory
├── snmp-config-01.yml
├── snmp-config-02.yml
├── snmp-config-03.yml
├── snmp-config-04.yml
├── tmp
│   ├── eos
│   │   ├── eos-leaf1-snmp.conf
│   │   ├── eos-leaf2-snmp.conf
│   │   ├── eos-spine1-snmp.conf
│   │   └── eos-spine2-snmp.conf
│   ├── ios
│   │   ├── csr1-snmp.conf
│   │   ├── csr2-snmp.conf
│   │   └── csr3-snmp.conf
│   ├── junos
│   │   ├── vmx1-snmp.conf
│   │   ├── vmx2-snmp.conf
│   │   └── vmx3-snmp.conf
│   └── nxos
│       ├── nxos-spine1-snmp.conf
│       └── nxos-spine2-snmp.conf
└── user_input.yml

6 directories, 22 files

```



##### Step 10

Delete the first two tasks and replace the first task with one that deletes the `tmp` directory, cleaning up all the files.

> **Note:** The `file` module with the parameter `state: absent` will delete the directory and all the sub-directories and files in an idempotent fashion.


```yaml

---

  - name: Auto Generate Files and Directories
    hosts: all
    connection: local
    gather_facts: no

    tasks:

      - name: DELETE DIRECTORIES PREVIOUSLY CREATED BASED ON OS
        file:
          path: ./tmp
          state: absent
            
```

##### Step 11

Save and execute the playbook. 

You should see the following output. 


```commandline

ntc@ntc-training:ansible$ ansible-playbook -i inventory auto-create.yml


PLAY [Auto Generate Files and Directories] ***********************************************************************************************

TASK [DELETE DIRECTORIES PREVIOUSLY CREATED BASED ON OS] *********************************************************************************
changed: [csr1]
ok: [eos-leaf1]
ok: [nxos-spine2]
ok: [nxos-spine1]
ok: [eos-leaf2]
ok: [csr2]
ok: [csr3]
ok: [vmx1]
ok: [vmx2]
ok: [vmx3]
ok: [eos-spine2]
ok: [eos-spine1]

PLAY RECAP *******************************************************************************************************************************
csr1                       : ok=1    changed=1    unreachable=0    failed=0
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


```

##### Step 12

Type the command `tree` in the terminal again to see the new files in the directories.

```commandline
.
├── auto-create.yml
├── configs
│   ├── ios-snmp.cfg
│   └── junos-snmp.cfg
├── debug.yml
├── inventory
├── snmp-config-01.yml
├── snmp-config-02.yml
├── snmp-config-03.yml
├── snmp-config-04.yml
└── user_input.yml

1 directory, 10 files

```
