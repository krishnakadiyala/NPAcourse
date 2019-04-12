## Lab 14 - Using Network Centric Jija2 Filters


### Task 1 - Using Jinja2 Filters

Filters in Asible are from Jinja2, and some are used for transforming data inside a template expression. Building Jinja2 templates happens in the Ansible control host not in the targeted remote device, so filters execute on the control host as theey manipulate local data.

Jinja2 ships with many filters already but in addition to those Ansible also ships with it's own and allow users to add their own custom filters.


##### Step 1

Create a new playbook in the `ansible` directory called `jinja_filters.yml`.

```
ntc@jump-host:ansible$ touch user_input.yml
ntc@jump-host:ansible$

```
##### Step 2

Open this file with a text editor and input the play definition as follows:

```yaml

---

  - name: TEST JINJA FILTERS
    hosts: localhost
    connection: local
    gather_facts: no
      
```

>Note: Since we are not targeting any remote devices lets use `localhost` as the value for `hosts`.

##### Step 3

Add a `vars` key and our first variable `hostname` and task to debug and apply the `upper` filter. This filter will convert a value to uppercase as we will see after running the playbook.


```yaml

---

  - name: TEST JINJA FILTERS
    hosts: localhost
    connection: local
    gather_facts: no

    vars:
      hostname: nycr1
      
    tasks:
    
    
      - name: UPPERCASE HOSTNAME
        debug:
          var: hostname | upper
          
      - name: UPPERCASE HOSTNAME IN A MESSAGE
        debug:
          msg: "The hostname is {{ hostname | upper }}"
            
```

##### Step 4

Save and execute the playbook.

You should see the following output.

```commandline

ntc@jump-host:ansible$ ansible-playbook jinja_filters.yml

PLAY [TEST JINJA FILTERS] ***************************************************************************************

TASK [UPPERCASE HOSTNAME] ***************************************************************************************
ok: [localhost] => {
    "hostname | upper": "NYCR1"
}

TASK [UPPERCASE HOSTNAME IN A MESSAGE] **************************************************************************
ok: [localhost] => {
    "msg": "The hostname is NYCR1"
}

PLAY RECAP ******************************************************************************************************
localhost                  : ok=2    changed=0    unreachable=0    failed=0

ntc@jump-host:ansible$

```

##### Step 5


Lets add another variable under `vars` called `vlans` and make a list of vlans and it's name for each. Also add a new `debug` task using the `lenght` filter which will return the number of items of a sequence (list) or mapping (dictionary). 

```yaml

---

  - name: TEST JINJA FILTERS
    hosts: localhost
    connection: local
    gather_facts: no

    vars:
      hostname: nycr1

      vlans:
        - id: 10
          name: web_vlan
        - id: 20
          name: app_vlan
        - id: 30
          name: db_vlan
      
    tasks:
    
      - name: UPPERCASE HOSTNAME
        debug:
          var: hostname | upper
          
      - name: UPPERCASE HOSTNAME IN A MESSAGE
        debug:
          msg: "The hostname is {{ hostname | upper }}"

      - name: VERIFY LENGTH OF LIST
        debug:
          msg: "There are {{ vlans | length }} VLANs on the switch."

```

##### Step 6

Save and execute the playbook.

You should see the following output. 


```commandline

ntc@jump-host:ansible$ ansible-playbook jinja_filters.yml

PLAY [TEST JINJA FILTERS] ***************************************************************************************

TASK [UPPERCASE HOSTNAME] ***************************************************************************************
ok: [localhost] => {
    "hostname | upper": "NYCR1"
}

TASK [UPPERCASE HOSTNAME IN A MESSAGE] **************************************************************************
ok: [localhost] => {
    "msg": "The hostname is NYCR1"
}

TASK [VERIFY LENGTH OF LIST] **************************************************************************************
ok: [localhost] => {
    "msg": "There are 3 VLANs on the switch."
}

PLAY RECAP ******************************************************************************************************
localhost                  : ok=3    changed=0    unreachable=0    failed=0

ntc@jump-host:ansible$

```

##### Step 7

Add a new variable under `vars` called `interfaces_config` and a new `debug` task to use the `selectattr` and `list` filters chained together. 

The `selectattr` filter reads through a sequence of objects by applying a test to the specified attribute of each object, and only selecting the objects with the test succeeding. If no test is specified, the attribute’s value will be evaluated as a boolean.


```yaml

---

  - name: TEST JINJA FILTERS
    hosts: localhost
    connection: local
    gather_facts: no

    vars:
      hostname: nycr1

      vlans:
        - id: 10
          name: web_vlan
        - id: 20
          name: app_vlan
        - id: 30
          name: db_vlan
          
      interfaces_config:
        - name: Eth1
          speed: 1000
          duplex: full
          status: true
        - name: Eth3
          speed: 1000
          duplex: full
          status: true
        - name: Eth3
          speed: 1000
          duplex: full
          status: false
      
    tasks:
    
      - name: UPPERCASE HOSTNAME
        debug:
          var: hostname | upper
          
      - name: UPPERCASE HOSTNAME IN A MESSAGE
        debug:
          msg: "The hostname is {{ hostname | upper }}"

      - name: VERIFY LENGTH OF LIST
        debug:
          msg: "There are {{ vlans | length }} VLANs on the switch."
          
      - name: GET ELEMENTS THAT HAVE A TRUE VALUE FOR STATUS AS A LIST
        debug:
          var: interfaces_config | selectattr("status") | list

```

##### Step 8

Save and execute the playbook.

You should see the following output.

```commandline

ntc@jump-host:ansible$ ansible-playbook jinja_filters.yml

PLAY [TEST JINJA FILTERS] ***************************************************************************************

TASK [UPPERCASE HOSTNAME] ***************************************************************************************
ok: [localhost] => {
    "hostname | upper": "NYCR1"
}

TASK [UPPERCASE HOSTNAME IN A MESSAGE] **************************************************************************
ok: [localhost] => {
    "msg": "The hostname is NYCR1"
}

TASK [VERIFY LENGTH OF LIST] **************************************************************************************
ok: [localhost] => {
    "msg": "There are 3 VLANs on the switch."
}

TASK [GET ELEMENTS THAT HAVE A TRUE VALUE FOR STATUS AS A LIST] ***************************************************
ok: [localhost] => {
    "interfaces_config | selectattr(\"status\") | list": [
        {
            "duplex": "full",
            "name": "Eth1",
            "speed": 1000,
            "status": true
        },
        {
            "duplex": "full",
            "name": "Eth3",
            "speed": 1000,
            "status": true
        }
    ]
}

PLAY RECAP ******************************************************************************************************
localhost                  : ok=4    changed=0    unreachable=0    failed=0

ntc@jump-host:ansible$
```

##### Step 9

Add two more `debug` tasks to the playbook using the `map` filter that is applied on a sequence of objects or looks up an attribute. This filter can be useful when dealing with lists of objects but you are only really interested in a certain value of it.

The basic usage is mapping on an attribute. Imagine you have a list of  `interfaces` or `vlans` but you are only interested in a list of __names__ of the interfaces or vlans.



```yaml

      - name: RETURN LIST OF ALL NAME KEYS IN THE INTERFACES_CONFIG LIST OF DICTIONARIES
        debug:
          var: interfaces_config | map(attribute="name") | list

      - name: RETURN LIST OF ALL NAME KEYS IN THE INTERFACES_CONFIG LIST OF DICTIONARIES
        debug:
          var: vlans | map(attribute="name") | list

```

##### Step 10

Save and execute the playbook.

You should see the following output.

```commandline

ntc@jump-host:ansible$ ansible-playbook jinja_filters.yml
....output omitted

TASK [RETURN LIST OF ALL NAME KEYS IN THE INTERFACES_CONFIG LIST OF DICTIONARIES] *******************************************************
ok: [localhost] => {
    "interfaces_config | map(attribute=\"name\") | list": [
        "Eth1",
        "Eth3",
        "Eth3"
    ]
}

TASK [RETURN LIST OF ALL NAME KEYS IN THE INTERFACES_CONFIG LIST OF DICTIONARIES] ********************************************************ok: [localhost] => {
    "vlans | map(attribute=\"name\") | list": [
        "web_vlan",
        "app_vlan",
        "db_vlan"
    ]
}
PLAY RECAP ******************************************************************************************************
localhost                  : ok=6    changed=0    unreachable=0    failed=0

ntc@jump-host:ansible$

```

##### Step 11


Add another task to the playbook but this time we are going to chain together `selectattr`, `map` and `list` filters. This is going to allow us to just return a list of interface names that are up.

Chaining these filters together will allow `selectattr` to just target the status of the interfaces that are `true` and using the `map` filter will target the names of the interfaces then `list` filter will return a list.  


```yaml

      - name: RETURN JUST LIST OF INTERFACE NAMES THAT ARE UP (TRUE)
        debug:
          var: interfaces_config | selectattr("status") | map(attribute="name") | list

```

##### Step 12

Save and execute the playbook.

You should see the following output.

```commandline

ntc@jump-host:ansible$ ansible-playbook jinja_filters.yml
....output omitted

TASK [RETURN JUST LIST OF INTERFACE NAMES THAT ARE UP (TRUE)] ***************************************************
ok: [localhost] => {
    "interfaces_config | selectattr(\"status\") | map(attribute=\"name\") | list": [
        "Eth1",
        "Eth3"
    ]
}

PLAY RECAP ************************************************************************************************************
localhost                  : ok=7    changed=0    unreachable=0    failed=0

```

##### Step 13

Lets try out one more test. Add another variable and call it `interface_state` and one more `debug` task using the `ternary` filter. 

This filter allows us to apply logic to a variable without having to use `python` syntax. Both tasks will return the same output based on the variable value but are written differently.

```yaml


vars:

  interface_state: false
  
  #....omitted
  
tasks:
  
  #....omitted

      - name: CONVERT BOOLEAN T/F TO SOMETHING MORE CONTEXTUAL FOR NETWORKING
        debug:
          var: interface_state | ternary("up", "down")

      - name: CONVERT BOOLEAN T/F TO SOMETHING MORE CONTEXTUAL FOR NETWORKING
        debug:
          msg: "{{ 'up' if interface_state else 'down' }}"

```

##### Step 14

Save and execute the playbook.

You should see the following output.

```commandline

ntc@jump-host:ansible$ ansible-playbook jinja_filters.yml
....output omitted

TASK [CONVERT BOOLEAN T/F TO SOMETHING MORE CONTEXTUAL FOR NETWORKING] *******************************************************************
ok: [localhost] => {
    "interface_state | ternary(\"up\", \"down\")": "down"
}

TASK [CONVERT BOOLEAN T/F TO SOMETHING MORE CONTEXTUAL FOR NETWORKING] ****************************************************
ok: [localhost] => {
    "msg": "down"
}

PLAY RECAP ***************************************************************************************
localhost                  : ok=9    changed=0    unreachable=0    failed=0

ntc@jump-host:ansible$

```

Give it another try, except this time change `interface_state` to **true**


Check the final playbook

```yaml

---

  - name: TEST JINJA FILTERS
    hosts: localhost
    connection: local
    gather_facts: no

    vars:
      interface_state: false

      hostname: nycr1

      vlans:
        - id: 10
          name: web_vlan
        - id: 20
          name: app_vlan
        - id: 30
          name: db_vlan
          
      interfaces_config:
        - name: Eth1
          speed: 1000
          duplex: full
          status: true
        - name: Eth3
          speed: 1000
          duplex: full
          status: true
        - name: Eth3
          speed: 1000
          duplex: full
          status: false
          
    tasks:
    
      - name: UPPERCASE HOSTNAME
        debug:
          var: hostname | upper
          
      - name: UPPERCASE HOSTNAME IN A MESSAGE
        debug:
          msg: "The hostname is {{ hostname | upper }}"

      - name: VERIFY LENGTH OF LIST
        debug:
          msg: "There are {{ vlans | length }} VLANs on the switch."
        
      - name: GET ELEMENTS THAT HAVE A TRUE VALUE FOR STATUS AS A LIST
        debug:
          var: interfaces_config | selectattr("status") | list

      - name: RETURN LIST OF ALL NAME KEYS IN THE INTERFACES_CONFIG LIST OF DICTIONARIES
        debug:
          var: interfaces_config | map(attribute="name") | list

      - name: RETURN LIST OF ALL NAME KEYS IN THE INTERFACES_CONFIG LIST OF DICTIONARIES
        debug:
          var: vlans | map(attribute="name") | list

      - name: RETURN JUST LIST OF INTERFACE NAMES THAT ARE UP (TRUE)
        debug:
          var: interfaces_config | selectattr("status") | map(attribute="name") | list

      - name: CONVERT BOOLEAN T/F TO SOMETHING MORE CONTEXTUAL FOR NETWORKING
        debug:
          var: interface_state | ternary("up", "down")

      - name: CONVERT BOOLEAN T/F TO SOMETHING MORE CONTEXTUAL FOR NETWORKING
        debug:
          msg: "{{ 'up' if interface_state else 'down' }}"
```
