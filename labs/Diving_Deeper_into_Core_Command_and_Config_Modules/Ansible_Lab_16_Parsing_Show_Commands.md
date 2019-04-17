## Lab 16 - Parsing Show Commands with Ansible

In the next few labs, we'll introduce a few different methodologies for parsing show commands with Ansible looking at several different built-in Jinja2 filters.  They are `regex_search`, `regex_findall` and `parse_cli_textfsm`.


### Task 1

In the first task, we'll parse show data on IOS using a pre-built TextFSM template for the "show version" and "show interfaces"command called `parse_cli_textfsm`.

##### Step 1

Create a new playbook called `parse-ios.yml` in the `ansible` directory.

Use the following playbook to gather `show version` and `show interfaces` for the IOS devices.

```yaml

---

  - name: PARSING SHOW COMMANDS
    hosts: csr1
    connection: network_cli
    gather_facts: no

    vars:
      template_path: "/etc/ntc/ansible/library/ntc-ansible/ntc-templates/templates/"
      show_version_path: "{{ template_path }}cisco_ios_show_version.template"
      show_interface_path: "{{ template_path }}cisco_ios_show_interfaces.template"

    tasks:

      - name: GET SHOW COMMANDS
        ios_command:
          commands: 
            - show version
            - show interfaces
        register: config_data


```

> Note: we've also defined three variables to know the path and file that should be used for the parsing.

Feel free to open the TextFSM templates so you can review it.

##### Step 2

Add two new tasks:

  * One that will _parse_ the "show version" and "show interfaces" response using the pre-built TextFSM template and save them as a new variables using the `set_fact` module.
  * One that will debug the new variables.

```yaml
      - name: PARSE CLI TXFSM SHOW INTERFACE
        set_fact:
          show_version: "{{ config_data.stdout.0 | parse_cli_textfsm(show_version_path) }}"
          show_interface: "{{ config_data.stdout.1 | parse_cli_textfsm(show_interface_path) }}"

      - name: DISPLAY PARSED DATA
        debug:
          var: "{{ item }}"
        loop: 
          - show_interface
          - show_version
```

##### Step 3

Execute the playbook.

Looking at the relevant debug output, you should see the following:

```

ntc@jump-host:ansible$ ansible-playbook -i inventory parse-ios.yml

.......Output omitted

TASK [DISPLAY PARSED DATA] ******************************************************************
ok: [csr1] => (item=show_version) => {
    "item": "show_version",
    "show_version": [
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
            "UPTIME": "23 minutes",
            "VERSION": "16.08.01a"
        }
    ]
}
ok: [csr1] => (item=show_interface) => {
    "item": "show_interface",
    "show_interface": [
        {
            "ADDRESS": "2cc2.6031.1341",
            "BANDWIDTH": "1000000 Kbit",
            "BIA": "2cc2.6031.1341",
            "DELAY": "10 usec",
            "DESCRIPTION": "",
            "DUPLEX": "Full Duplex",
            "ENCAPSULATION": "ARPA",
            "HARDWARE_TYPE": "CSR vNIC",
            "INPUT_ERRORS": "0",
            "INPUT_PACKETS": "2206",
            "INPUT_RATE": "1000",
            "INTERFACE": "GigabitEthernet1",
            "IP_ADDRESS": "10.0.0.51/24",
            "LAST_INPUT": "00:00:24",
            "LAST_OUTPUT": "00:00:12",
            "LAST_OUTPUT_HANG": "never",
            "LINK_STATUS": "up",
            "MTU": "1500",
            "OUTPUT_ERRORS": "0",
            "OUTPUT_PACKETS": "2324",
            "OUTPUT_RATE": "1000",
            "PROTOCOL_STATUS": "up",
            "QUEUE_STRATEGY": "fifo",
            "SPEED": "1000Mbps"
        },
        {
            "ADDRESS": "2cc2.6069.e08c",
            "BANDWIDTH": "1000000 Kbit",
            "BIA": "2cc2.6069.e08c",
            "DELAY": "10 usec",
            "DESCRIPTION": "",
            "DUPLEX": "Full Duplex",
            "ENCAPSULATION": "ARPA",
            "HARDWARE_TYPE": "CSR vNIC",
            "INPUT_ERRORS": "0",
            "INPUT_PACKETS": "0",
            "INPUT_RATE": "0",
            "INTERFACE": "GigabitEthernet2",
            "IP_ADDRESS": "",
            "LAST_INPUT": "never",
            "LAST_OUTPUT": "00:00:11",
            "LAST_OUTPUT_HANG": "never",
            "LINK_STATUS": "up",
            "MTU": "1500",
            "OUTPUT_ERRORS": "0",
            "OUTPUT_PACKETS": "46",
            "OUTPUT_RATE": "0",
            "PROTOCOL_STATUS": "up",
            "QUEUE_STRATEGY": "fifo",
            "SPEED": "1000Mbps"
        },
        .......Output omitted
```



##### Step 5

Add two new tasks:

  * One that will _parse_ the "show version" using the `regex_search` and "show interfaces" using the `regex_findall` jinja2 filters.
  * One that will debug the new variables.
  
  The `regex_search` will allow us to find the specified string applied on the regular expression and `regex_findall` will do the same but return as a list. 

```yaml

      - name: PARSING WITH REGEX_SEARCH AND REGEX_FINDALL
        set_fact:
          show_version_search: "{{ config_data.stdout.0 | regex_search('(\\d+\\.\\S+)') }}"
          show_interface_find_all: "{{ config_data.stdout.1 | regex_findall('G\\w+|Loopback\\w+') }}"
          
      - name: DISPLAY REGEX_SEARCH AND REGEX_FINDALL
        debug:
          msg: "{{ item }}"
        loop:
          - "The device version is {{ show_version_search }}"
          - "{{ show_interface_find_all }}"
```

Save and execute the playbook.

##### Step 6

Looking at the relevant debug output, you should see the following:

```commandline

.......Output omitted

TASK [PARSING WITH REGEX_SEARCH AND REGEX_FINDALL] ************************************************************
ok: [csr1]

TASK [DISPLAY REGEX_SEARCH AND REGEX_FINDALL] *****************************************************************
ok: [csr1] => (item=The device version is 16.08.01a) => {
    "msg": "The device version is 16.08.01a"
}
ok: [csr1] => (item=[u'GigabitEthernet1', u'GigabitEthernet2', u'GigabitEthernet3', u'GigabitEthernet4', u'Loopback0', u'Loopback200']) => {
    "msg": [
        "GigabitEthernet1",
        "GigabitEthernet2",
        "GigabitEthernet3",
        "GigabitEthernet4",
        "Loopback0",
        "Loopback200"
    ]
}

.......Output omitted
```

##### CHECK


The full playbook should look like the following: 


```yaml

---

  - name: PING TEST
    hosts: csr1
    connection: network_cli
    gather_facts: no

    vars:
      template_path: "/etc/ntc/ansible/library/ntc-ansible/ntc-templates/templates/"
      show_version_path: "{{ template_path }}cisco_ios_show_version.template"
      show_interface_path: "{{ template_path }}cisco_ios_show_interfaces.template"

    tasks:

      - name: GET SHOW COMMANDS
        ios_command:
          commands: 
            - show version
            - show interfaces
        register: config_data

      - name: PARSE CLI TXFSM SHOW INTERFACE
        set_fact:
          show_version: "{{ config_data.stdout.0 | parse_cli_textfsm(show_version_path) }}"
          show_interface: "{{ config_data.stdout.1 | parse_cli_textfsm(show_interface_path) }}"

      - name: DISPLAY PARSED DATA
        debug:
          var: "{{ item }}"
        loop: 
          - show_version
          - show_interface

      - name: PARSING WITH REGEX_SEARCH AND REGEX_FINDALL
        set_fact:
          show_version_search: "{{ config_data.stdout.0 | regex_search('(\\d+\\.\\S+)') }}"
          show_interface_find_all: "{{ config_data.stdout.1 | regex_findall('G\\w+|Loopback\\w+') }}"
          
      - name: DISPLAY REGEX_SEARCH AND REGEX_FINDALL
        debug:
          msg: "{{ item }}"
        loop:
          - "The device version is {{ show_version_search }}"
          - "{{ show_interface_find_all }}"
```