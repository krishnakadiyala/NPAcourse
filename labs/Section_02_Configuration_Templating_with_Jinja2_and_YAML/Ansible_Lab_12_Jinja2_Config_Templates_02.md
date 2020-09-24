# Lab 12 - Using Improved Jinja2 Templates

### Task 1 - Updating the SNMP Data Model

In the previous lab, the SNMP data was modeled as a set of invdividual key-value pairs.

This works for a simple use case, but what if we had to configure multiple read-only and read-write strings?

This task will expand the data structure currently being used by the `AMER` and `EMEA` groups.


##### Step 1

Add the `snmp_config` variable into the `AMER.yml` file and also remove what was currently there from the last lab:


``` yaml
snmp_config:
  ro:
    - public
    - ntc-course
  rw:
    - private
    - ntc-private
  contact: netops_team
  location: NYC

```

Note: Ensure the existing four variables, e.g. `snmp_ro`, `snmp_rw`, `snmp_location`, and `snmp_contact` are no longer in this file.


##### Step 2

Repeat and add the `snmp_config` variable to the `EMEA.yml` file.


``` yaml
snmp_config:
  ro:
    - public
    - ntc-course
  rw:
    - private
    - ntc-private
  contact: netops_team
  location: MILAN


```

Note: Ensure the existing four variables, e.g. `snmp_ro`, `snmp_rw`, `snmp_location`, and `snmp_contact` are no longer in this file.


##### Step 3

But now, since our data model has changed, we need to also update our Jinja2 templates to correctly access the values.

Create a new file called `ios-snmpv2.j2` within the templates directory and open it with a text editor.
We will use the following template to render the desired configuration.


```
{% for ro_comm in snmp_config.ro %}
snmp-server community {{ ro_comm }} RO
{% endfor %}
{% for rw_comm in snmp_config.rw %}
snmp-server community {{ rw_comm }} RW
{% endfor %}
snmp-server location {{ snmp_config.location }}
snmp-server contact {{ snmp_config.contact }}

```


Similarly, create a `junos-snmpv2.j2` template file, using the JUNOS configuration commands.

```
{% for ro_comm in snmp_config.ro %}
set snmp community {{ ro_comm }} authorization read-only
{% endfor %}
{% for rw_comm in snmp_config.rw %}
set snmp community {{ rw_comm }} authorization read-write
{% endfor %}
set snmp location {{ snmp_config.location }}
set snmp contact {{ snmp_config.contact }}

```


##### Step 4

Return to `deploy-snmp.yml` and update the `src` parameter in the template task to point to the new templates that were created in the previous step and also remove the `debug` tasks for now.

At this point, the playbook should look as follows: 

``` yaml

---

- name: GENERATE SNMP CONFIGS USING JINJA2 - AMERICAS
  hosts: AMER
  connection: local
  gather_facts: no

  tasks:
 
    - name: GENERATE IOS SNMP CONFIGURATIONS
      template:
         src: ios-snmpv2.j2
         dest: "./configs/{{ inventory_hostname }}-snmp.cfg"

- name: GENERATE SNMP CONFIGS USING JINJA2 - EMEA
  hosts: EMEA
  connection: local
  gather_facts: no

  tasks:
    
    - name: GENERATE JUNOS SNMP CONFIGURATIONS
      template:
        src: junos-snmpv2.j2
        dest: "./configs/{{ inventory_hostname }}-snmp.cfg"


```

##### Step 5

Now run the playbook.

```
ntc@ntc-training:ansible$ ansible-playbook -i inventory deploy-snmp.yml
```


##### Step 6

Validate that all device configurations are correct in the `configs` sub-directory.



### Task 2 - Managing Unique Devices

In the last task, you built configurations for all `AMER` devices (all CSRs) and for all `EMEA` devices (all vMXs).  In this task, you need to account for a one-off device that requires a different SNMP configuration than what has been defined in the `group_vars` directory.


##### Step 1

Create a new directory called `host_vars`.  

The name of the directory called `host_vars` is an important and reserved directory name within Ansible, just like you've seen with `group_vars`.  This directory will store "host based variables" - these map directly to a host that is found in the inventory file.  For example, the variables that end up in `host_vars/nxos-spine1.yml` will only be used and available to **nxos-spine1**.

##### Step 2

In the `host_vars` directory, create one `host_vars` file, called `csr3.yml`.  This is the device that requires a special configuration for SNMP.

##### Step 3

Add the following `snmp_config` variable into the `csr3.yml` file.

``` yaml
snmp_config:
  ro:
    - ntc-public
  rw:
    - private
    - ntc-private
  contact: netdevops_tiger_team
  location: NYC

```

##### Step 4

Now run the playbook.

```
ntc@ntc-training:ansible$ ansible-playbook -i inventory deploy-snmp.yml
```


##### Step 5

Validate that all device configurations are correct in the `configs` sub-directory focusing on **csr3**.  Compare its configuration to **csr1**.

##### Step 6

Add a `debug` statement to *each* play to debug the `snmp_config` variable for each group of devices, e.g. `AMER` and `EMEA`.

```yaml
    - name: DEBUG AND PRINT SNMP VARIABLES
      debug:
        var: snmp_config
```

This should be added for _each_ play.

##### Step 7

Execute the playbook.  

What do you see?  

What kind of data type is `snmp_config`?  

##### Step 8

Ansible allows us to parameterize not only the file names of the config files being generated, such as using `inventory_hostname` 
to dynamically make unique filenames, but also to parameterize the template file name. Since Ansible is aware of each inventory device's
network operating system, and our templates adhere to that naming convention, we can consolidate both template tasks into one task, using 
the `ansible_network_os` magic variable. 

The new source filename Ansible looks for would be `"{{ ansible_network_os }}-snmpv2.j2"`, where the first part of the filename would be replaced
with `ios` or `junos` depending on the `ansible_network_os`. 

The new playbook is as follows:
```yaml
---

- name: GENERATE SNMP CONFIGS USING JINJA2
  hosts: AMER, EMEA
  connection: local
  gather_facts: no

  tasks:
 
    - name: GENERATE SNMP CONFIGURATIONS
      template:
         src: "{{ ansible_network_os }}-snmpv2.j2"
         dest: "./configs/{{ inventory_hostname }}-snmp.cfg"

```

The new playbook has both the AMER and EMEA groups in one play. Change your playbook to be the same as the above playbook, updating both the `hosts`
and `tasks`.

Re-run your playbook and observe the output, which should result in the same config file outputs. 