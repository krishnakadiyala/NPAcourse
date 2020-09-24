# Bonus Lab 3 - Generating Reports Using NAPALM to Gather Data

Network Automation, or automation in general, is often equated with configuring devices faster, but as you've seen by now, it offers greater predictability and more deterministic outcomes.

On top of that, it also offers even greater value when it comes to collecting data and reporting.  In these next few tasks, you will use Ansible modules to automate the data collection process and also dynamically generate different types of reports.

### Task 1 - Create directory structure

##### Step 1

Create a playbook called `generate-reports.yml` which will be executed on all `vmx` devices.


Include a `napalm_connection_detail` variable with the data needed to log into the devices as we've been using in the previous labs.


```
---

  - name: GATHER AND STORE FACTS
    hosts: vmx
    connection: local
    gather_facts: no

    vars:
      napalm_connection_detail:
        hostname: '{{ inventory_hostname }}'
        username: '{{ ansible_user }}'
        dev_os: '{{ ansible_network_os }}'
        password: '{{ ansible_ssh_pass }}'

```

##### Step 2

Add a task to create the needed directory structure to store the reports per device.

```
    tasks:

      - name: ENSURE DIRECTORY EXISTS
        file:
          path: ./reports/{{ inventory_hostname }}
          state: directory
```

##### Step 3

Execute the playbook.

```
ntc@ntc-training:ansible$ ansible-playbook -i inventory generate-reports.yml

PLAY [GATHER AND STORE FACTS] **************************************************************************************************************************************************************************************

TASK [ENSURE DIRECTORY EXISTS] *************************************************************************************************************************************************************************************
changed: [vmx2]
changed: [vmx1]
changed: [vmx3]

PLAY RECAP *********************************************************************************************************************************************************************************************************
vmx1                       : ok=1    changed=1    unreachable=0    failed=0
vmx2                       : ok=1    changed=1    unreachable=0    failed=0
vmx3                       : ok=1    changed=1    unreachable=0    failed=0


```

The task ran successfully and the directory structure has been created.

You can use the Linux command `tree` to view the new directories.

```
ntc@ntc-training:ansible$ tree
.
├── filtered-facts.yml
├── generate-reports.yml
├── inventory
├── napalm-facts.yml
├── outputs
│   └── facts.json
├── reports
│   ├── vmx1
│   ├── vmx2
│   └── vmx3
└── templates
    └── facts.j2

6 directories, 6 files
ntc@ntc-training:ansible$
```



### Task 2 - Generate fact reports

##### Step 1

Add a task to get facts from devices using `napalm_get_facts`.

```
      - name: GATHER GENERAL DEVICES FACTS
        napalm_get_facts:
          provider: "{{ napalm_connection_detail }}"
          filter: ['facts']
        register: fact_data
        tags: facts
```

Using the `filter` parameter with just "facts" as the default (the same as not using the `filter` parameter at all).

##### Step 2

Execute the playbook using the `facts` tag.

```
ntc@ntc-training:ansible$ ansible-playbook -i inventory generate-reports.yml --tags=facts

PLAY [GATHER AND STORE FACTS] **************************************************************************************************************************************************************************************

TASK [GATHER GENERAL DEVICES FACTS] ********************************************************************************************************************************************************************************
ok: [vmx1]
ok: [vmx3]
ok: [vmx2]

PLAY RECAP *********************************************************************************************************************************************************************************************************
vmx1                       : ok=1    changed=0    unreachable=0    failed=0
vmx2                       : ok=1    changed=0    unreachable=0    failed=0
vmx3                       : ok=1    changed=0    unreachable=0    failed=0
```

##### Step 3

Add a new task to print (debug) the `fact_data` variable.

```
      - name: PRINT GENERAL FACTS
        debug:
          var: fact_data
        tags: facts  
```

##### Step 4

Re-run the playbook using `facts` tag. This will print out the facts from all 3 devices.

##### Step 5

Update template called `facts.j2` you created in the lab with the following content.

```

Device:  {{ inventory_hostname }}

Hostname:        {{ napalm_hostname }}
FQDN:            {{ napalm_fqdn }}
Model:           {{ napalm_model }}
OS Version:      {{ napalm_os_version }}
Serial Number:   {{ napalm_serial_number }}
Vendor:          {{ napalm_vendor }}


```

Again, any variable within `ansible_facts` can be accessed directly.  This is very important to remember.

##### Step 6

Add a task to create the report file using the above template.

```yaml
---

  - name: GATHER AND STORE FACTS
    hosts: vmx
    connection: local
    gather_facts: no

    vars:
      napalm_connection_detail:
        hostname: '{{ inventory_hostname }}'
        username: '{{ ansible_user }}'
        dev_os: '{{ ansible_network_os }}'
        password: '{{ ansible_ssh_pass }}'

    tasks:

      - name: ENSURE DIRECTORY EXISTS
        file:
          path: ./reports/{{ inventory_hostname }}
          state: directory

      - name: GATHER GENERAL DEVICES FACTS
        napalm_get_facts:
          provider: "{{ napalm_connection_detail }}"
          filter: ['facts']
        register: fact_data
        tags: facts

      - name: PRINT GENERAL FACTS
        debug:
          var: fact_data
        tags: facts  

      - name: GENERATE REPORT FOR GENERAL FACTS
        template:
          src: facts.j2
          dest: ./reports/{{ inventory_hostname }}/01_facts.txt
        tags: facts
```


##### Step 7

Run the playbook with the `facts` tag.


```
ntc@ntc-training:ansible$ ansible-playbook -i inventory generate-reports.yml --tags=facts

```

##### Step 8

Check out the new files.

For example:

```
ntc@ntc-training:ansible$ cat reports/vmx1/01_facts.txt
Device:  vmx1

Hostname:        vmx1
FQDN:            vmx1.ntc.com
Model:           VMX
OS Version:      15.1F4.15
Serial Number:   VMXab
Vendor:          Juniper
ntc@ntc-training:ansible$

```

This created a general device fact text-based report for each.  Let's build on this and now build a LLDP report.


### Task 3 - Generate LLDP reports

##### Step 1

Add a new task at the bottom of the playbook to gather LLDP neighbors from devices.

```
      - name: GATHER LLDP FACTS
        napalm_get_facts:
          provider: "{{ napalm_connection_detail }}"
          filter: ['lldp_neighbors']
        register: lldp_data
        tags: lldp
```

##### Step 2

Add another task to print `lldp_data`.

```
      - name: PRINT LLDP FACTS
        debug:
          var: lldp_data
        tags: lldp
```


##### Step 3

Execute the playbook using the `lldp` tag.

```
ntc@ntc-training:ansible$ ansible-playbook -i inventory generate-reports.yml --tags=lldp
```

You should see all LLDP neighbor data is stored in the `napalm_lldp_neighbors` key within the `ansible_facts` dictionary in the debug output.  


##### Step 4

Create a new templated called `lldp.j2`.

```

Neighbors: {{ napalm_lldp_neighbors | to_nice_json }}

```

##### Step 5

Add a task to create the report files for LLDP neighbors.

```yaml
      - name: GENERATE REPORT FOR LLDP
        template:
          src: lldp.j2
          dest: ./reports/{{ inventory_hostname }}/02_lldp.txt
        tags: lldp
```

Feel free to check the new created files:

```
ntc@ntc-training:ansible$ cat reports/vmx1/02_lldp.txt
Neighbors: {
    "fxp0": [
        {
            "hostname": "vmx2",
            "port": "fxp0"
        },
        {
            "hostname": "vmx3",
            "port": "fxp0"
        },
        {
            "hostname": "eos-spine1.ntc.com",
            "port": "Management1"
        },
        {
            "hostname": "eos-leaf4.ntc.com",
            "port": "Management1"
        },
        {
            "hostname": "eos-leaf3.ntc.com",
            "port": "Management1"
        },
        {
            "hostname": "eos-spine3.ntc.com",
            "port": "Management1"
        },
        {
            "hostname": "eos-spine2.ntc.com",
            "port": "Management1"
        },
        {
            "hostname": "eos-spine4.ntc.com",
            "port": "Management1"
        },
        {
            "hostname": "eos-leaf2.ntc.com",
            "port": "Management1"
        },
        {
            "hostname": "eos-leaf1.ntc.com",
            "port": "Management1"
        }
    ],
    "ge-0/0/0": [
        {
            "hostname": "vmx2",
            "port": "ge-0/0/0"
        }
    ],
    "ge-0/0/1": [
        {
            "hostname": "vmx3",
            "port": "ge-0/0/1"
        }
    ]
}
ntc@ntc-training:ansible$

```

##### Step 6

In order to make this a real report, we'll need to loop through the data.  We should see that the core data structure is a dictionary with keys being local interfaces and the values are a list of dictionaries that contain all neighbors found on the local interfaces.

Update `lldp.j2` so it looks like the following:

```

Neighbors:

{% for interface, neighbors in napalm_lldp_neighbors.items() %}
{% for neighbor in neighbors %}
Local Device:       {{ inventory_hostname }}
Local Interface:    {{ interface }}
Neighbor Device:    {{ neighbor.hostname.split('.')[0] }}
Neighbor Interface: {{ neighbor.port }}

{% endfor %}
{% endfor %}
```

##### Step 7

Re-run the playbook.

```
ntc@ntc-training:ansible$ ansible-playbook -i inventory generate-reports.yml --tags=lldp
```

##### Step 8

View the enhanced reports:

```
ntc@ntc-training:ansible$ cat reports/vmx1/02_lldp.txt                                  
Local Device:       vmx1
Local Interface:    ge-0/0/1
Neighbor Device:    vmx3
Neighbor Interface: ge-0/0/1

Local Device:       vmx1
Local Interface:    fxp0
Neighbor Device:    vmx2
Neighbor Interface: fxp0

Local Device:       vmx1
Local Interface:    fxp0
Neighbor Device:    vmx3
Neighbor Interface: fxp0

Local Device:       vmx1
Local Interface:    fxp0
Neighbor Device:    eos-spine1
Neighbor Interface: Management1

Local Device:       vmx1
Local Interface:    fxp0
Neighbor Device:    eos-leaf4
Neighbor Interface: Management1

Local Device:       vmx1
Local Interface:    fxp0
Neighbor Device:    eos-leaf3
Neighbor Interface: Management1

Local Device:       vmx1
Local Interface:    fxp0
Neighbor Device:    eos-spine3
Neighbor Interface: Management1

Local Device:       vmx1
Local Interface:    fxp0
Neighbor Device:    eos-spine2
Neighbor Interface: Management1

Local Device:       vmx1
Local Interface:    fxp0
Neighbor Device:    eos-spine4
Neighbor Interface: Management1

Local Device:       vmx1
Local Interface:    fxp0
Neighbor Device:    eos-leaf2
Neighbor Interface: Management1

Local Device:       vmx1
Local Interface:    fxp0
Neighbor Device:    eos-leaf1
Neighbor Interface: Management1

Local Device:       vmx1
Local Interface:    ge-0/0/0
Neighbor Device:    vmx2
Neighbor Interface: ge-0/0/0

ntc@ntc-training:ansible$
```


### Task 4 - Assemble reports

##### Step 1

Add a new task to make sure the `./reports/summary` directory exist.  We are now going to create a master report for our devices.

```
      - name: ENSURE SUMMARY DIRECTORY EXISTS
        file:
          path: ./reports/summary
          state: directory
        tags: summary
```

##### Step 2

Execute the playbook with the `summary` tag set.

##### Step 3

Use the `assemble` module to assemble the devices' reports into a single `{{ inventory_hostname }}.txt` report in `./reports/summary`.

```
      - name: CREATE DEVICE SUMMARY REPORT
        assemble:
          src: ./reports/{{ inventory_hostname}}/
          dest: ./reports/summary/{{ inventory_hostname}}.txt
          delimiter: "---"
        tags: summary
```

Check out the new summary reports.  This is why we numbered the templates using 01 and 02--so they are assembled in order.

```
ntc@ntc-training:ansible$ cat reports/summary/vmx1.txt                       

Device:  vmx1

Hostname:        vmx1
FQDN:            vmx1.ntc.com
Model:           VMX
OS Version:      15.1F4.15
Serial Number:   VMXab
Vendor:          Juniper
---
Local Device:       vmx1
Local Interface:    ge-0/0/1
Neighbor Device:    vmx3
Neighbor Interface: ge-0/0/1

Local Device:       vmx1
Local Interface:    fxp0
Neighbor Device:    vmx2
Neighbor Interface: fxp0

Local Device:       vmx1
Local Interface:    fxp0
Neighbor Device:    vmx3
Neighbor Interface: fxp0

Local Device:       vmx1
Local Interface:    fxp0
Neighbor Device:    eos-spine1
Neighbor Interface: Management1

Local Device:       vmx1
Local Interface:    fxp0
Neighbor Device:    eos-leaf4
Neighbor Interface: Management1

Local Device:       vmx1
Local Interface:    fxp0
Neighbor Device:    eos-leaf3
Neighbor Interface: Management1

Local Device:       vmx1
Local Interface:    fxp0
Neighbor Device:    eos-spine3
Neighbor Interface: Management1

Local Device:       vmx1
Local Interface:    fxp0
Neighbor Device:    eos-spine2
Neighbor Interface: Management1

Local Device:       vmx1
Local Interface:    fxp0
Neighbor Device:    eos-spine4
Neighbor Interface: Management1

Local Device:       vmx1
Local Interface:    fxp0
Neighbor Device:    eos-leaf2
Neighbor Interface: Management1

Local Device:       vmx1
Local Interface:    fxp0
Neighbor Device:    eos-leaf1
Neighbor Interface: Management1

Local Device:       vmx1
Local Interface:    ge-0/0/0
Neighbor Device:    vmx2
Neighbor Interface: ge-0/0/0

ntc@ntc-training:ansible$
```

##### Step 4

Add a new task to create ONE MASTER report from the device summary reports.

      - name: CREATE DEVICE SUMMARY REPORT
        assemble:
          src: ./reports/summary
          dest: ./reports/master-all.txt
          delimiter: "___________________"
        tags: summary

##### Step 5

Run the playbook with the `summary` tag.

##### Step 6

View the final report:

```
ntc@ntc-training:ansible$ cat reports/master-all.txt
```

### Task 5 - Optional

The `napalm_get_facts` module supports even more filters. A few more of them are:

  * bgp_neighbors
  * bgp_neighbors_detail
  * lldp
  * lldp_neighbor_detail
  * interfaces
  * interfaces_ip

For a complete list of supported "filters" or _getters_ per operating system (OS), please reference the [NAPALM support matrix](http://napalm.readthedocs.io/en/latest/support/).

Now try a few out in your playbook, and debug what is returned!
