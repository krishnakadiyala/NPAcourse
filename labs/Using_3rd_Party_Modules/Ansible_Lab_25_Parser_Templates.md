## Lab 25 - Using Parser Templates


In this lab we are going to use different modules to collect data, reuse it and also parse unstructured data that comes back from the operational command. The main important modules we are going to be using are `snmp_device_version`, `ntc_show_command`, `command_parser` and `textfsm_parser`. 



##### Step 1

Create a playbook file called `parsers.yml` Inside the playbook add the following play definition and vars to define template path. Feel free to look inside the template path to view all the exisiting templates and how they are built.

>Note: Later in this lab we are going to use a role called network-engine so for now it's been added to the play definition so Ansible can find the roles we've installed.

```yaml

---

  - name: USING PARSER TEMPLATES
    hosts: csr1
    connection: network_cli
    gather_facts: no
    roles:
      - ansible-network.network-engine

    vars:
      template_path: "/etc/ntc/ansible/library/ntc-ansible/ntc-templates/templates/"
      show_version_path: "{{ template_path }}cisco_ios_show_version.template"

    tasks:
```




##### Step 2

Add two more tasks, one with the `ntc_show_command` and the other with a `debug` statement to view the parsed data.
The `ntc_show_command` module is a multi-vendor Ansible module designed for converting raw text into JSON key/value pairs. 

This module leverages TextFSM as the templating tool to parse the unstructured data. Netmiko is also used for transport to enalbe support for all devices. 


```yaml

      - name: Using ntc_show_command and txt_fsm
        ntc_show_command:
          connection: ssh
          platform: "{{ ntc_vendor }}_{{ ansible_network_os }}"
          command: 'show version'
          provider: "{{ connection_details }}"
          template_dir: "{{ template_path }}"
        register: ntc_version_data

      - name: View ntc_show_version data
        debug:
          var: ntc_version_data
```

>Note: `conection_details` variable should be coming from `group_vars/all.yml` if it's not there add:

```yaml
connection_details:
  username: "{{ ansible_user }}"
  password: "{{ ansible_ssh_pass }}"
  host: "{{ inventory_hostname }}"
```

##### Step 3

Save the playbook and execute it. You should see the following output:

```commandline

....output omitted

TASK [Using ntc_show_command and txt_fsm] *************************************************
ok: [csr1]

TASK [View ntc_show_version data] *************************************************************
ok: [csr1] => {
    "ntc_version_data": {
        "changed": false,
        "failed": false,
        "response": [
            {
                "config_register": "0x2102",
                "hardware": [
                    "CSR1000V"
                ],
                "hostname": "csr1",
                "mac": [],
                "reload_reason": "reload",
                "rommon": "IOS-XE",
                "running_image": "packages.conf",
                "serial": [
                    "9KIBQAQ3OPE"
                ],
                "uptime": "32 minutes",
                "version": "16.08.01a"
            }
        ],
        "response_list": []
    }
}

PLAY RECAP *************************************************************************************
csr1                       : ok=4    changed=0    unreachable=0    failed=0

```

>Note: We sent the command and also parsed the data with a single task.


##### Step 4

Create two new directories locally called `parsers` and `ios` as a subdirectory of `parsers` add a new file called `show_version.yml`. Inside `ios` and add this template.

```yaml

---
- name: parser meta data
  parser_metadata:
    version: 1.0
    command: show version
    network_os: ios

- name: match version
  pattern_match:
    regex: "Version (\\S+),"
  register: version

- name: match model
  pattern_match:
    regex: "cisco\\s(\\w+)\\s\\(\\w+\\)"
  register: model

- name: match image
  pattern_match:
    regex: "^System image file is (\\S+)"
  register: image

- name: match uptime
  pattern_match:
    regex: "uptime is (.+)"
  register: uptime

- name: match total memory
  pattern_match:
    regex: "with (\\S+)/(\\w*) bytes of memory"
  register: total_mem

- name: match free memory
  pattern_match:
    regex: "with \\w*/(\\S+) bytes of memory"
  register: free_mem

- name: export system facts to playbook
  set_vars:
    model: "{{ model.matches.0 }}"
    image_file: "{{ image.matches.0 }}"
    uptime: "{{ uptime.matches.0 }}"
    version: "{{ version.matches.0 }}"
    memory:
      total: "{{ total_mem.matches.0 }}"
      free: "{{ free_mem.matches.0 }}"
  export: yes
  register: system_facts
```

>Note: This template uses YAML syntax and regex to find the specified data from the rutured data from the show command. 

##### Step 5

Add three new tasks to your playbook. 

The first one will just be using the `ios_command` module so we can send a cli command to the device and return unstructured data.

The second task for `command_parser` is a module from the `network-engine` roles. This role is available through Ansible galaxy. The module we are using enables the user to parse the output of show commands that will come back from the previous task. 

The third task will be a `debug` module that will show the parsed data performed by the `command_parser`

>Note: On the previous task we used `ntc_show_command` that uses textfsm to parse the data. This time we are using a different type of parser which uses YAML syntax rather than what textfsm uses. Look inside the file which is indicated in the path of the `file` parameter to see the differences. 

```yaml
      - name: SHOW VERSION
        ios_command:
          commands: show version
        register: version_data

      - name: Generate JSON data structure usin command_parser
        command_parser:
          file: "./parsers/{{ ansible_network_os }}/show_version.yml"
          content: "{{ version_data['stdout'][0] }}"
        register: command_parser

      - name: View command_parsed data
        debug: 
          var: command_parser
```
##### Step 6

Save the playbook and execute it. You should see the following output:


```commandline
...output omitted

TASK [SHOW VERSION] *******************************************************************
ok: [csr1]

TASK [Generate JSON data structure usin command_parser] *************************************
ok: [csr1]

TASK [View command_parsed data] **************************************************
ok: [csr1] => {
    "command_parser": {
        "ansible_facts": {
            "system_facts": {
                "image_file": "\"bootflash:packages.conf\"",
                "memory": {
                    "free": "3075K",
                    "total": "2190795K"
                },
                "model": "CSR1000V",
                "uptime": "44 minutes",
                "version": "16.08.01a"
            }
        },
        "changed": false,
        "failed": false,
        "included": [
            "./parsers/ios/show_version.yml"
        ]
    }
}

PLAY RECAP *******************************************************************
csr1                       : ok=7    changed=0    unreachable=0    failed=0

```

##### Step 7

Add two more tasks to the playbook. This time we are using a different module called `textfsm_parser` from the network-engine. 

For this module we can reuse the same template that we used for the `ntc_show_command` module since it parses data with textfsm. The second task is the `debug` module which will allow us to view the parsed data.

```yaml
      - name: Generate JSON data structure usin textfsm_parser
        textfsm_parser:
          file: "{{ show_version_path }}"
          content: "{{ version_data['stdout'][0] }}"
          name: system_facts
        register: txt_fsm 

      - name: using textfsm_parser
        debug:
          var: txt_fsm
```

##### Step 8

Save the playbook and execute it. You should see the following output:

```commandline

...output omitted

TASK [Generate JSON data structure usin textfsm_parser] *********************************************
ok: [csr1]

TASK [using textfsm_parser] *************************************************************************
ok: [csr1] => {
    "txt_fsm": {
        "ansible_facts": {
            "system_facts": [
                {
                    "CONFIG_REGISTER": "0x2102",
                    "HARDWARE": [
                        "CSR1000V"
                    ],
                    "HOSTNAME": "csr1",
                    "MAC": [],
                    "RELOAD_REASON": "reload",
                    "ROMMON": "IOS-XE",
                    "RUNNING_IMAGE": "packages.conf",
                    "SERIAL": [
                        "9KIBQAQ3OPE"
                    ],
                    "UPTIME": "46 minutes",
                    "VERSION": "16.08.01a"
                }
            ]
        },
        "changed": false,
        "failed": false
    }
}

PLAY RECAP ************************************************************************************************
csr1                       : ok=9    changed=0    unreachable=0    failed=0

```


##### Step 9

Add this last task using the `debug` module that will show the data from `snmp_device_version` and the device version from all the parsers that we just used.

```yaml
      - name: Display Version data from the different parsers
        debug:
          msg: "The version for this {{ ansible_device_vendor }} {{ ansible_device_os }} device is {{ item }}"
        loop: 
           - "{{ ntc_version_data['response'][0]['version'] }} using ntc_show_command" 
           - "{{ command_parser['ansible_facts']['system_facts']['version'] }} using network engine command_parser"
           - "{{ txt_fsm['ansible_facts']['system_facts'][0]['VERSION'] }} using network engine textfsm_parser"
```

##### Step 10

Save the playbook and execute it. You should see the following output:

```commandline
...output omitted

TASK [Display Version data from the different parsers] ************************************************************
ok: [csr1] => (item=16.08.01a using ntc_show_command) => {
    "msg": "The version for this cisco ios device is 16.08.01a using ntc_show_command"
}
ok: [csr1] => (item=16.08.01a using network engine command_parser) => {
    "msg": "The version for this cisco ios device is 16.08.01a using network engine command_parser"
}
ok: [csr1] => (item=16.08.01a using network engine textfsm_parser) => {
    "msg": "The version for this cisco ios device is 16.08.01a using network engine textfsm_parser"
}

PLAY RECAP ********************************************************************************************************
csr1                       : ok=8   changed=0    unreachable=0    failed=0

```

