## Lab 10 - Using the Core Command Module

### Task 1 - Using the cli_command module

In this task, you will use the cli_command module to issue show commands against network devices and save the command outputs to a file.

##### Step 1

Create a new playbook called `cli-command.yml` in the `ansible` directory.  You have your choice to automate EOS, or NXOS devices.  While all examples reflect IOS and JUNOS devices, it's the same workflow for any of them.


```yaml

---

  - name: BACKUP SHOW VERSION FOR IOS
    hosts: csr1,vmx1
    connection: network_cli
    gather_facts: no

    tasks:

```

##### Step 2

Add a task to issue the `show version` command.

```yaml

---

  - name: BACKUP SHOW VERSION ON IOS
    hosts: csr1,vmx1
    connection: network_cli
    gather_facts: no

    tasks:
      - name: GET SHOW COMMANDS
        cli_command:
          command: show version
        register: config_data

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
        cli_command:
          command: show version
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

TASK [VIEW DATA STORED IN CONFIG_DATA] *****************************************************************************************************************************************************
ok: [csr1] => {
    "config_data": {
        "changed": false,
        "failed": false,
        "stdout": "Cisco IOS XE Software, Version 16.08.01a\nCisco IOS Software [Fuji], Virtual XE Software (X86_64_LINUX_IOSD-UNIVERSALK9-M), Version 16.8.1a, RELEASE SOFTWARE (fc1)\nTechnical Support:
         ...
         
         
ok: [vmx1] => {
    "config_data": {
        "changed": false,
        "failed": false,
        "stdout": "Hostname: vmx1\nModel: vmx\nJunos: 18.2R1.9\nJUNOS OS Kernel 64-bit  [20180614.6c3f819_builder_stable_11]\nJUNOS OS libs [20180614.6c3f819_builder_stable_11]\nJUNOS OS runtime [20180614.6c3f819_builder_stable_11]\nJUNOS
        ....
```

`config_data` is a JSON object (think dictionary) that has several key value pairs, e.g. `changed`, `failed`, `stdout`, and `stdout_lines` (not shown).

You can also see that `stdout` is a dictionary key given it has a value after the key.  

`stdout` is **ALWAYS** a dictionary when you're using the "cli_command" modules.  It is a list of show command responses.

##### Step 8

Our goal is to save the show command output to a file.  We are going to do this using the `template` module.

Create a new Jinja2 template called `basic-copy.j2` stored in the `templates` directory.  

It should look like this:

```
{{ config_data['stdout'] }}
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
          dest: ./command-outputs/show_version.txt
```

##### Step 11

Execute the playbook.

##### Step 12

Make the required changes to save command output for all 3 CSR and all 3 VMX devices.

(1) Change `hosts: csr1,vmx1` to `hosts: iosxe,vmx`


(2) Add a variable to the `dest` filename in the `template` module task:

```yaml

dest: ./command-outputs/{{ ansible_network_os }}/{{ inventory_hostname}}-show_version.txt
```

##### Check

Full and final playbook will look like this:

```yaml

---

  - name: BACKUP SHOW VERSION ON IOS
    hosts: iosxe,vmx
    connection: network_cli
    gather_facts: no

    tasks:
      - name: GET SHOW COMMANDS
        cli_command:
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


##### Step 14 **MAYBE ADD AN EXAMPLE THAT WE COULD RUN THROUGH A LIST OF COMMANDS, BUT THAT WOULD INTRODUCE LOOPS EARLY IN THE CLASS**

```yaml

---

  - name: BACKUP SHOW VERSION ON IOS
    hosts: csr1,vmx1
    connection: network_cli
    gather_facts: no

    tasks:
      - name: GET SHOW COMMANDS
        cli_command:
          command: "{{ item }}"
        loop:
            - show version
            - show arp
        register: config_data

      - name: VIEW DATA STORED IN CONFIG_DATA
        debug:
          var: "{{ item }}"
        loop:
            - config_data['results'][0]['stdout']
            - config_data['results'][1]['stdout']

```
