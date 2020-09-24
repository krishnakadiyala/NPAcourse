# Lab 10 - Continuous Compliance with IOS

This lab introduces a methodology to perform real-time validation and compliance of network configuration and operational state.

### Task 1

In order to perform any type of compliance, we must first gather data from the device.  We'll do this with the `_command` module similar to the last few labs.

##### Step 1

Create a new playbook called `compliance.yml` in the `ansible` directory.  

Use the following playbook to gather `show version` for the IOS devices.

```yaml

---

  - name: IOS COMPLIANCE
    hosts: iosxe
    connection: network_cli
    gather_facts: no


    tasks:

      - name: IOS show version
        ios_command:
          commands:
            - show version
        register: output

```

##### Step 2

Add a task that will _assert_ that version "17.01.01" is running each device and that the config register is set properly to "0x2102".

```yaml
      - name: CHECK OS AND CONFIG REGISTER
        assert:
          that:
           - "'17.01.01' in output['stdout'][0]"
           - "'0x2102' in output['stdout'][0]"

```

Since IOS doesn't return structured data (JSON), we're simply seeing if strings are inside other strings.  

> Note: In an upcoming lab, we'll look at parsing this data and converting it to structured data.

##### Step 3

Execute the playbook.

```
ntc@ntc-training:ansible$ ansible-playbook -i inventory compliance.yml   

PLAY [IOS COMPLIANCE] ***********************************************************************

TASK [IOS show version] *********************************************************************
ok: [csr1]
ok: [csr2]
ok: [csr3]

TASK [CHECK OS AND CONFIG REGISTER] *********************************************************
ok: [csr1] => {
    "changed": false,
    "msg": "All assertions passed"
}
ok: [csr2] => {
    "changed": false,
    "msg": "All assertions passed"
}
ok: [csr3] => {
    "changed": false,
    "msg": "All assertions passed"
}


PLAY RECAP **********************************************************************************
csr1                       : ok=2    changed=0    unreachable=0    failed=0   
csr2                       : ok=2    changed=0    unreachable=0    failed=0   
csr3                       : ok=2    changed=0    unreachable=0    failed=0   

ntc@ntc-training:ansible$
```

##### Check

Full and final playbook will look like this:

```yaml

---

  - name: IOS COMPLIANCE
    hosts: iosxe
    connection: network_cli
    gather_facts: no


    tasks:

      - name: IOS show version
        ios_command:
          commands:
            - show version
        register: output

      - name: CHECK OS AND CONFIG REGISTER
        assert:
          that:
           - "'17.01.01' in output['stdout'][0]"
           - "'0x2102' in output['stdout'][0]"

```

### Task 2

In Ansible 2.7 two new parameters were added to this module, `fail_msg` and `success_msg`. These new parameters allow us to customize what the user will see on the output of the result of a fail message or success message. 

##### Step 1

Add a new play and task to the existing playbook. 

Normally on the CLI of the newer versions of JUNOS OS you can run ` command | display json`  or ` command | display xml` to get a structured response on the terminal. For this playbook we are going to use that parameter to collect structured data and access values inside. 

```yaml

---

  - name: IOS COMPLIANCE
    hosts: iosxe
    connection: network_cli
    gather_facts: no


    tasks:

      - name: IOS show version
        ios_command:
          commands:
            - show version
        register: output

      - name: CHECK OS AND CONFIG REGISTER
        assert:
          that:
           - "'17.01.01' in output['stdout'][0]"
           - "'0x2102' in output['stdout'][0]"
           
           
  
  - name: JUNOS COMPLIANCE
    hosts: vmx
    connection: netconf
    gather_facts: no
    tags: vmx


    tasks:

      - name: JUNOS show version
        junos_command:
          commands:
            - show system storage
          display: json
        register: output
```

>Note: This time we added a new parameter called `display:` with a value of `json`

##### Step 2

Add a task that will display the response data from the variable stored in the `register` parameter.

```yaml

      - name: VIEW JSON DATA
        debug:
          var: output

```

##### Step 3

Execute the playbook and view the data that is stored in the `output` variable. 


```commandline


ntc@ntc-training:ansible$ ansible-playbook -i inventory compliance.yml   

.... output omitted ....

TASK [VIEW JSON DATA] ***********************************************************
ok: [vmx1] => {
    "output": {
        "changed": false,
        "failed": false,
        "stdout": [
            {
                "system-storage-information": [
                    {
                        "filesystem": [
                            {
                                "available-blocks": [
                                    {
                                        "attributes": {
                                            "junos:format": "17G"
                                        },
                                        "data": "36045584"
                                    }
                                ],
                                "filesystem-name": [
                                    {
                                        "data": "/dev/gpt/junos"
                                    }
                                ],
                                "mounted-on": [
                                    {
                                        "data": "/.mount"
                                    }
                                ],
                                "total-blocks": [
                                    {
                                        "attributes": {
                                            "junos:format": "20G"
                                        },
                                        "data": "41803892"
                                    }
                                ],
                                "used-blocks": [
                                    {
                                        "attributes": {
                                            "junos:format": "1.2G"
                                        },
                                        "data": "2413998"
                                    }
                                ],
                                "used-percent": [
                                    {
                                        "data": "  6"
                                    }
                                ]
                            },
                            {
                                "available-blocks": [
                                    {
                                        "attributes": {
                                            "junos:format": "365M"
                                        },
                                        "data": "746752"
                                    }
                                ],
                                
                                ..... output omitted
```


##### Step 4

Add a new task using the `set_fact` module that allows us to create new variables based on the output that we received and simplifies how to access the data when calling it. 

```yaml

      - name: CREATE NEW VARIABLES
        set_fact:
          percent: "{{ output['stdout'][0]['system-storage-information'][0]['filesystem'][0]['used-percent'][0]['data'] }}"
          filesystem: "{{ output['stdout'][0]['system-storage-information'][0]['filesystem'][0]['filesystem-name'][0]['data'] }}"
          blocks: "{{ output['stdout'][0]['system-storage-information'][0]['filesystem'][0]['available-blocks'][0]['data'] }}"
          storage: "{{ output['stdout'][0]['system-storage-information'][0]['filesystem'][0]['available-blocks'][0]['attributes']['junos:format'] }}"
```

##### Step 5

Add a task that will display the new variables created with `set_fact`. 

```yaml

      - name: VIEW DATA STORED IN NEW VARIABLES
        debug:
          msg: "Percent: {{ percent }}%,  filesystem: {{ filesystem }}, Blocks: {{ blocks }}, Storage: {{ storage }}"
```

##### Step 6

Execute the playbook and view the data that is stored in the new variables. 


```commandline
ntc@ntc-training:ansible$ ansible-playbook -i inventory compliance.yml   

.... output omitted ....

TASK [CREATE NEW VARIABLES] ****************************************************************************************************************************************************************************************************************************************************************
ok: [vmx3]
ok: [vmx1]
ok: [vmx2]

TASK [VIEW DATA STORED IN NEW VARIABLES] *******************************************************************************************************************************************************************************************************************************************************************
ok: [vmx1] => {
    "msg": "Percent:   6%,  filesystem: /dev/gpt/junos, Blocks: 36045584, Storage: 17G"
}
ok: [vmx2] => {
    "msg": "Percent:   6%,  filesystem: /dev/gpt/junos, Blocks: 36045584, Storage: 17G"
}
ok: [vmx3] => {
    "msg": "Percent:   6%,  filesystem: /dev/gpt/junos, Blocks: 36045584, Storage: 17G"
}

..... output omitted

```

##### Step 7

Add two tasks that will _assert_ the data returned from the stored variables and check the specified file systems to make sure they are at a desired storage space and availability. 

>Note: This task will run conditional logic to check that `if` data stored in `percent` is greater `>` than or equal `=` to the presented data which is integer of `50` then it will return either `True` or `False` in the form of `success_msg` or `fail_msg`. 


The assertion is also using `| int` after the `percent` because you can see the percent value is actually a string.  So this is using something called a Jinja filter (more on this later!) to convert the string to an integer so mathematical operations can be performed on the data.

```yaml

      - name: CHECK STORAGE FILESYSTEM PERCENT
        assert:
          that:
            - "percent | int  <= 50"
          fail_msg: "Warning!! filesystem {{ filesystem }} is at {{ percent }}%"
          success_msg: "Current filesystem  {{ filesystem }} is at {{ percent }}%"
        
      - name: CHECK STORAGE FILESYSTEM AVAILABILITY
        assert:
          that:
            - "blocks | int >= 4194304"
          fail_msg: "Warning!! filesystem {{ filesystem }} is at {{ storage }}"
          success_msg: "Current filesystem  {{ filesystem }} is at {{ storage }}"

```

##### Step 8


Execute the playbook and view results. 

```yaml
ntc@ntc-training:ansible$ ansible-playbook -i inventory compliance.yml   

.... output omitted ....

TASK [CREATE NEW VARIABLES] ********************************************************************************************************************************************************************************
ok: [vmx1]
ok: [vmx2]
ok: [vmx3]

TASK [VIEW DATA STORED IN NEW VARIABLES] *******************************************************************************************************************************************************************
ok: [vmx1] => {
    "msg": "Percent:   6%,  filesystem: /dev/gpt/junos, Blocks: 36045584, Storage: 17G"
}
ok: [vmx2] => {
    "msg": "Percent:   6%,  filesystem: /dev/gpt/junos, Blocks: 36045584, Storage: 17G"
}
ok: [vmx3] => {
    "msg": "Percent:   6%,  filesystem: /dev/gpt/junos, Blocks: 36045584, Storage: 17G"
}

TASK [CHECK STORAGE FILESYSTEM PERCENT] ********************************************************************************************************************************************************************
ok: [vmx1] => {
    "changed": false,
    "msg": "Current filesystem  /dev/gpt/junos is at   6%"
}
ok: [vmx2] => {
    "changed": false,
    "msg": "Current filesystem  /dev/gpt/junos is at   6%"
}
ok: [vmx3] => {
    "changed": false,
    "msg": "Current filesystem  /dev/gpt/junos is at   6%"
}

TASK [CHECK STORAGE FILESYSTEM AVAILABILITY] ****************************************************************************************************************************************************************
ok: [vmx1] => {
    "changed": false,
    "msg": "Current filesystem  /dev/gpt/junos is at 17G"
}
ok: [vmx2] => {
    "changed": false,
    "msg": "Current filesystem  /dev/gpt/junos is at 17G"
}
ok: [vmx3] => {
    "changed": false,
    "msg": "Current filesystem  /dev/gpt/junos is at 17G"
}

PLAY RECAP *************************************************************************************************************************************************************************************************
vmx1                       : ok=6    changed=0    unreachable=0    failed=0
vmx2                       : ok=6    changed=0    unreachable=0    failed=0
vmx3                       : ok=6    changed=0    unreachable=0    failed=0

```

Looks like everything passed and is in a good state, but what if the file system reaches a level above the specified amount?

##### Step 9

Let's make a change on the `set_fact` module, change the variable `percent` to `60` and comment out the original variable.

```yaml

      - name: CREATE NEW VARIABLES
        set_fact:
          #percent: "{{ output['stdout'][0]['system-storage-information'][0]['filesystem'][0]['used-percent'][0]['data'] }}"
          percent: "60"
          filesystem: "{{ output['stdout'][0]['system-storage-information'][0]['filesystem'][0]['filesystem-name'][0]['data'] }}"
          blocks: "{{ output['stdout'][0]['system-storage-information'][0]['filesystem'][0]['available-blocks'][0]['data'] }}"
          storage: "{{ output['stdout'][0]['system-storage-information'][0]['filesystem'][0]['available-blocks'][0]['attributes']['junos:format'] }}"
```


Execute the playbook and view results. Notice that the assertion failed and returned the msg stored in `fail_msg` parameter. 


```commandline

ntc@ntc-training:ansible$ ansible-playbook -i inventory compliance.yml   

.... output omitted ....

TASK [CHECK STORAGE FILESYSTEM PERCENT] ********************************************************************************************************************************************************************
fatal: [vmx1]: FAILED! => {
    "assertion": "percent | int  <= 50",
    "changed": false,
    "evaluated_to": false,
    "msg": "Warning!! filesystem /dev/gpt/junos is at 60%"
}

fatal: [vmx2]: FAILED! => {
    "assertion": "percent | int  <= 50",
    "changed": false,
    "evaluated_to": false,
    "msg": "Warning!! filesystem /dev/gpt/junos is at 60%"
}

fatal: [vmx3]: FAILED! => {
    "assertion": "percent | int  <= 50",
    "changed": false,
    "evaluated_to": false,
    "msg": "Warning!! filesystem /dev/gpt/junos is at 60%"
}

PLAY RECAP *************************************************************************************************************************************************************************************************
vmx1                       : ok=4    changed=0    unreachable=0    failed=1
vmx2                       : ok=4    changed=0    unreachable=0    failed=1
vmx3                       : ok=4    changed=0    unreachable=0    failed=1

```

Another thing to point out is that the assertions stopped being analyzed after the first task and did not run the second task because the module returned with an error. 

To prevent that from happening you can add the argument `ignore_errors: true` and it will ignore any errors and move on to the next task. 

##### Step 10

Add the `ignore_errors: true` argument to the end of the task. 


```yaml

      - name: CHECK STORAGE FILESYSTEM PERCENT
        assert:
          that:
           - "percent | int  <= 50"
          fail_msg: "Warning!! filesystem {{ filesystem }} is at {{ percent }}%"
          success_msg: "Current filesystem  {{ filesystem }} is at {{ percent }}%"
        ignore_errors: true
        

      - name: CHECK STORAGE FILESYSTEM AVAILABILITY
        assert:
          that:
           - "blocks | int >= 4194304"
          fail_msg: "Warning!! filesystem {{ filesystem }} is at {{ storage }}"
          success_msg: "Current filesystem  {{ filesystem }} is at {{ storage }}"
        ignore_errors: true

```

##### Step 11

Execute the playbook and view results.

```commandline

ntc@ntc-training:ansible$ ansible-playbook -i inventory compliance.yml   

.... output omitted ....

TASK [CREATE NEW VARIABLES] ********************************************************************************************************************************************************************************
ok: [vmx1]
ok: [vmx2]
ok: [vmx3]

TASK [VIEW DATA STORED IN NEW VARIABLES] *******************************************************************************************************************************************************************
ok: [vmx1] => {
    "msg": "Percent: 60%,  filesystem: /dev/gpt/junos, Blocks: 36045584, Storage: 17G"
}
ok: [vmx2] => {
    "msg": "Percent: 60%,  filesystem: /dev/gpt/junos, Blocks: 36045584, Storage: 17G"
}
ok: [vmx3] => {
    "msg": "Percent: 60%,  filesystem: /dev/gpt/junos, Blocks: 36045584, Storage: 17G"
}

TASK [CHECK STORAGE FILESYSTEM PERCENT] ********************************************************************************************************************************************************************
fatal: [vmx1]: FAILED! => {
    "assertion": "percent | int  <= 50",
    "changed": false,
    "evaluated_to": false,
    "msg": "Warning!! filesystem /dev/gpt/junos is at 60%"
}
...ignoring

fatal: [vmx2]: FAILED! => {
    "assertion": "percent | int  <= 50",
    "changed": false,
    "evaluated_to": false,
    "msg": "Warning!! filesystem /dev/gpt/junos is at 60%"
}
...ignoring

fatal: [vmx3]: FAILED! => {
    "assertion": "percent | int  <= 50",
    "changed": false,
    "evaluated_to": false,
    "msg": "Warning!! filesystem /dev/gpt/junos is at 60%"
}
...ignoring

TASK [CHECK STORAGE FILESYSTEM AVAILABILITY] ****************************************************************************************************************************************************************
ok: [vmx1] => {
    "changed": false,
    "msg": "Current filesystem  /dev/gpt/junos is at 17G"
}

ok: [vmx2] => {
    "changed": false,
    "msg": "Current filesystem  /dev/gpt/junos is at 17G"
}

ok: [vmx3] => {
    "changed": false,
    "msg": "Current filesystem  /dev/gpt/junos is at 17G"
}

PLAY RECAP *************************************************************************************************************************************************************************************************
vmx1                       : ok=6    changed=0    unreachable=0    failed=0
vmx2                       : ok=6    changed=0    unreachable=0    failed=0
vmx3                       : ok=6    changed=0    unreachable=0    failed=0
```

##### Status Check

Full and final playbook will look like this:

```yaml

---

  - name: IOS COMPLIANCE
    hosts: iosxe
    connection: network_cli
    gather_facts: no
    tags: ios


    tasks:

      - name: IOS show version
        ios_command:
          commands:
            - show version
        register: output

      - name: CHECK OS AND CONFIG REGISTER
        assert:
          that:
           - "'17.01.01' in output['stdout'][0]"
           - "'0x2102' in output['stdout'][0]"


  - name: JUNOS COMPLIANCE
    hosts: vmx
    connection: netconf
    gather_facts: no
    tags: vmx


    tasks:

      - name: JUNOS show version
        junos_command:
          commands:
            - show system storage
          display: json
        register: output


      - name: VIEW JSON DATA
        debug:
          var: output

      - name: CREATE NEW VARIABLES
        set_fact:
           #percent: "{{ output['stdout'][0]['system-storage-information'][0]['filesystem'][0]['used-percent'][0]['data'] }}"
           percent: "60"
           filesystem: "{{ output['stdout'][0]['system-storage-information'][0]['filesystem'][0]['filesystem-name'][0]['data'] }}"
           blocks: "{{ output['stdout'][0]['system-storage-information'][0]['filesystem'][0]['available-blocks'][0]['data'] }}"
           storage: "{{ output['stdout'][0]['system-storage-information'][0]['filesystem'][0]['available-blocks'][0]['attributes']['junos:format'] }}"


      - name: VIEW DATA STORED IN NEW VARIABLES
        debug:
          msg: "Percent: {{ percent }}%,  filesystem: {{ filesystem }}, Blocks: {{ blocks }}, Storage: {{ storage }}"


      - name: CHECK STORAGE FILESYSTEM PERCENT
        assert:
          that:
           - "percent | int  <= 50"
          fail_msg: "Warning!! filesystem {{ filesystem }} is at {{ percent }}%"
          success_msg: "Current filesystem  {{ filesystem }} is at {{ percent }}%"
        ignore_errors: true
        

      - name: CHECK STORAGE FILESYSTEM AVAILABILITY
        assert:
          that:
           - "blocks | int >= 4194304"
          fail_msg: "Warning!! filesystem {{ filesystem }} is at {{ storage }}"
          success_msg: "Current filesystem  {{ filesystem }} is at {{ storage }}"
        ignore_errors: true



```
