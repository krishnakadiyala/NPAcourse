# Lab 10 - Getting started with the cli_command Module

### Task 1 - Using the cli_command module

In this task, you will use the `cli_command` module to issue show commands against network devices and save the command outputs to a file.  This is showing exactly what you did in Lab 3, but now for issuing show commands in a single task.

##### Step 1

Create a new playbook called `cli-command.yml` in the `ansible` directory.  You have your choice to automate EOS, or NXOS devices.  While all examples reflect IOS and JUNOS devices, it's the same workflow for any of them.

```yaml

---

  - name: BACKUP SHOW VERSION FOR IOS AND JUNOS
    hosts: all
    connection: network_cli
    gather_facts: no

    tasks:

```

##### Step 2

Add a task to issue the `show version` command.

```yaml

---

  - name: BACKUP SHOW VERSION FOR IOS AND JUNOS
    hosts: all
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

##### Step 4

Execute the playbook using the `-v` verbose flag.

##### Step 5

In order to clean up the output, use `register` task attribute and debug the new variable to the terminal.

This is the same exact process you did in the last lab so it should look very familiar already.

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

Take note of the data being debugged:

```

TASK [VIEW DATA STORED IN CONFIG_DATA] *****************************************************************************************************************************************************
ok: [csr1] => {
    "config_data": {
        "changed": false,
        "failed": false,
        "stdout": "Cisco IOS XE Software, Version 16.08.01a\nCisco IOS Software [Fuji], Virtual XE Software (X86_64_LINUX_IOSD-UNIVERSALK9-M), Version 16.8.1a, RELEASE SOFTWARE (fc1)\nTechnical Support:
         
         output ommited ...
         
         
ok: [vmx1] => {
    "config_data": {
        "changed": false,
        "failed": false,
        "stdout": "Hostname: vmx1\nModel: vmx\nJunos: 18.2R1.9\nJUNOS OS Kernel 64-bit  [20180614.6c3f819_builder_stable_11]\nJUNOS OS libs [20180614.6c3f819_builder_stable_11]\nJUNOS OS runtime [20180614.6c3f819_builder_stable_11]\nJUNOS
        
        output ommited ...
```

`config_data` is a JSON object (think dictionary) that has several key value pairs, e.g. `changed`, `failed`, `stdout`, and `stdout_lines` (not shown).

You can also see that `stdout` is a dictionary key given it has a value after the key.  

`stdout` is **ALWAYS** a dictionary when you're using the "cli_command" modules.  Notice the difference from the previous lab using the `core_command` module which returns a list.

##### Step 7

Add the required task(s) to save the output from the "show interfaces" command to a file using the `copy` module just like you did in the last lab.

