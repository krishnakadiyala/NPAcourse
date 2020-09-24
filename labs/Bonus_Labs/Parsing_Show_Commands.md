# Parsing Show Commands with Ansible

In the next few labs, we'll introduce a few different methodologies for parsing show commands with Ansible looking at several different built-in Jinja2 filters.  They are `regex_search`, `regex_findall` and `parse_cli_textfsm`.


### Task 1 - Using the `parse_cli_textfsm` Filter

In the first task, we'll parse show data on IOS using a pre-built TextFSM template for the "show version" and "show interfaces"command called `parse_cli_textfsm`. A benefit of using the TextFSM filter and associated templates as opposed to other options is that Network to Code has developed a robust list of parsing templates which render all major vendors and all major show commands into structured data. 
The only remaining effort for you is to map the template to the associated show command. Other 3rd party modules will do this for you, but
using Ansible Core `ios_command` and the `parse_cli_textfsm` filter requires you to tell Ansible which parsing template to use. 

This really provides auto-magic parsing against output for legacy devices which do not have an API giving output with data in a data structure. 

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
      show_version_path: "{{ template_path }}cisco_ios_show_version.textfsm"
      show_interface_path: "{{ template_path }}cisco_ios_show_interfaces.textfsm"

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

  * One that will _parse_ the "show version" and "show interfaces" response using the pre-built TextFSM template and save them as new variables using the `set_fact` module.
  * One that will debug the new variables.

```yaml
      - name: PARSE CLI TextFSM SHOW INTERFACE
        set_fact:
          show_version: "{{ config_data.stdout[0] | parse_cli_textfsm(show_version_path) }}"
          show_interface: "{{ config_data.stdout[1] | parse_cli_textfsm(show_interface_path) }}"

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

ntc@ntc-training:ansible$ ansible-playbook -i inventory parse-ios.yml

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

This is incredibly useful data now that it is provided with a list of dictionaries, rather just a big string with no structure to look up a particular piece of data. 

### Task 2 - Using the `regex_` Filters

Instead of using TextFSM templates to automatically parse the raw output into a list of dictionaries, you can also use Jinja Filters which search through the `show` commmand output for particular patterns. This approach requires more effort, but can be useful if you are looking for a specific piece of information in the output and there is no TextFSM template available for your command output to use. 

##### Step 1

Since we already have the `show` command output stored in the `config_data` variable, we can reference the first command output (`show version`) by looking up list index `[0]` of `config_data` and then applying a Jinja Filter to search in that text for a particular pattern using Python regular expression syntax. 

In order to find the version information in the `show version` output, we need to define a regular expression pattern to match our expected output. The expected output of an IOS version output is three sets of one to two integers, separated by a period `.`, with a potential of having letters at the end, such as `16.08.01a`. You can use regular expression helper websites to build out the pattern matching, such as [RegEx101](https://regex101.com/). In this lab, the pattern is provided for you, but feel free to explore that site with the raw `show version` output in the bottom and a pattern in the top field. 

First we will add a task using `set_fact` to transform the `config_data` variable combined with some key and index lookups along with a Jinja filter into a new variable. 
  
The `regex_search` filter will allow us to find the specified string applied on the regular expression pattern we have defined to search for the IOS Version string. `regex_search` will return empty if it cannot find the pattern. In our task, we want the new variable `show_version_search` to have the IOS version taken out of the big string of command output. We will then debug print out the output of the new fact. 

Add the following tasks to your playbook:

```yaml

      - name: PARSING WITH REGEX_SEARCH
        set_fact:
          show_version_search: "{{ config_data.stdout[0] | regex_search('(\\d+\\.\\S+)') }}"
          
      - name: DISPLAY REGEX_SEARCH FOR IOS VERSION
        debug:
          msg: "The device version is {{ show_version_search }}"
```

Save and execute the playbook.

##### Step 2

Looking at the relevant debug output, you should see the following:

```commandline

.......Output omitted
TASK [PARSING WITH REGEX_SEARCH] *********************************************************************************************************
ok: [csr1]

TASK [DISPLAY REGEX_SEARCH FOR IOS VERSION] **********************************************************************************************
ok: [csr1] => {
    "msg": "The device version is 16.08.01a"
}

PLAY RECAP *******************************************************************************************************************************
csr1                       : ok=3    changed=0    unreachable=0    failed=0

.......Output omitted
```

##### Step 3 
Rather than finding one specific string in an output, we may want to find multiple strings according to a regex pattern. For example, when we have the `show interface` output, we may want to find the names of all the interfaces present. 

The `regex_search` filter allows us to find all matches of a particular pattern. Now applying this filter against the previous show command output of `show interfaces` allows us to find all interface names, assuming we have a regular expression pattern which matches the interface names we are expecting. Once we have all the interface names we will debug print that list element by element using a `loop` to the screen with a simple message. 

Add the following tasks to your playbook:
```yaml

      - name: PARSING WITH REGEX_FINDALL
        set_fact:
          show_interface_find_all: "{{ config_data.stdout[1] | regex_findall('Gig\\w+|Loopback\\w+') }}"
          
      - name: DISPLAY REGEX_FINDALL
        debug:
          msg: " An interface on this device is {{ item }}"
        loop: "{{ show_interface_find_all }}"
```

Save and execute the playbook.

##### Step 4

Looking at the relevant debug output, you should see the following:

```commandline
.......Output omitted
TASK [PARSING WITH REGEX_FINDALL] ********************************************************************************************************
ok: [csr1]

TASK [DISPLAY REGEX_FINDALL] *************************************************************************************************************
ok: [csr1] => (item=GigabitEthernet1) => {
    "msg": " An interface on this device is GigabitEthernet1"
}
ok: [csr1] => (item=GigabitEthernet2) => {
    "msg": " An interface on this device is GigabitEthernet2"
}
ok: [csr1] => (item=GigabitEthernet3) => {
    "msg": " An interface on this device is GigabitEthernet3"
}
ok: [csr1] => (item=GigabitEthernet4) => {
    "msg": " An interface on this device is GigabitEthernet4"
}
ok: [csr1] => (item=GigabitEthernet5) => {
    "msg": " An interface on this device is GigabitEthernet5"
}
ok: [csr1] => (item=GigabitEthernet6) => {
    "msg": " An interface on this device is GigabitEthernet6"
}
ok: [csr1] => (item=GigabitEthernet7) => {
    "msg": " An interface on this device is GigabitEthernet7"
}
ok: [csr1] => (item=GigabitEthernet8) => {
    "msg": " An interface on this device is GigabitEthernet8"
}
ok: [csr1] => (item=GigabitEthernet9) => {
    "msg": " An interface on this device is GigabitEthernet9"
}
ok: [csr1] => (item=GigabitEthernet10) => {
    "msg": " An interface on this device is GigabitEthernet10"
}
ok: [csr1] => (item=GigabitEthernet11) => {
    "msg": " An interface on this device is GigabitEthernet11"
}
ok: [csr1] => (item=GigabitEthernet12) => {
    "msg": " An interface on this device is GigabitEthernet12"
}
ok: [csr1] => (item=GigabitEthernet13) => {
    "msg": " An interface on this device is GigabitEthernet13"
}
ok: [csr1] => (item=GigabitEthernet14) => {
    "msg": " An interface on this device is GigabitEthernet14"
}
ok: [csr1] => (item=GigabitEthernet15) => {
    "msg": " An interface on this device is GigabitEthernet15"
}
ok: [csr1] => (item=GigabitEthernet16) => {
    "msg": " An interface on this device is GigabitEthernet16"
}
ok: [csr1] => (item=GigabitEthernet17) => {
    "msg": " An interface on this device is GigabitEthernet17"
}
ok: [csr1] => (item=GigabitEthernet18) => {
    "msg": " An interface on this device is GigabitEthernet18"
}
ok: [csr1] => (item=GigabitEthernet19) => {
    "msg": " An interface on this device is GigabitEthernet19"
}
ok: [csr1] => (item=GigabitEthernet20) => {
    "msg": " An interface on this device is GigabitEthernet20"
}
ok: [csr1] => (item=GigabitEthernet21) => {
    "msg": " An interface on this device is GigabitEthernet21"
}
ok: [csr1] => (item=GigabitEthernet22) => {
    "msg": " An interface on this device is GigabitEthernet22"
}
ok: [csr1] => (item=GigabitEthernet23) => {
    "msg": " An interface on this device is GigabitEthernet23"
}
ok: [csr1] => (item=GigabitEthernet24) => {
    "msg": " An interface on this device is GigabitEthernet24"
}
ok: [csr1] => (item=GigabitEthernet25) => {
    "msg": " An interface on this device is GigabitEthernet25"
}
ok: [csr1] => (item=GigabitEthernet26) => {
    "msg": " An interface on this device is GigabitEthernet26"
}
ok: [csr1] => (item=Loopback200) => {
    "msg": " An interface on this device is Loopback200"
}
ok: [csr1] => (item=Loopback222) => {
    "msg": " An interface on this device is Loopback222"
}

PLAY RECAP *******************************************************************************************************************************
csr1                       : ok=5    changed=0    unreachable=0    failed=0


```


The full playbook should look like the following: 


```yaml

---

  - name: PING TEST
    hosts: csr1
    connection: network_cli
    gather_facts: no

    vars:
      template_path: "/etc/ntc/ansible/library/ntc-ansible/ntc-templates/templates/"
      show_version_path: "{{ template_path }}cisco_ios_show_version.textfsm"
      show_interface_path: "{{ template_path }}cisco_ios_show_interfaces.textfsm"

    tasks:

      - name: GET SHOW COMMANDS
        ios_command:
          commands: 
            - show version
            - show interfaces
        register: config_data

      - name: PARSE CLI TXFSM SHOW INTERFACE
        set_fact:
          show_version: "{{ config_data.stdout[0] | parse_cli_textfsm(show_version_path) }}"
          show_interface: "{{ config_data.stdout[1] | parse_cli_textfsm(show_interface_path) }}"

      - name: DISPLAY PARSED DATA
        debug:
          var: "{{ item }}"
        loop: 
          - show_version
          - show_interface

      - name: PARSING WITH REGEX_SEARCH
        set_fact:
          show_version_search: "{{ config_data.stdout[0] | regex_search('(\\d+\\.\\S+)') }}"
          
      - name: DISPLAY REGEX_SEARCH FOR IOS VERSION
        debug:
          msg: "The device version is {{ show_version_search }}"

      - name: PARSING WITH REGEX_FINDALL
        set_fact:
          show_interface_find_all: "{{ config_data.stdout[1] | regex_findall('Gig\\w+|Loopback\\w+') }}"
          
      - name: DISPLAY REGEX_FINDALL
        debug:
          msg: "An interface on this device is {{ item }}"
        loop: "{{ show_interface_find_all }}"
```

