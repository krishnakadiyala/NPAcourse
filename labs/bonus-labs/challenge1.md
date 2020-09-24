# Challenge 1

* Generate a report (markdown table or CSV file) for visualizing network reachability
* Use the `napalm_ping` module.  
* The goal is to visualize reachability in an easy to read documentation format.  
* Start with just one device type such as MX, then add in EOS.
* Columns for the markdown or CSV table should be "Device", "Destination", "Success Rate (%)", and "Status"

**Table/Column Details:**
* Device is basically inventory_hostname
* Destination will be whatever addresses are being pinged.
* Success Rate should be the % of successful requests 
* Status should be Pass if the success rate is >= 80%, else Fail.

EXAMPLE:

| Device | Destination | Success Rate | Status |
| :---: | :---: | :---: | :---: |
| eos-leaf1 | 10.1.254.101 | 100.0% | Success |
| eos-leaf1 | 10.1.254.109 | 100.0% | Success |
| eos-leaf2 | 10.1.254.105 | 100.0% | Success |
| eos-leaf2 | 10.1.254.113 | 100.0% | Success |
| eos-spine1 | 10.1.254.102 | 100.0% | Success |
| eos-spine1 | 10.1.254.106 | 100.0% | Success |
| eos-spine2 | 10.1.254.110 | 100.0% | Success |
| eos-spine2 | 10.1.254.114 | 100.0% | Success |

