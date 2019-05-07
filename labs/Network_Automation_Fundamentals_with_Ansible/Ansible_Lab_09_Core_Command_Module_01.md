## Lab 9 - Using the Core Command Module

### Task 1 - Using the *_command module

In this task, you will use the _command module to issue show commands against network devices and save the command outputs to a file.

##### Step 1

Create a new playbook called `core-command.yml` in the `ansible` directory.  You have your choice to automate EOS, or NXOS devices.  While all examples reflect IOS and JUNOS devices, it's the same workflow for any of them.


```yaml

---

  - name: BACKUP SHOW VERSION FOR IOS
    hosts: csr1
    connection: network_cli
    gather_facts: no

    tasks:

```

##### Step 2

Add a task to issue the `show version` command.

```yaml

---

  - name: BACKUP SHOW VERSION FOR IOS
    hosts: csr1
    connection: network_cli
    gather_facts: no

    tasks:
      - name: GET SHOW COMMANDS
        ios_command:
          commands: show version

```

##### Step 3

Execute the playbook.

Did you see the output anywhere?

##### Step 4

Execute the playbook using the `-v` verbose flag.

Did you see the output anywhere?

##### Step 5

In order to clean up the output, use `register` task attribute and debug the new variable to the terminal.

```yaml
      - name: GET SHOW COMMANDS
        ios_command:
          commands: show version
        register: config_data

      - name: VIEW DATA STORED IN CONFIG_DATA
        debug:
          var: config_data
```

##### Step 6

Execute the playbook.  Do not use the `-v` flag.

The output seen is much cleaner and easier to read than using the `-v` flag.

> Note that when you use `register`, it's creating a new variable and storing the JSON return data from the module into the variable name defined.  In this case, it's `config_data`.

##### Step 7

Take note of the data being debugged:

```

TASK [VIEW DATA STORED IN CONFIG_DATA] ********************************************************
ok: [csr1] => {
    "config_data": {
        "changed": false,
        "failed": false,
        "stdout": [
            "Cisco IOS XE Software, Version 16.08.01a\nCisco IOS Software [Fuji], Virtual XE Software (X86_64_LINUX_IOSD-UNIVERSALK9-M), Version 16.8.1a, RELEASE SOFTWARE (fc1)\nTechnical Support:
            ...
```

`config_data` is a JSON object (think dictionary) that has several key value pairs, e.g. `changed`, `failed`, `stdout`, and `stdout_lines` (not shown).

You can also see that `stdout` is a list given it has square brackets next to it.  

`stdout` is **ALWAYS** a list when you're using the "command" modules.  It is a list of show command responses.  It's a list that has a length equal to the number of commands sent to the device.  In this case, we sent 1 command, so it's a length of 1, thus we'd access the "show version" response as element 0.

##### Step 8

Our goal is to save the show command output to a file.  We are going to do this using the `template` module.

Create a new Jinja2 template called `basic-copy.j2` stored in the `templates` directory.  

It should look like this:

```
{{ config_data['stdout'][0] }}
```

Take a second to think about this object.  Remember the data type of `stdout`?

##### Step 9

Add a task to create a directory using the *file* module where we can store the command outputs.  

We'll use `command-outputs`.

```yaml
      - name: GENERATE DIRECTORIES
        file:
          path: ./command-outputs/{{ ansible_network_os }}/
           state: directory
```

##### Step 10

Add the required task using `template` to the playbook.

```yaml
      - name: SAVE SH VERSION TO FILE
        template:
          src: basic-copy.j2
          dest: ./command-outputs/{{ ansible_network_os }}/show_version.txt
```

##### Step 11

Execute the playbook.

##### Step 12

Make the required changes to save command output for all 3 CSR devices.

(1) Change `hosts: csr1` to `hosts: iosxe`


(2) Add a variable to the `dest` filename in the `template` module task:

```yaml

dest: ./command-outputs/{{ ansible_network_os }}/{{ inventory_hostname}}-show_version.txt
```

##### Check

Full and final playbook will look like this:

```yaml

---

  - name: BACKUP SHOW VERSION ON IOS
    hosts: iosxe
    connection: network_cli
    gather_facts: no

    tasks:
      - name: GET SHOW COMMANDS
        ios_command:
          commands: show version
        register: config_data

      - name: VIEW DATA STORED IN CONFIG_DATA
        debug:
          var: config_data

      - name: GENERATE DIRECTORIES
        file:
          path: ./command-outputs/{{ ansible_network_os }}/
          state: directory

      - name: SAVE SH VERSION TO FILE
        template:
          src: basic-copy.j2
          dest: ./command-outputs/{{ ansible_network_os }}/{{ inventory_hostname}}-show_version.txt
          
```
Save and execute the playbook

##### Step 13 

Lets try the same thing but with JUNOS. Add another play below the first one.

```yaml

---

  - name: BACKUP SHOW VERSION FOR JUNOS
    hosts: vmx1
    connection: netconf
    gather_facts: no

    tasks:

```

##### Step 14

Add a task to issue the `show version` command.

```yaml

---

  - name: BACKUP SHOW VERSION FOR JUNOS
    hosts: vmx1
    connection: netconf
    gather_facts: no

    tasks:
      - name: GET SHOW COMMANDS
        junos_command:
          commands: show version

```

##### Step 15

Execute the playbook.

Did you see the output anywhere?

##### Step 16

Execute the playbook using the `-v` verbose flag.

Did you see the output anywhere?

##### Step 17

In order to clean up the output, use `register` task attribute and debug the new variable to the terminal.

```yaml
      - name: GET SHOW COMMANDS
        junos_command:
          commands: show version
        register: config_data

      - name: VIEW DATA STORED IN CONFIG_DATA
        debug:
          var: config_data
```

##### Step 18

Execute the playbook.  Do not use the `-v` flag.

The output seen is much cleaner and easier to read than using the `-v` flag.

> Note that when you use `register`, it's creating a new variable and storing the JSON return data from the module into the variable name defined.  In this case, it's `config_data`.

##### Step 19

Take note of the data being debugged:

```
TASK [VIEW DATA STORED IN CONFIG_DATA] ********************************************************
ok: [vmx1] => {
    "config_data": {
        "changed": false,
        "failed": false,
        "stdout": [
            "Hostname: vmx1\nModel: vmx\nJunos: 18.2R1.9\nJUNOS OS Kernel 64-bit  [20180614.6c3f819_builder_stable_11]\nJUNOS OS libs [20180614.6c3f819_builder_stable_11]\nJUNOS OS runtime [20180614.6c3f819_builder_stable_11]\nJUNOS OS time zone information
        .....
```

`config_data` is a JSON object (think dictionary) that has several key value pairs, e.g. `changed`, `failed`, `stdout`, and `stdout_lines` (not shown).

You can also see that `stdout` is a list given it has square brackets next to it.  

`stdout` is **ALWAYS** a list when you're using the "command" modules.  It is a list of show command responses.  It's a list that has a length equal to the number of commands sent to the device.  In this case, we sent 1 command, so it's a length of 1, thus we'd access the "show version" response as element 0.

##### Step 20

Our goal is to save the show command output to a file.  We are going to do this using the `template` module.

Create a new Jinja2 template called `basic-copy.j2` stored in the `templates` directory.  

It should look like this:

```
{{ config_data['stdout'][0] }}
```

Take a second to think about this object.  Remember the data type of `stdout`?

##### Step 21

Add a task to create a directory using the *file* module where we can store the command outputs.  

We'll use `command-outputs`.

```yaml
      - name: GENERATE DIRECTORIES
        file:
          path: ./command-outputs/{{ ansible_network_os }}/
          state: directory
```

##### Step 22

Add the required task using `template` to the playbook.

```yaml
      - name: SAVE SH VERSION TO FILE
        template:
          src: basic-copy.j2
          dest: ./command-outputs/{{ ansible_network_os }}/show_version.txt
```

##### Step 23

Execute the playbook.

##### Step 24

Make the required changes to save command output for all 3 VMX devices.

(1) Change `hosts: vmx1` to `hosts: vmx`


(2) Add a variable to the `dest` filename in the `template` module task:

```yaml

dest: ./command-outputs/{{ ansible_network_os }}/{{ inventory_hostname}}-show_version.txt
```

##### Check

Full and final playbook will look like this:

```yaml

---

  - name: BACKUP SHOW VERSION ON IOS
    hosts: iosxe
    connection: network_cli
    gather_facts: no

    tasks:
      - name: GET SHOW COMMANDS
        ios_command:
          commands: show version
        register: config_data

      - name: VIEW DATA STORED IN CONFIG_DATA
        debug:
          var: config_data

      - name: GENERATE DIRECTORIES
        file:
          path: ./command-outputs/{{ ansible_network_os }}/
          state: directory

      - name: SAVE SH VERSION TO FILE
        template:
          src: basic-copy.j2
          dest: ./command-outputs/{{ ansible_network_os }}/{{ inventory_hostname}}-show_version.txt
          

  - name: BACKUP SHOW VERSION ON JUNOS
    hosts: vmx
    connection: netconf
    gather_facts: no

    tasks:
      - name: GET SHOW COMMANDS
        junos_command:
          commands: show version
        register: config_data

      - name: VIEW DATA STORED IN CONFIG_DATA
        debug:
          var: config_data

      - name: GENERATE DIRECTORIES
        file:
          path: ./command-outputs/{{ ansible_network_os }}/
          state: directory

      - name: SAVE SH VERSION TO FILE
        template:
          src: basic-copy.j2
          dest: ./command-outputs/{{ ansible_network_os }}/{{ inventory_hostname}}-show_version.txt        
```

Save and execute the playbook