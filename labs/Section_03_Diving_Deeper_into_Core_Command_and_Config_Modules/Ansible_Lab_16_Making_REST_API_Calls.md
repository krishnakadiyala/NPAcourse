# Lab 16 - Making REST API Calls from Ansible

This lab shows how you can make HTTP-based API calls from Ansible.  We'll look at making API calls to IOS-XE and NX-OS based systems using RESTCONF and NX-API, respectively, on those systems.

### Task 1 - Using the IOS-XE API

This task will query Cisco IOS-XE routers for their GigE1 IP using the RESTCONF API available in 16.6 and later.

##### Step 1

SSH into `csr2` and apply the following changes:

```
!
interface GigabitEthernet2
 ip address 10.1.13.1 255.255.255.0
!
```


##### Step 2

Create a playbook called `rest-apis.yml` and insert the following into it:

```yaml

---

  - name: PLAY 1 - ISSUE API CALL TO CSR
    hosts: csr2
    connection: local
    gather_facts: no
    tags: ios

    tasks:

      - name: GET INTERFACE IP ADDRESS
        uri:
          url: https://{{ inventory_hostname }}/restconf/data/Cisco-IOS-XE-native:native/interface=GigabitEthernet/2/ip/address
          method: GET
          user: "{{ ansible_user }}"
          password: "{{ ansible_ssh_pass }}"
          return_content: yes
          validate_certs: no
          headers:
            Content-Type: application/yang-data+json
            Accept: application/yang-data+json
        register: response

      - debug:
          var: response
```

##### Step 3

Save and execute the playbook.

Do you see the API response?

##### Step 4

You should see there is a `content` key inside `response` that contains the actual response we need.  Let's print just the `content` data now.

Add a new debug statement to the playbook:

```yaml

---

  - name: PLAY 1 - ISSUE API CALL TO CSR
    hosts: csr2
    connection: local
    gather_facts: no
    tags: ios

    tasks:

      - name: GET INTERFACE IP ADDRESS
        uri:
          url: https://{{ inventory_hostname }}/restconf/data/Cisco-IOS-XE-native:native/interface=GigabitEthernet/2/ip/address
          method: GET
          user: "{{ ansible_user }}"
          password: "{{ ansible_ssh_pass }}"
          return_content: yes
          validate_certs: no
          headers:
            Content-Type: application/yang-data+json
            Accept: application/yang-data+json
        register: response

      - debug:
          var: response

      - debug:
          var: response['content']
```


##### Step 5

Execute the playbook.

You should see this response for the new task.

```
ok: [csr2] => {
    "response['content']": {
        "Cisco-IOS-XE-native:address": {
            "primary": {
                "address": "10.1.13.1",
                "mask": "255.255.255.0"
            }
        }
    }
}
```


##### Step 6

Try parsing the object to debug Primary IP address.

```yaml
      - debug:
          var: response['content']['Cisco-IOS-XE-native:address']['primary']['address']
```

Does it work?

You should see this response:

```
TASK [debug] *******************************************************************
ok: [csr2] => {
    "response['content']['Cisco-IOS-XE-native:address']['primary']['address']": "VARIABLE IS NOT DEFINED!"
}
```

This is not working because remember HTTP API responses come back as a JSON string.  

**We need to convert it to be a dictionary.**

##### Step 7

Remove the debug task you just added.

##### Step 8

Add the following tasks to convert the JSON string to a dictionary and then debug the IP address:

> Note: take note of the `from_json` Jinja2 filter.  This is doing what `json.loads()` does in Python when using the Python `requests` library.

```yaml
      - set_fact:
          ip_info: "{{ response['content'] | from_json }}"

      - debug:
          var: ip_info['Cisco-IOS-XE-native:address']['primary']['address']
```

##### Step 9

Save and execute the playbook.

You should see this output:

```
TASK [set_fact] ****************************************************************
ok: [csr2]

TASK [debug] *******************************************************************
ok: [csr2] => {
    "ip_info['Cisco-IOS-XE-native:address']['primary']['address']": "10.1.13.1"
}
```

##### Step 10 (Optional)

Add a task to make it easier to access the IP address using the `set_fact` module.  Then debug it.

```yaml
      - set_fact:
          ipaddr: "{{ ip_info['Cisco-IOS-XE-native:address']['primary']['address'] }}"

      - debug:
          var: ipaddr
```

Save and re-run the playbook.

This is the full output you should see:

```
ntc@ntc-training:ansible$ ansible-playbook -i inventory rest-apis.yml --tags=ios

PLAY [PLAY 1 - ISSUE API CALL TO CSR] ******************************************

TASK [GET INTERFACE IP ADDRESS] ************************************************
ok: [csr2]

TASK [debug] *******************************************************************
ok: [csr2] => {
    "response": {
        "cache_control": "private, no-cache, must-revalidate, proxy-revalidate",
        "changed": false,
        "connection": "close",
        "content": "{\n  \"Cisco-IOS-XE-native:address\": {\n    \"primary\": {\n      \"address\": \"10.1.13.1\",\n      \"mask\": \"255.255.255.0\"\n    }\n  }\n}\n",
        "content_type": "application/yang-data+json",
        "cookies": {},
        "cookies_string": "",
        "date": "Sun, 02 Dec 2018 12:37:38 GMT",
        "failed": false,
        "json": {
            "Cisco-IOS-XE-native:address": {
                "primary": {
                    "address": "10.1.13.1",
                    "mask": "255.255.255.0"
                }
            }
        },
        "msg": "OK (unknown bytes)",
        "pragma": "no-cache",
        "redirected": false,
        "server": "nginx",
        "status": 200,
        "transfer_encoding": "chunked",
        "url": "https://csr2/restconf/data/Cisco-IOS-XE-native:native/interface=GigabitEthernet/2/ip/address"
    }
}

TASK [debug] *******************************************************************
ok: [csr2] => {
    "response['content']": {
        "Cisco-IOS-XE-native:address": {
            "primary": {
                "address": "10.1.13.1",
                "mask": "255.255.255.0"
            }
        }
    }
}

TASK [set_fact] ****************************************************************
ok: [csr2]

TASK [debug] *******************************************************************
ok: [csr2] => {
    "ip_info['Cisco-IOS-XE-native:address']['primary']['address']": "10.1.13.1"
}

TASK [set_fact] ****************************************************************
ok: [csr2]

TASK [debug] *******************************************************************
ok: [csr2] => {
    "ipaddr": "10.1.13.1"
}

PLAY [PLAY 2 - ISSUE SHOW VERSION TO NEXUS VIA API] ****************************

PLAY RECAP *********************************************************************
csr2                       : ok=7    changed=0    unreachable=0    failed=0   

```

This is the full playbook:

```yaml

---

  - name: PLAY 1 - ISSUE API CALL TO CSR
    hosts: csr2
    connection: local
    gather_facts: no
    tags: ios

    tasks:

      - name: GET INTERFACE IP ADDRESS
        uri:
          url: https://{{ inventory_hostname }}/restconf/data/Cisco-IOS-XE-native:native/interface=GigabitEthernet/2/ip/address
          method: GET
          user: "{{ ansible_user }}"
          password: "{{ ansible_ssh_pass }}"
          return_content: yes
          validate_certs: no
          headers:
            Content-Type: application/yang-data+json
            Accept: application/yang-data+json
        register: response

      - debug:
          var: response

      - debug:
          var: response['content']

      - set_fact:
          ip_info: "{{ response['content'] | from_json }}"

      - debug:
          var: ip_info['Cisco-IOS-XE-native:address']['primary']['address']

      - set_fact:
          ipaddr: "{{ ip_info['Cisco-IOS-XE-native:address']['primary']['address'] }}"

      - debug:
          var: ipaddr
```



### Task 2 - Using the NXOS NX-API

##### Step 1

Add a NEW play in your EXISTING playbook.

This task is showing you can also do a HTTP POST passing a multi-line string within the `body` parameter. Take note of the `|` that permits this.

```yaml
  - name: PLAY 2 - ISSUE SHOW VERSION TO NEXUS VIA API
    hosts: nxos-spine1
    connection: local
    gather_facts: no
    tags: nxos

    tasks:

      - name: SHOW VERSION NEXUS API
        uri:
          url: https://nxos-spine1/ins
          method: POST
          user: "{{ ansible_user }}"
          password: "{{ ansible_ssh_pass }}"
          return_content: yes
          validate_certs: no
          body_format: json
          headers:
            Content-Type: application/json
            Accept: application/json
          body: |
            {
              "ins_api": {
                "version": "1.0",
                "type": "cli_show",
                "chunk": "0",
                "sid": "1",
                "input": "show version",
                "output_format": "json"
              }
            }
        register: response

      - debug:
          var: response

      - debug:
          var: response.content
```

##### Step 2

Save and execute the playbook using the "nxos" tag.

##### Step 3

Try debugging a few different variables from this object.


The full playbook is as follows:

```yaml

---

  - name: PLAY 1 - ISSUE API CALL TO CSR
    hosts: csr2
    connection: local
    gather_facts: no
    tags: ios

    tasks:

      - name: GET INTERFACE IP ADDRESS
        uri:
          url: https://{{ inventory_hostname }}/restconf/data/Cisco-IOS-XE-native:native/interface=GigabitEthernet/2/ip/address
          method: GET
          user: "{{ ansible_user }}"
          password: "{{ ansible_ssh_pass }}"
          return_content: yes
          validate_certs: no
          headers:
            Content-Type: application/yang-data+json
            Accept: application/yang-data+json
        register: response

      - debug:
          var: response

      - debug:
          var: response['content']

      - set_fact:
          ip_info: "{{ response['content'] | from_json }}"

      - debug:
          var: ip_info['Cisco-IOS-XE-native:address']['primary']['address']

      - set_fact:
          ipaddr: "{{ ip_info['Cisco-IOS-XE-native:address']['primary']['address'] }}"

      - debug:
          var: ipaddr


  - name: PLAY 2 - ISSUE SHOW VERSION TO NEXUS VIA API
    hosts: nxos-spine1
    connection: local
    gather_facts: no
    tags: nxos

    tasks:

      - name: SHOW VERSION NEXUS API
        uri:
          url: https://nxos-spine1/ins
          method: POST
          user: "{{ ansible_user }}"
          password: "{{ ansible_ssh_pass }}"
          return_content: yes
          body_format: json
          validate_certs: no
          headers:
            Content-Type: application/json
            Accept: application/json
          body: |
            {
              "ins_api": {
                "version": "1.0",
                "type": "cli_show",
                "chunk": "0",
                "sid": "1",
                "input": "show version",
                "output_format": "json"
              }
            }
        register: response


      - debug:
          var: response

      - debug:
          var: response.content
```
