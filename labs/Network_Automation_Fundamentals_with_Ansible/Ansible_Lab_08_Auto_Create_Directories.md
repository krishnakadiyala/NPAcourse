## Lab 8 - Auto-Create Directories using the file module

This lab introduces the `file` module to help us auto-create files and directories.

##### Step 1

Type in the command `ansible-doc file`, this will open up a description of the module and available parameters. The two main parameters we are going to focus on are `path` and `state`. 

```

ntc@jump-host:ansible$ ansible-doc file

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
ntc@jump-host:ansible$ touch auto-create.yml
ntc@jump-host:ansible$
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
          path: ./{{ ansible_network_os }}/
          state: directory
          
          
          
```

##### Step 5

Save and execute the playbook.

You should see the following output. 


```commandline

ntc@jump-host:ansible$ ansible-playbook -i inventory auto-create.yml

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
ntc@jump-host:ansible$
```

##### Step 6

Type the command `tree` in the terminal to see the directory structure.

```
ntc@jump-host:ansible$ tree
.
├── auto-create.yml
├── eos
├── inventory
├── ios
├── junos
└── nxos

4 directories, 2 files
```

##### Step 7

Add a new task to create the config file inside the new diretories

> **Note:** The difference in the parameter here is that we are using `touch` to create an empty file. 


```yaml

---

  - name: Auto Generate Files and Directories
    hosts: all
    connection: local
    gather_facts: no

    tasks:

      - name: CREATE DIRECTORIES BASED ON OS
        file:
          path: ./{{ ansible_network_os }}/
          state: directory

      - name: CREATE SNMP.CONF FILE
        file:
          path: ./{{ ansible_network_os }}/snmp.conf
          state: touch 
            
```

##### Step 8

Save and execute the playbook. 

You should see the following output. 

```commandline

ntc@jump-host:ansible$ ansible-playbook -i inventory auto-create.yml

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
ntc@jump-host:ansible$ tree
.
├── auto-create.yml
├── eos
│   └── snmp.conf
├── inventory
├── ios
│   └── snmp.conf
├── junos
│   └── snmp.conf
└── nxos
    └── snmp.conf

4 directories, 6 files

```


##### Step 10

We can run the same exercise with `templates` directories and empty `jinja2` files. 

Add two more tasks to create these.

```yaml

---

  - name: Auto Generate Files and Directories
    hosts: all
    connection: local
    gather_facts: no

    tasks:

      - name: CREATE DIRECTORIES BASED ON OS
        file:
          path: ./{{ ansible_network_os }}/
          state: directory

      - name: CREATE SNMP.CONF FILE
        file:
          path: ./{{ ansible_network_os }}/snmp.conf
          state: touch 
          
      - name: CREATE TEMPLATES DIRECTORIES
        file:
          path: ./templates/
          state: directory

      - name: CREATE JINJA2 FILES
        file:
          path: ./templates/{{ ansible_network_os }}-snmp.j2
          state: touch
          
```

##### Step 11


Save and execute the playbook. 

Type the tree command to see the final results. 


```
ntc@jump-host:ansible$ tree
.
├── auto-create.yml
├── eos
│   └── snmp.conf
├── inventory
├── ios
│   └── snmp.conf
├── junos
│   └── snmp.conf
├── nxos
│   └── snmp.conf
└── templates
    ├── eos-snmp.j2
    ├── ios-snmp.j2
    ├── junos-snmp.j2
    └── nxos-snmp.j2

5 directories, 10 files

```