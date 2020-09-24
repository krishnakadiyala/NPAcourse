# Lab 11 - Getting Started with Jinja2 Templating in Ansible

### Task 1 - Using Jinja2 to Build Configuration Templates

In this task we will learn how to use Jinja2 templates in Ansible to dynamically build configuration files.



##### Step 1

Create a new playbook within the `ansible` directory:

```
ntc@ntc-training:ansible$ touch deploy-snmp.yml
ntc@ntc-training:ansible$
```


##### Step 2

Open this file using any text editor and add the following play definition:

```yaml

---

- name: GENERATE SNMP CONFIGS USING JINJA2 - AMERICAS
  hosts: AMER
  connection: local
  gather_facts: no

```

##### Step 3

Define a SNMP RO string as a variable within the playbook:

``` yaml

---

- name: GENERATE SNMP CONFIGS USING JINJA2 - AMERICAS
  hosts: AMER
  connection: local
  gather_facts: no

  vars:
    snmp_ro: ntc_course

```

##### Step 4

Using the `debug` module, create a task that will display the variable `snmp_ro`.


```yaml

---

- name: GENERATE SNMP CONFIGS USING JINJA2 - AMERICAS
  hosts: AMER
  connection: local
  gather_facts: no

  vars:
    snmp_ro: ntc_course

  tasks:

    - name: VIEW SNMP_RO VARIABLE
      debug: 
        var: snmp_ro
```
##### Step 5

Execute the playbook and view the results from the `debug` module.


```commandline
ntc@ntc-training:ansible$ ansible-playbook -i inventory deploy-snmp.yml

PLAY [GENERATE SNMP CONFIGS USING JINJA2 - AMERICAS] ***************************************************

TASK [VIEW SNMP_RO VARIABLE] ****************************************************************************
ok: [csr1] => {
    "snmp_ro": "ntc_course"
}
ok: [csr2] => {
    "snmp_ro": "ntc_course"
}
ok: [csr3] => {
    "snmp_ro": "ntc_course"
}

PLAY RECAP ********************************************************************************************
csr1                       : ok=1    changed=0    unreachable=0    failed=0
csr2                       : ok=1    changed=0    unreachable=0    failed=0
csr3                       : ok=1    changed=0    unreachable=0    failed=0

ntc@ntc-training:ansible$
```

>Note: As we learned earlier we can define variables in different locations like inside our inventory, playbook, included files, roles, Ansible command line, local facts, host_vars and group_vars directories, which Ansible will find based on the module.

##### Step 6


Using the Ansible `template` module, let's add a new task that will take this variable and render it with a Jinja template (that is yet to be created):

``` yaml

---

- name: GENERATE SNMP CONFIGS USING JINJA2 - AMERICAS
  hosts: AMER
  connection: local
  gather_facts: no

  vars:
    snmp_ro: ntc_course

  tasks:
  
    - name: VIEW SNMP_RO VARIABLE
      debug: 
        var: snmp_ro
        
    - name: GENERATE IOS SNMP CONFIGURATIONS
      template:
        src: ios-snmp.j2
        dest: "./configs/{{ inventory_hostname }}-snmp.cfg"
```



##### Step 7

In the previous step, the source of the template was identified as a `j2` file. Ansible by default will look in the current directory and a directory named `templates` for these files. Let us create this if it's not there already.

Create a `templates` directory if it's not there already within the `ansible` directory and navigate to that directory.

```
ntc@ntc-training:ansible$
ntc@ntc-training:ansible$ mkdir templates
ntc@ntc-training:ansible$ cd templates
ntc@ntc-training:templates$
```

##### Step 8

In the `templates` directory, create the Jinja template we will be using to render the SNMP configuration, by using the `touch` command if it's not present already. 

> Note: this already referenced in the playbook.

```
ntc@ntc-training:templates$ touch ios-snmp.j2
ntc@ntc-training:templates$
```


##### Step 9

Open the `ios-snmp.j2` file using a text editor and add the snmp configuration template for it. This is simply a text file with the values for the SNMP variable "parameterized".

```
snmp-server community {{ snmp_ro }}  RO
```

Keep in mind that the value for this variable was defined in **Step 3** within the playbook.  

**Ansible auto-loads all variables it's aware of at run-time and makes those variables available to the playbook and any template similar to what we saw with the debug module.**


##### Step 10

Run the playbook as follows:

```
ntc@ntc-training:ansible$ ansible-playbook -i inventory deploy-snmp.yml

PLAY [GENERATE SNMP CONFIGS USING JINJA2 - AMERICAS] *********************************************************************************

TASK [VIEW SNMP_RO VARIABLE] ***********************************************************************************************************
ok: [csr1] => {
    "snmp_ro": "ntc_course"
}
ok: [csr2] => {
    "snmp_ro": "ntc_course"
}
ok: [csr3] => {
    "snmp_ro": "ntc_course"
}
TASK [GENERATE IOS SNMP CONFIGURATIONS] ***********************************************************************************
changed: [csr1]
changed: [csr2]
changed: [csr3]

PLAY RECAP **************************************************************************************************************
csr1                       : ok=2    changed=1    unreachable=0    failed=0   
csr2                       : ok=2    changed=1    unreachable=0    failed=0   
csr3                       : ok=2    changed=1    unreachable=0    failed=0   

ntc@ntc-training:ansible$
```

##### Step 11

Validate that the variables have been rendered correctly by checking the files created in the `configs` directory.

```
ntc@ntc-training:ansible$ cd configs
ntc@ntc-training:configs$ cat csr1-snmp.cfg

snmp-server community ntc_course  RO
```


### Task 2 - Expanding the Jinaj2 Template and Using Group Variables

In this task we will template the configuration for some additional SNMP parameters, which will be different for the `AMER` group and the `EMEA` group.

##### Step 1

Create a new directory called `group_vars`.  

The name of the directory called `group_vars` is an important name within Ansible.  It will store "group based variables" - these map directly to the groups that are found in the inventory file.  For example, the variables that end up in `group_vars/all.yml` will be available to all devices. In this directory, create two group_vars files, called `AMER.yml` and `EMEA.yml`


```
ntc@ntc-training:ansible$ mkdir group_vars
ntc@ntc-training:ansible$ cd group_vars
ntc@ntc-training:group_vars$ touch AMER.yml
ntc@ntc-training:group_vars$ touch EMEA.yml
ntc@ntc-training:group_vars$

```


##### Step 2

Open the `AMER.yml` using a text editor and update it with the following variables:

```yaml
snmp_ro: ntc_course
snmp_rw: ntc_private
snmp_location: NYC
snmp_contact: netops_team

```

##### Step 3

Similarly update `EMEA.yml` to contain the EMEA region specific SNMP variables.

``` yaml
snmp_ro: ntc_course
snmp_rw: ntc_private
snmp_location: MILAN
snmp_contact: netops_team
```



##### Step 4

Update the `ios-snmp.j2` file to render the rest of the SNMP configurations:

```
snmp-server community {{ snmp_ro }}  RO
snmp-server community {{ snmp_rw }}  RW
snmp-server contact {{ snmp_contact }}  
snmp-server location {{ snmp_location }}

```

##### Step 5

Create a `junos-snmp.j2` file in the templates directory to render the JUNOS configuration commands if it's not there already.

```
set snmp community {{ snmp_ro }} authorization read-only
set snmp community {{ snmp_rw }} authorization read-write
set snmp location {{ snmp_location }}
set snmp contact {{ snmp_contact }}


```

##### Step 6

Since the `snmp_ro` variable has been defined as a group variable, we can now remove it from the top of the playbook `deploy-snmp.yml` and add another task using the `debug` module to view `snmp_location`.

``` yaml

---

- name: GENERATE SNMP CONFIGS USING JINJA2 - AMERICAS
  hosts: AMER
  connection: local
  gather_facts: no

  tasks:
 
    - name: VIEW SNMP_RO VARIABLE
      debug: 
         var: snmp_ro
        
    - name: VIEW SNMP_LOCATION VARIABLE
      debug: 
         var: snmp_location
        
        
    - name: GENERATE IOS SNMP CONFIGURATIONS
      template:
         src: ios-snmp.j2
         dest: "./configs/{{ inventory_hostname }}-snmp.cfg"

```

##### Step 7

Add one more play to this playbook to also build the JUNOS specific configurations used on the EMEA devices and add the same debug tasks from the first play.

``` yaml

---

- name: GENERATE SNMP CONFIGS USING JINJA2 - AMERICAS
  hosts: AMER
  connection: local
  gather_facts: no

  tasks:
 
    - name: VIEW SNMP_RO VARIABLE
      debug: 
         var: snmp_ro
        
    - name: VIEW SNMP_LOCATION VARIABLE
      debug: 
         var: snmp_location
        
        
    - name: GENERATE IOS SNMP CONFIGURATIONS
      template:
         src: ios-snmp.j2
         dest: "./configs/{{ inventory_hostname }}-snmp.cfg"

- name: GENERATE SNMP CONFIGS USING JINJA2 - EMEA
  hosts: EMEA
  connection: local
  gather_facts: no

  tasks:
    
    - name: VIEW SNMP_RO VARIABLE
      debug: 
        var: snmp_ro
        
    - name: VIEW SNMP_LOCATION VARIABLE
      debug: 
        var: snmp_location
    
    - name: GENERATE JUNOS SNMP CONFIGURATIONS
      template:
        src: junos-snmp.j2
        dest: "./configs/{{ inventory_hostname }}-snmp.cfg"

```


##### Step 8

Execute the playbook and take a look at the output of the `debug` module:

```
ntc@ntc-training:ansible$ ansible-playbook -i inventory deploy-snmp.yml

PLAY [GENERATE SNMP CONFIGS USING JINJA2 - AMERICAS] **********************************************************************

TASK [VIEW SNMP_RO VARIABLE] ************************************************************************************************
ok: [csr1] => {
    "snmp_ro": "ntc_course"
}
ok: [csr2] => {
    "snmp_ro": "ntc_course"
}
ok: [csr3] => {
    "snmp_ro": "ntc_course"
}


TASK [VIEW SNMP_LOCATION VARIABLE] *************************************************************************************
ok: [csr1] => {
    "snmp_location": "NYC"
}
ok: [csr2] => {
    "snmp_location": "NYC"
}
ok: [csr3] => {
    "snmp_location": "NYC"
}

TASK [GENERATE IOS SNMP CONFIGURATIONS] ***********************************************************************************
changed: [csr3]
changed: [csr2]
changed: [csr1]

PLAY [GENERATE SNMP CONFIGS USING JINJA2 - EMEA] **************************************************************************

TASK [VIEW SNMP_RO VARIABLE] ************************************************************************************************
ok: [vmx1] => {
    "snmp_ro": "ntc_course"
}
ok: [vmx2] => {
    "snmp_ro": "ntc_course"
}
ok: [vmx3] => {
    "snmp_ro": "ntc_course"
}


TASK [VIEW SNMP_LOCATION VARIABLE] *************************************************************************************
ok: [vmx1] => {
    "snmp_location": "MILAN"
}
ok: [vmx2] => {
    "snmp_location": "MILAN"
}
ok: [vmx3] => {
    "snmp_location": "MILAN"
}


TASK [GENERATE JUNOS SNMP CONFIGURATIONS] *********************************************************************************
changed: [vmx2]
changed: [vmx1]
changed: [vmx3]

PLAY RECAP **************************************************************************************************************
csr1                       : ok=3    changed=0    unreachable=0    failed=0
csr2                       : ok=3    changed=0    unreachable=0    failed=0
csr3                       : ok=3    changed=0    unreachable=0    failed=0
vmx1                       : ok=3    changed=0    unreachable=0    failed=0
vmx2                       : ok=3    changed=0    unreachable=0    failed=0
vmx3                       : ok=3    changed=0    unreachable=0    failed=0  

ntc@ntc-training:ansible$

```


##### Step 9

Validate that the configurations have been created in the `configs` directory:

```
ntc@ntc-training:ansible$ ls configs/
# output omitted
```

Based on what you've learned so far, you should realize that you can simply add another task or play in this playbook and use the `ios_config` and `junos_config` modules or the `cli_config` module for a complete process of building and deploying the configurations.

