
# Bonus Lab 2 - Generating a Report for OS Compliance



Add a variable called `supported_os_versions` to `group_vars/all.yml`.  It should look like this:

```yaml
supported_os_versions:
  junos:
    - 15.1F4.15
    - 18.1
  eos:
    - 4.17
  ios:
    - 16.6.2
  nxos:
    - 7.3

```

Your goal is to generate reports that check to see if the actual real-time OS version is compliant, e.g. check to see if it's one of your supported OS versions (in the YAML data).

You should generate both of the following reports.  One is a text report and one is a CSV based report.

### HINT: make sure you did Lab 20.



### Text Report

```
---

Hostname:      vmx1
Model:         vmx
OS Version:    15.1F4.15
Compliant (Pass/Fail): Pass

---

Hostname:      vmx2
Model:         vmx
OS Version:    15.1F4.15
Compliant (Pass/Fail): Pass

---

Hostname:      vmx3
Model:         vmx
OS Version:    15.1F4.15
Compliant (Pass/Fail): Pass

---

Hostname:      eos-leaf1
Model:         vEOS
OS Version:    4.20.0F-7058194.bloomingtonrel (engineering build)
Compliant (Pass/Fail): Fail

---

Hostname:      eos-leaf2
Model:         vEOS
OS Version:    4.20.0F-7058194.bloomingtonrel (engineering build)
Compliant (Pass/Fail): Fail

---

Hostname:      eos-spine1
Model:         vEOS
OS Version:    4.20.0F-7058194.bloomingtonrel (engineering build)
Compliant (Pass/Fail): Fail

---

Hostname:      eos-spine2
Model:         vEOS
OS Version:    4.20.0F-7058194.bloomingtonrel (engineering build)
Compliant (Pass/Fail): Fail

```

### CSV Report

```
Hostname,Model,OS Version,Compliance
eos-leaf1,vEOS,4.20.0F-7058194.bloomingtonrel (engineering build),Fail
eos-leaf2,vEOS,4.20.0F-7058194.bloomingtonrel (engineering build),Fail
eos-spine1,vEOS,4.20.0F-7058194.bloomingtonrel (engineering build),Fail
eos-spine2vEOS,4.20.0F-7058194.bloomingtonrel (engineering build),Fail
vmx1,junos,15.1F4.15,Pass
vmx2,junos,15.1F4.15,Pass
vmx3,junos,15.1F4.15,Pass
```
