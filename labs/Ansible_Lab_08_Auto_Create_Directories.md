```---

  - name: Auto Generate Files and Directories
    hosts: all
    connection: local
    gather_facts: no

    tasks:

      - name: CREATE DIRECTORIES BASED ON OS
        file:
          path: ./{{ ansible_network_os }}/
          state: directory

      - name: CREATE SNMP.CONF FILE
        file:
          path: ./{{ ansible_network_os }}/snmp.conf
          state: touch 

      - name: CREATE TEMPLATES DIRECTORIES
        file:
          path: ./templates/
          state: directory

      - name: CREATE JINJA2 FILES
        file:
          path: ./templates/{{ ansible_network_os }}-snmp.j2
          state: touch``` 

```

```
├── eos
│   └── snmp.conf
├── file_module.yml
├── inventory
├── ios
│   └── snmp.conf
├── junos
│   └── snmp.conf
├── nxos
│   └── snmp.conf
├── templates
│   ├── eos-snmp.j2
│   ├── ios-snmp.j2
│   ├── junos-snmp.j2
│   └── nxos-snmp.j2

```