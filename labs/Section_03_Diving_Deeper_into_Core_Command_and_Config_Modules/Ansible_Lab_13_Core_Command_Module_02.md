# Lab 13 Challenge - Issuing Ping Commands and Saving the Responses

This lab will have you ping a certain amount of destinations from _each_ Cisco CSR router.  

Each of the responses will then be stored in one or more files.  You can either store all responses in a single file or store the responses in individual files.

Create a new playbook called `ping.yml` in the `ansible` directory for this lab.

Start with this base playbook that includes the IP addresses that you need to ping:

```yaml

---

  - name: TEST REACHABILITY
    hosts: iosxe
    connection: network_cli
    gather_facts: no

    vars:
      target_ips:
        - "10.0.0.15"
        - "10.0.0.2"
        - "198.6.1.4"
```


The solution should output one of the following directory and file structures:

**Solution Option 1**

```
ntc@ntc-training:ansible$ tree ping-responses/
ping-responses
├── ping_results_from_csr1.txt
├── ping_results_from_csr2.txt
└── ping_results_from_csr3.txt

1 directory, 3 files

ntc@ntc-training:ansible$
```

**Solution Option 2**

```
ntc@ntc-training:ansible$ tree ping-responses/
ping-responses/
├── csr1
│   ├── to_198.6.1.4.txt
│   ├── to_10.0.0.2.txt
│   └── to_10.0.0.15.txt
├── csr2
│   ├── to_198.6.1.4.txt
│   ├── to_10.0.0.2.txt
│   └── to_10.0.0.15.txt
└── csr3
    ├── to_198.6.1.4.txt
    ├── to_10.0.0.2.txt
    └── to_10.0.0.15.txt

3 directories, 9 files
ntc@ntc-training:ansible$
```

## STOP SCROLLING - SOLUTIONS BELOW

```
.































































...





































...
```




### Solution Option 1


```yaml
---

  - name: TEST REACHABILITY - SOLUTION 1
    hosts: iosxe
    connection: network_cli
    gather_facts: no

    vars:
      target_ips:
        - "10.0.0.15"
        - "10.0.0.2"
        - "198.6.1.4"

    tasks:

      - name: ENSURE DIRECTORY FOR EACH DEVICE EXISTS
        file:
          path: ./ping-responses/
          state: directory

      - name: SEND PING COMMANDS TO DEVICES
        ios_command:
          commands: "ping {{ item }} repeat 2"
        register: ping_responses
        loop: "{{ target_ips }}"

      - name: VERIFY REGISTERED VARIABLE
        debug:
          var: ping_responses

      - name: TEST LOOPING OVER REGISTERED VARIABLE
        debug:
          var: "{{ item }}"
        loop: "{{ ping_responses.results }}"

      - name: SAVE OUTPUTS TO INDIVIDUAL FILES
        template:
          src: basic-copy-single.j2
          dest: ./ping-responses/ping_responses_from_{{ inventory_hostname }}.txt

```


**templates/basic-copy-single.j2**

```
{% for result in ping_responses.results %}
{{ result['stdout'][0] }}
{% endfor %}
```



### Solution Option 2


Playbook **ping.yml**

```yaml
---

  - name: TEST REACHABILITY - SOLUTION 2
    hosts: iosxe
    connection: network_cli
    gather_facts: no

    vars:
      target_ips:
        - "10.0.0.15"
        - "10.0.0.2"
        - "198.6.1.4"

    tasks:

      - name: ENSURE DIRECTORY FOR EACH DEVICE EXISTS
        file:
          path: ./ping-responses/{{ inventory_hostname }}/
          state: directory

      - name: SEND PING COMMANDS TO DEVICES
        ios_command:
          commands: "ping {{ item }} repeat 2"
        register: ping_responses
        loop: "{{ target_ips }}"

      - name: VERIFY REGISTERED VARIABLE
        debug:
          var: ping_responses

      - name: TEST LOOPING OVER REGISTERED VARIABLE
        debug:
          var: "{{ item }}"
        loop: "{{ ping_responses.results }}"

      - name: SAVE OUTPUTS TO INDIVIDUAL FILES
        template:
          src: basic-copy.j2
          dest: ./ping-responses/{{ inventory_hostname }}/to_{{ item.item }}.txt
        loop: "{{ ping_responses.results }}"
```

**templates/basic-copy.j2**

```
{{ item['stdout'][0] }}
```


