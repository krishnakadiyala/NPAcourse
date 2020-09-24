# Lab 19 - Backup and Restore Network Configurations Part 1

Before starting the lab we are going to go over how to add 3rd party modules to your Ansible environment.  This could include open source modules or custom modules you decide to write over time. 

Below are some tips on how to do it, but for this lab environment it has already been added so we **don't** have to apply any changes.   This first Task is **read-only**.

### Task 1 - Adding 3rd Party Modules

##### Step 1

You need to perform two steps to start using 3rd party modules.

* Ensure the modules you want to use (usually a repository that has been cloned) is in your Ansible module search path
* Install any dependencies required by the modules (usually Python modules or packages installable via `pip`)

Issue the command `ansible --version`.  This will give us a wealth of information about our Ansible environment.

```commandline
ntc@ntc-training:~$ ansible --version
ansible 2.9.9
  config file = /etc/ansible/ansible.cfg
  configured module search path = ['/etc/ntc/ansible/library']
  ansible python module location = /usr/local/lib/python3.6/site-packages/ansible
  executable location = /usr/local/bin/ansible
  python version = 3.6.8 (default, Jun 11 2019, 01:16:11) [GCC 6.3.0 20170516]
```

You can note our configured module search path as `/etc/ntc/ansible/library`.  Ansible will recursively search for modules in that path now.

If you have a "default" or No search path shown, open the config file that is shown in the output above, in this example we have `/etc/ansible/ansible.cfg`.
In that file, you'll see these first few lines:

```commandline
  [defaults]

  # some basic default values...

  inventory      = /etc/ansible/hosts
  library        = ADD PATH HERE
```


##### Step 2

Add a path for library - this will become your search path. Validate it with `ansible --version` after you make the change. If you would like to add an additional path use `:` to add another path to the list.

```bash
[defaults]

# some basic default values...

inventory      = /etc/ansible/hosts
library        = /home/ntc/projects/:/etc/ntc/ansible/library
```

Save and exit the file.

```commandline
ntc@ntc-training:~$ ansible --version
ansible 2.9.9
  config file = /etc/ansible/ansible.cfg
  configured module search path = ['/etc/ntc/ansible/library']
  ansible python module location = /usr/local/lib/python3.6/site-packages/ansible
  executable location = /usr/local/bin/ansible
  python version = 3.6.8 (default, Jun 11 2019, 01:16:11) [GCC 6.3.0 20170516]
```

##### Step 3

You can now just `git clone` any git project that has modules inside your configured search path.

* It's recommended to follow the 3rd party module instructions to make sure it has met its dependencies requirements. What's important after the install is to make sure the libraries are in placed in where we have configured `configured module search path = [u'/etc/ntc/ansible/library', u'/home/ntc/projects']` of the `ansible.cfg` file.  Remember, you will need to ensure any Python dependencies are met too, e.g. `pip install $package`.


For the course, we have a number of repositories cloned that contain 3rd party open source Ansible modules:

```
ntc@ntc-training:~$ ls /etc/ntc/ansible/library/
ansible-junos-stdlib  ansible-pan  ansible-snmp  napalm  napalm-ansible  ntc-ansible
ntc@ntc-training:~$
```

Each one of these also required Python packages to be installed via `pip` including: `pyntc`, `napalm`, `ntc_templates`, `nelsnmp` just to name a few.

### Task 2 - Backup Configurations

This lab will show how to use Ansible to manage network device configurations and focuses on the process of backing up and re-storing full configuration files.

We'll use two main modules to do this:  one that is used to backup the configurations (ntc_show_command) in this lab and another that is used to deploy the configurations (NAPALM) in the next lab.

In this task, you will save and backup the current running configuration of all of your devices.

##### Step 1

Within the `ansible` directory, create a new directory called `backups`.

```
ntc@ntc-training:ansible$ mkdir backups
ntc@ntc-training:ansible$
```

> Note: you could also do this with the `file` module if you'd like so it's fully automated!

Additionally, in the same `ansible` directory, create a playbook called `backup.yml`

```
ntc@ntc-training:ansible$ touch backup.yml
ntc@ntc-training:ansible$
```

##### Step 2

Open the newly created playbook in your text editor.

Create a play that'll be executed against **all** hosts defined in the inventory file.

```yaml

---

  - name: BACKUP CONFIGURATIONS
    hosts: all
    connection: local
    gather_facts: no


```

> Note: most 3rd party modules use `connection: local` because the actual connection setup happens in the Python code within the module or dependencies for that module.

##### Step 3

Add a variable in your playbook called `backup_command`.  It should be a dictionary that contains 4 key-value pairs.  The keys should map to an OS and the value should be the command required to gather the existing running configuration.

```yaml

---

  - name: BACKUP CONFIGURATIONS
    hosts: all
    connection: local
    gather_facts: no

    vars:
      backup_command:
        eos: show run
        ios: show run
        nxos: show run
        junos: show configuration

```

By making an object like this, it'll allow us to use a single task to backup all configuration instead of needing a task/play per OS!


##### Step 4

Since we're using a 3rd party module, credentials and connection properties are handled a little differently.  We need to pass them into the module.

Add a variable to handle the login to the devices. Often referred to as a provider variable, this is a dictionary that can be passed to the `provider` parameter of the `ntc` and `napalm` modules.


```yaml

---

  - name: BACKUP CONFIGURATIONS
    hosts: all
    connection: local
    gather_facts: no

    vars:
      backup_command:
        eos: show run
        ios: show run
        nxos: show run
        junos: show configuration
      connection_details:
        username: "{{ ansible_user }}"
        password: "{{ ansible_ssh_pass }}"
        host: "{{ inventory_hostname }}"


```



##### Step 5

Add a task to backup the running configuration using the module called `ntc_show_command`.

Create a `backups` directory.

All backup files should be saved locally inside the `backups` directory.


```yaml

---

  - name: BACKUP CONFIGURATIONS
    hosts: all
    connection: local
    gather_facts: no

    vars:
      backup_command:
        eos: show run
        ios: show run
        nxos: show run
        junos: show configuration
      connection_details:
        username: "{{ ansible_user }}"
        password: "{{ ansible_ssh_pass }}"
        host: "{{ inventory_hostname }}"

    tasks:

      - name: BACKUP CONFIGS FOR ALL DEVICES
        ntc_show_command:
          provider: "{{ connection_details }}"
          command: "{{ backup_command[ansible_network_os] }}"
          local_file: "./backups/{{ inventory_hostname }}.cfg"
          platform: "{{ ntc_vendor }}_{{ ansible_network_os }}"
          

```

**Pay attention to how we are using variables for the `platform` parameter**.  

Supported platforms for this module actually matches anything Netmiko, a popular Python-based SSH library, supports, e.g. vendor_os like cisco_ios, cisco_nxos, juniper_junos, arista_eos, etc.  Since we have those variables pre-built in our inventory file, we can use them as defined in the output above.

Save and execute the playbook.

```
ntc@ntc-training:ansible$ ansible-playbook -i inventory backup.yml
```

You will see the following output during execution (this output doesn't include Nexus):

```
ntc@ntc-training:ansible$ ansible-playbook -i inventory backup.yml

PLAY [BACKUP] *************************************************************************************************

TASK [BACKUP CONFIGS] *****************************************************************************************
ok: [vmx1]
ok: [eos-spine2]
ok: [eos-leaf1]
ok: [eos-leaf2]
ok: [eos-spine1]
ok: [vmx2]
ok: [vmx3]
ok: [nxos-spine1]
ok: [nxos-spine2]
ok: [csr1]
ok: [csr2]
ok: [csr3]

PLAY RECAP ****************************************************************************************************
csr1                       : ok=1    changed=0    unreachable=0    failed=0   
csr2                       : ok=1    changed=0    unreachable=0    failed=0   
csr3                       : ok=1    changed=0    unreachable=0    failed=0   
eos-leaf1                  : ok=1    changed=0    unreachable=0    failed=0   
eos-leaf2                  : ok=1    changed=0    unreachable=0    failed=0   
eos-spine1                 : ok=1    changed=0    unreachable=0    failed=0   
eos-spine2                 : ok=1    changed=0    unreachable=0    failed=0   
nxos-spine1                : ok=1    changed=0    unreachable=0    failed=0   
nxos-spine2                : ok=1    changed=0    unreachable=0    failed=0   
vmx1                       : ok=1    changed=0    unreachable=0    failed=0   
vmx2                       : ok=1    changed=0    unreachable=0    failed=0   
vmx3                       : ok=1    changed=0    unreachable=0    failed=0   

ntc@ntc-training:ansible$

```

##### Step 6

Move to the `backups` directory and open the newly created files to verify everything worked as expected.  

Pay particular attention to the IOS configurations.  In these configurations, you'll see two lines at the top of each including:

* `Building configuration...`
* `Current configuration : 4043 bytes`

These CANNOT be included when we re-deploy them and push full configs back to each device.  This is not supported by IOS (you can try copying and pasting a full config from the CLI--you'll see this first hand)

We need an automated way to remove them from each.

##### Step 7

Add two tasks to cleanup the backup configs. While it's only relevant for IOS configs, there is no harm on running this against all devices.

```yaml

      # this goes below the existing tasks

      - name: CLEAN UP IOS CONFIGS - LINE 1
        lineinfile:
          dest: ./backups/{{ inventory_hostname }}.cfg
          line: "Building configuration..."
          state: absent
        tags: clean

      - name: CLEAN UP IOS CONFIGS - LINE 2
        lineinfile:
          dest: ./backups/{{ inventory_hostname }}.cfg
          regexp: "Current configuration .*"
          state: absent
        tags: clean
```

Notice how there are now tags embedded for each of these tasks.  This allows us to selectively run just these two tasks without having to run the backup task again.

##### Step 8


Save the playbook and run it again with the following command.

```
ntc@ntc-training:ansible$ $ ansible-playbook -i inventory backup.yml --tags=clean

```


Relevant output:

```

TASK [CLEAN UP IOS CONFIGS LINE 1] ******************************************************
ok: [vmx1]
ok: [eos-spine1]
ok: [eos-leaf1]
ok: [eos-leaf2]
ok: [eos-spine2]
ok: [vmx2]
changed: [csr2]
ok: [vmx3]
changed: [csr1]
changed: [csr3]

TASK [CLEAN UP IOS CONFIGS LINE 2] ******************************************************
ok: [eos-spine1]
ok: [eos-spine2]
ok: [eos-leaf2]
ok: [eos-leaf1]
ok: [vmx1]
ok: [vmx2]
changed: [csr1]
ok: [vmx3]
changed: [csr3]
changed: [csr2]
```

Open one or more of the new configuration files and take a look at them and notice how those lines are gone from the files.

##### Step 9

At the top of your playbook are two variables: `backup_command` and `connection_details`.  It's not great practice to keep variables hard-coded in your playbook as you cannot re-use them in other playbooks or areas of your project.

Re-locate both of these variables to `group_vars/all.yml`.

The final updated playbook should look like this:

```yaml

---

  - name: BACKUP CONFIGURATIONS
    hosts: all
    connection: local
    gather_facts: no

    tasks:

      - name: BACKUP CONFIGS FOR ALL DEVICES
        ntc_show_command:
          provider: "{{ connection_details }}"
          command: "{{ backup_command[ansible_network_os] }}"
          local_file: "./backups/{{ inventory_hostname }}.cfg"
          platform: "{{ ntc_vendor }}_{{ ansible_network_os }}"

      - name: CLEAN UP IOS CONFIGS - LINE 1
        lineinfile:
          dest: ./backups/{{ inventory_hostname }}.cfg
          line: "Building configuration..."
          state: absent
        tags: clean

      - name: CLEAN UP IOS CONFIGS - LINE 2
        lineinfile:
          dest: ./backups/{{ inventory_hostname }}.cfg
          regexp: "Current configuration .*"
          state: absent
        tags: clean


```

And `group_vars/all.yml` should now have both variables:

```yaml

---

backup_command:
  eos: show run
  ios: show run
  nxos: show run
  junos: show configuration
connection_details:
  username: "{{ ansible_user }}"
  password: "{{ ansible_ssh_pass }}"
  host: "{{ inventory_hostname }}"

```


Note: in other labs, you've also seen how you can back up configurations using "core" modules.  This is just another way while showing how to use 3rd party modules.
