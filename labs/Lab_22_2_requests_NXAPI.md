# Lab 22.2 - Cisco NX-API

### Task 1 - Getting Started with the Python Requests Module

In this task, you will explore working with the Python requests module built to simplify working with HTTP-based (REST) APIs.

For this lab, you will use two Cisco Nexus switches.

##### Step 1

Verify you can ping the Cisco switches by name.  They have been pre-configured in your `/etc/hosts` file.

```
$ ping nxos-spine1
$ ping nxos-spine2
```

##### Step 2

Enter the Python shell.

```python
$ python

Python 3.6.8 (default, Jun 11 2019, 01:16:11)
[GCC 6.3.0 20170516] on linux
Type "help", "copyright", "credits" or "license" for more information.

>>>
```

##### Step 3

Import the `requests` module while on the Python shell.  In addition, import the object that simplified using authentication for REST APIs as well as the `json` module.

```python
>>> import requests
>>> from requests.auth import HTTPBasicAuth
>>> import json
>>>
```

##### Step 4

Use `help` on `requests`.  You will see a description of this Python package.

```python
>>> help(requests)

```

```
Help on package requests:

NAME
    requests

DESCRIPTION
    Requests HTTP Library
    ~~~~~~~~~~~~~~~~~~~~~

    Requests is an HTTP library, written in Python, for human beings. Basic GET
    usage:

       >>> import requests
       >>> r = requests.get('https://www.python.org')
       >>> r.status_code
       200
       >>> 'Python is a programming language' in str(r.content)
       True

    ... or POST:

       >>> payload = dict(key1='value1', key2='value2')
       >>> r = requests.post('https://httpbin.org/post', data=payload)
       >>> print(r.text)
       {
         ...
         "form": {
           "key2": "value2",
           "key1": "value1"
         },
         ...
       }

# output omitted

```


You can also do a `dir(requests)` to see available attributes and built-in methods.


##### Step 5

Navigate to the NX-API Sandbox.  

Set the message format to `json` and command type is `cli_show`.  Enter the command `show version` into the text box.

You should see the following Request object in the bottom left:

```python
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
```

This is the object we need to send to the device.  We'll use this in an upcoming step, so don't close the browser.

> You could also Press the "Python" button in the NX-API sandbox to give you a jump start, but we are doing things slightly different in this lab, so we won't use that code directly from the sandbox.


##### Step 6

Create four new variables while on the Python shell: `auth`, `headers`, `payload`, and `url`.

`auth` should be equal to `auth = HTTPBasicAuth('ntc', 'ntc123')`

`headers` should be equal to `headers = { 'Content-Type': 'application/json' }`

`payload` should be equal to the Request object you copied above as a dictionary.


`url` should be equal to `url = 'https://nxos-spine1/ins'` - this needs the `ins` appended to the switch name or IP to work.  


The summary up until this point is the following:

> Note: there is no need to format the dictionaries as shown below.  It is done for readability.  

```python
>>> import requests
>>> import json
>>> from requests.auth import HTTPBasicAuth
>>>
>>> auth = HTTPBasicAuth('ntc', 'ntc123')
>>> headers = {
...     'Content-Type': 'application/json'
... }
>>>
>>> payload = {
...     "ins_api": {
...         "version": "1.0",
...         "type": "cli_show",
...         "chunk": "0",
...         "sid": "1",
...         "input": "show version",
...         "output_format": "json"
...     }
... }
>>>
>>> url = 'https://nxos-spine1/ins'
>>>
```

At this point, we are ready to make a HTTP API call to the Nexus switch.  Remember the Nexus switch only supports HTTP POSTs even though we are _getting_ data back. This is why it's non-RESTful HTTP API.

##### Step 7

Make the API call to the device using the `post` function of `requests` as shown below.

```python
>>> response = requests.post(url, data=json.dumps(payload), headers=headers, auth=auth, verify=False)
/usr/local/lib/python3.6/site-packages/urllib3/connectionpool.py:986: InsecureRequestWarning: Unverified HTTPS request is being made to host 'nxos-spine1'. Adding certificate verification is strongly advised. See: https://urllib3.readthedocs.io/en/latest/advanced-usage.html#ssl-warnings
  InsecureRequestWarning,
>>>
```

The output of the above command is just a warning stating that certificate verification has been disabled, and it's recommended to enable it. Since this is only for testing, it can be disabled by using the following command:
```python
>>>
>>> requests.packages.urllib3.disable_warnings()
>>>
```

Executing the `POST` request again will not show the warning anymore. 

```python
>>>
>>> response = requests.post(url, data=json.dumps(payload), headers=headers, auth=auth, verify=False)
>>>
```

This made the API call and returned data back stored as response.

You can verify the type of response and see it's still a Requests object:

```python
>>> type(response)
<class 'requests.models.Response'>
>>>
```

##### Step 8

Let's explore key attributes of `response`.

First, let's validate the API call was successful.  If it was we should see an HTTP status code of "200" as the value for the `status_code`.

```python
>>> response.status_code
200
>>>
```

Now, let's see the actual response from the switch using the `text` attribute.

```python
>>> rsp = response.text
>>>
>>> type(rsp)
<class 'str'>
>>>
```


Now print out the `rsp` variable:

> Note: if you use the print statement, you actually can't tell it's a string. This is critical to understand because you may think it's a dictionary.


```python
>>> rsp
'{\n\t"ins_api":\t{\n\t\t"type":\t"cli_show",\n\t\t"version":\t"1.0",\n\t\t"sid":\t"eoc",\n\t\t"outputs":\t{\n\t\t\t"output":\t{\n\t\t\t\t"input":\t"show version",\n\t\t\t\t"msg":\t"Success",\n\t\t\t\t"code":\t"200",
\n\t\t\t\t"body":\t{\n\t\t\t\t\t"header_str":\t"Cisco Nexus Operating System (NX-OS) Software\\nTAC support: http://www.cisco.com/tac\\nDocuments: http://www.cisco.com/en/US/products/ps9372/tsd_products_support_series_home.
html\\nCopyright (c) 2002-2019, Cisco Systems, Inc. All rights reserved.\\nThe copyrights to certain works contained herein are owned by\\nother third parties and are used and distributed under license.\\nSome parts of this software
are covered under the GNU Public\\nLicense. A copy of the license is available at\\nhttp://www.gnu.org/licenses/gpl.html.\\n\\nNexus 9000v is a demo version of the Nexus Operating System\\n",\n\t\t\t\t\t"bios_ver_str":\t"",
\n\t\t\t\t\t"kickstart_ver_str":\t"9.3(3)",\n\t\t\t\t\t"nxos_ver_str":\t"9.3(3)",\n\t\t\t\t\t"bios_cmpl_time":\t"",\n\t\t\t\t\t"kick_file_name":\t"bootflash:///nxos.9.3.3.bin",\n\t\t\t\t\t"nxos_file_name":\t"bootflash:///nxos.9.3.3.
bin",\n\t\t\t\t\t"kick_cmpl_time":\t"12/22/2019 2:00:00",\n\t\t\t\t\t"nxos_cmpl_time":\t"12/22/2019 2:00:00",\n\t\t\t\t\t"kick_tmstmp":\t"12/22/2019 14:00:37",\n\t\t\t\t\t"nxos_tmstmp":\t"12/22/2019 14:00:37",
\n\t\t\t\t\t"chassis_id":\t"Nexus9000 C9300v Chassis",\n\t\t\t\t\t"cpu_name":\t"",\n\t\t\t\t\t"memory":\t6097044,\n\t\t\t\t\t"mem_type":\t"kB",\n\t\t\t\t\t"proc_board_id":\t"98IAC051ND7",\n\t\t\t\t\t"host_name":\t"nxos-spine1",
\n\t\t\t\t\t"bootflash_size":\t4287040,\n\t\t\t\t\t"kern_uptm_days":\t0,\n\t\t\t\t\t"kern_uptm_hrs":\t3,\n\t\t\t\t\t"kern_uptm_mins":\t28,\n\t\t\t\t\t"kern_uptm_secs":\t6,\n\t\t\t\t\t"rr_reason":\t"Unknown",
\n\t\t\t\t\t"rr_sys_ver":\t"",\n\t\t\t\t\t"rr_service":\t"",\n\t\t\t\t\t"plugins":\t"Core Plugin, Ethernet Plugin",\n\t\t\t\t\t"manufacturer":\t"Cisco Systems, Inc.",\n\t\t\t\t\t"TABLE_package_list":\t
{\n\t\t\t\t\t\t"ROW_package_list":\t{\n\t\t\t\t\t\t\t"package_id":\t""\n\t\t\t\t\t\t}\n\t\t\t\t\t}\n\t\t\t\t}\n\t\t\t}\n\t\t}\n\t}\n}'
>>>

```

Try also printing it with the `print` statement.

```python
>>>
>>> print(rsp)
{
	"ins_api":	{
		"type":	"cli_show",
		"version":	"1.0",
		"sid":	"eoc",
		"outputs":	{
			"output":	{
				"input":	"show version",
				"msg":	"Success",
				"code":	"200",
				"body":	{
					"header_str":	"Cisco Nexus Operating System (NX-OS) Software\nTAC support: http://www.cisco.com/tac\nDocuments: http://www.cisco.com/en/US/products/ps9372/tsd_products_support_series_home.html\nCopyright (c) 2002-2019, Cisco Systems, Inc. All rights reserved.\nThe copyrights to certain works contained herein are owned by\nother third parties and are used and distributed under license.\nSome parts of this software are covered under the GNU Public\nLicense. A copy of the license is available at\nhttp://www.gnu.org/licenses/gpl.html.\n\nNexus 9000v is a demo version of the Nexus Operating System\n",
					"bios_ver_str":	"",
					"kickstart_ver_str":	"9.3(3)",
					"nxos_ver_str":	"9.3(3)",
					"bios_cmpl_time":	"",
					"kick_file_name":	"bootflash:///nxos.9.3.3.bin",
					"nxos_file_name":	"bootflash:///nxos.9.3.3.bin",
					"kick_cmpl_time":	"12/22/2019 2:00:00",
					"nxos_cmpl_time":	"12/22/2019 2:00:00",
					"kick_tmstmp":	"12/22/2019 14:00:37",
					"nxos_tmstmp":	"12/22/2019 14:00:37",
					"chassis_id":	"Nexus9000 C9300v Chassis",
					"cpu_name":	"",
					"memory":	6097044,
					"mem_type":	"kB",
					"proc_board_id":	"98IAC051ND7",
					"host_name":	"nxos-spine1",
					"bootflash_size":	4287040,
					"kern_uptm_days":	0,
					"kern_uptm_hrs":	3,
					"kern_uptm_mins":	28,
					"kern_uptm_secs":	6,
					"rr_reason":	"Unknown",
					"rr_sys_ver":	"",
					"rr_service":	"",
					"plugins":	"Core Plugin, Ethernet Plugin",
					"manufacturer":	"Cisco Systems, Inc.",
					"TABLE_package_list":	{
						"ROW_package_list":	{
							"package_id":	""
						}
					}
				}
			}
		}
	}
}
>>>
```

##### Step 9

Load the response **JSON string** and convert it to a dictionary:

```python
>>> data = json.loads(response.text)
>>>
```

##### Step 10

Perform a type check:

```python
>>> type(data)
<class 'dict'>
>>>
```

##### Step 11

Print the dictionary using `json.dumps`:

```python
>>> print(json.dumps(data, indent=4))
{
    "ins_api": {
        "type": "cli_show",
        "version": "1.0",
        "sid": "eoc",
        "outputs": {
            "output": {
                "input": "show version",
                "msg": "Success",
                "code": "200",
                "body": {
                    "header_str": "Cisco Nexus Operating System (NX-OS) Software\nTAC support: http://www.cisco.com/tac\nDocuments: http://www.cisco.com/en/US/products/ps9372/tsd_products_support_series_home.html\nCopyright (c) 2002-2019, Cisco Systems, Inc. All rights reserved.\nThe copyrights to certain works contained herein are owned by\nother third parties and are used and distributed under license.\nSome parts of this software are covered under the GNU Public\nLicense. A copy of the license is available at\nhttp://www.gnu.org/licenses/gpl.html.\n\nNexus 9000v is a demo version of the Nexus Operating System\n",
                    "bios_ver_str": "",
                    "kickstart_ver_str": "9.3(3)",
                    "nxos_ver_str": "9.3(3)",
                    "bios_cmpl_time": "",
                    "kick_file_name": "bootflash:///nxos.9.3.3.bin",
                    "nxos_file_name": "bootflash:///nxos.9.3.3.bin",
                    "kick_cmpl_time": "12/22/2019 2:00:00",
                    "nxos_cmpl_time": "12/22/2019 2:00:00",
                    "kick_tmstmp": "12/22/2019 14:00:37",
                    "nxos_tmstmp": "12/22/2019 14:00:37",
                    "chassis_id": "Nexus9000 C9300v Chassis",
                    "cpu_name": "",
                    "memory": 6097044,
                    "mem_type": "kB",
                    "proc_board_id": "98IAC051ND7",
                    "host_name": "nxos-spine1",
                    "bootflash_size": 4287040,
                    "kern_uptm_days": 0,
                    "kern_uptm_hrs": 3,
                    "kern_uptm_mins": 28,
                    "kern_uptm_secs": 6,
                    "rr_reason": "Unknown",
                    "rr_sys_ver": "",
                    "rr_service": "",
                    "plugins": "Core Plugin, Ethernet Plugin",
                    "manufacturer": "Cisco Systems, Inc.",
                    "TABLE_package_list": {
                        "ROW_package_list": {
                            "package_id": ""
                        }
                    }
                }
            }
        }
    }
}
>>>
```

##### Step 12

Print the name of the kickstart image.

```python
>>> print(data['ins_api']['outputs']['output']['body']['kickstart_ver_str'])
9.3(3)
>>>
```

##### Step 13

Extract everything from `body` in a variable first and then print the kickstart image again.

```python
>>> body = data['ins_api']['outputs']['output']['body']
>>>
>>> print(body.get('kickstart_ver_str'))
9.3(3)
>>>
```

Saving everything under `body` as its own variable streamlines accessing data if you need to extract multiple key-value pairs.


##### Step 14

Use the command `show vlan brief` to get all vlans back from the device.

Print the JSON object using `json.dumps` out when complete.

```python
>>> payload = {
...     "ins_api": {
...         "version": "1.0",
...         "type": "cli_show",
...         "chunk": "0",
...         "sid": "1",
...         "input": "show vlan brief",
...         "output_format": "json"
...     }
... }
>>>
>>> response = requests.post(url, data=json.dumps(payload), headers=headers, auth=auth, verify=False)
>>>
>>> data = json.loads(response.text)
>>>
>>> print(json.dumps(data, indent=4))
{
    "ins_api": {
        "type": "cli_show",
        "version": "1.0",
        "sid": "eoc",
        "outputs": {
            "output": {
                "input": "show vlan brief",
                "msg": "Success",
                "code": "200",
                "body": {
                    "TABLE_vlanbriefxbrief": {
                        "ROW_vlanbriefxbrief": {
                            "vlanshowbr-vlanid": "1",
                            "vlanshowbr-vlanid-utf": "1",
                            "vlanshowbr-vlanname": "default",
                            "vlanshowbr-vlanstate": "active",
                            "vlanshowbr-shutstate": "noshutdown",
                            "vlanshowplist-ifidx": "Ethernet1/1,Ethernet1/2,Ethernet1/3,Ethernet1/4,Ethernet1/5,Ethernet1/6,Ethernet1/7,Ethernet1/8,Ethernet1/9,Ethernet1/10,Ethernet1/11,Ethernet1/12,Ethernet1/13,Ethernet1/14,Ethernet1/15,Ethernet1/16,Ethernet1/17,Ethernet1/18,Ethernet1/19,Ethernet1/20,Ethernet1/21,Ethernet1/22,Ethernet1/23,Ethernet1/24,Ethernet1/25,Ethernet1/26,Ethernet1/27,Ethernet1/28,Ethernet1/29,Ethernet1/30,Ethernet1/31,Ethernet1/32,Ethernet1/33,Ethernet1/34,Ethernet1/35,Ethernet1/36,Ethernet1/37,Ethernet1/38,Ethernet1/39,Ethernet1/40,Ethernet1/41,Ethernet1/42,Ethernet1/43,Ethernet1/44,Ethernet1/45,Ethernet1/46,Ethernet1/47,Ethernet1/48,Ethernet1/49,Ethernet1/50,Ethernet1/51,Ethernet1/52,Ethernet1/53,Ethernet1/54,Ethernet1/55,Ethernet1/56,Ethernet1/57,Ethernet1/58,Ethernet1/59,Ethernet1/60,Ethernet1/61,Ethernet1/62,Ethernet1/63,Ethernet1/64"
                        }
                    }
                }
            }
        }
    }
}
>>>
>>>

```

##### Step 15

Save the VLAN object (everything under body) as a new variable called `vlans`.

```python
>>> vlans = data['ins_api']['outputs']['output']['body']
>>>
>>> print(json.dumps(vlans, indent=4))
{
    "TABLE_vlanbriefxbrief": {
        "ROW_vlanbriefxbrief": {
            "vlanshowbr-vlanid": "1",
            "vlanshowbr-vlanid-utf": "1",
            "vlanshowbr-vlanname": "default",
            "vlanshowbr-vlanstate": "active",
            "vlanshowbr-shutstate": "noshutdown",
            "vlanshowplist-ifidx": "Ethernet1/1,Ethernet1/2,Ethernet1/3,Ethernet1/4,Ethernet1/5,Ethernet1/6,Ethernet1/7,Ethernet1/8,Ethernet1/9,Ethernet1/10,Ethernet1/11,Ethernet1/12,Ethernet1/13,Ethernet1/14,Ethernet1/15,Ethernet1/16,Ethernet1/17,Ethernet1/18,Ethernet1/19,Ethernet1/20,Ethernet1/21,Ethernet1/22,Ethernet1/23,Ethernet1/24,Ethernet1/25,Ethernet1/26,Ethernet1/27,Ethernet1/28,Ethernet1/29,Ethernet1/30,Ethernet1/31,Ethernet1/32,Ethernet1/33,Ethernet1/34,Ethernet1/35,Ethernet1/36,Ethernet1/37,Ethernet1/38,Ethernet1/39,Ethernet1/40,Ethernet1/41,Ethernet1/42,Ethernet1/43,Ethernet1/44,Ethernet1/45,Ethernet1/46,Ethernet1/47,Ethernet1/48,Ethernet1/49,Ethernet1/50,Ethernet1/51,Ethernet1/52,Ethernet1/53,Ethernet1/54,Ethernet1/55,Ethernet1/56,Ethernet1/57,Ethernet1/58,Ethernet1/59,Ethernet1/60,Ethernet1/61,Ethernet1/62,Ethernet1/63,Ethernet1/64"            
        }
    }
}
>>>
```

##### Step 16

**If you see more than VLAN 1 on the switch, manually SSH into nxos-spine1 and remove them.**

Print out the vlan name for VLAN 1.

```python
>>> print(vlans['TABLE_vlanbriefxbrief']['ROW_vlanbriefxbrief']['vlanshowbr-vlanname'])
default
```

You should see that this is quite the nested dictionary and the work from Module 1 is extremely helpful for working with REST APIs returning JSON data.

##### Step 17

SSH back into the switch and add VLAN 10.

##### Step 18

Re-issue the same API call and re-create the `vlans` variable.

```python
>>> response = requests.post(url, data=json.dumps(payload), headers=headers, auth=auth, verify=False)
>>>
>>> data = json.loads(response.text)
>>>
>>> vlans = data['ins_api']['outputs']['output']['body']
>>>
```

The same steps worked so far.

##### Step 19

Now print the name for VLAN 1.

```python
>>> print(vlans['TABLE_vlanbriefxbrief']['ROW_vlanbriefxbrief']['vlanshowbr-vlanname'])
### output omitted
```

Did it work?  

Print out `vlans` on its own:

```python
>>> print(json.dumps(vlans, indent=4))
{
    "TABLE_vlanbriefxbrief": {
        "ROW_vlanbriefxbrief": [
            {
                "vlanshowbr-vlanid": "1",
                "vlanshowbr-vlanid-utf": "1",
                "vlanshowbr-vlanname": "default",
                "vlanshowbr-vlanstate": "active",
                "vlanshowbr-shutstate": "noshutdown",
                "vlanshowplist-ifidx": "Ethernet1/1,Ethernet1/2,Ethernet1/3,Ethernet1/4,Ethernet1/5,Ethernet1/6,Ethernet1/7,Ethernet1/8,Ethernet1/9,Ethernet1/10,Ethernet1/11,Ethernet1/12,Ethernet1/13,Ethernet1/14,Ethernet1/15,Ethernet1/16,Ethernet1/17,Ethernet1/18,Ethernet1/19,Ethernet1/20,Ethernet1/21,Ethernet1/22,Ethernet1/23,Ethernet1/24,Ethernet1/25,Ethernet1/26,Ethernet1/27,Ethernet1/28,Ethernet1/29,Ethernet1/30,Ethernet1/31,Ethernet1/32,Ethernet1/33,Ethernet1/34,Ethernet1/35,Ethernet1/36,Ethernet1/37,Ethernet1/38,Ethernet1/39,Ethernet1/40,Ethernet1/41,Ethernet1/42,Ethernet1/43,Ethernet1/44,Ethernet1/45,Ethernet1/46,Ethernet1/47,Ethernet1/48,Ethernet1/49,Ethernet1/50,Ethernet1/51,Ethernet1/52,Ethernet1/53,Ethernet1/54,Ethernet1/55,Ethernet1/56,Ethernet1/57,Ethernet1/58,Ethernet1/59,Ethernet1/60,Ethernet1/61,Ethernet1/62,Ethernet1/63,Ethernet1/64"
            },
            {
                "vlanshowbr-vlanid": "10",
                "vlanshowbr-vlanid-utf": "10",
                "vlanshowbr-vlanname": "VLAN0010",
                "vlanshowbr-vlanstate": "active",
                "vlanshowbr-shutstate": "noshutdown"
            }
        ]
    }
}
>>>
>>>
```

Notice anything different about this object compared to the previous one?  You should see that this is a list of dictionaries and the previous was just a dictionary.  This often happens when using native JSON encoding with NX-API when there is ONE object being returned or MULTIPLE.  One VLAN == dictionary.  More than one VLAN is a list.  Same is true any other objects such as interfaces, neighbors, and so on.  We'll see how to mitigate this later on.

##### Step 20

Print out the VLAN name for VLAN 1 correctly since we now it's a list.

```python
>>> print(vlans['TABLE_vlanbriefxbrief']['ROW_vlanbriefxbrief'][0]['vlanshowbr-vlanname'])
default
```

Because of this, it's common to use the following block of code when using NX-API:

```
>>> if isinstance(<your-variable>, dict):
...     <your-variable> = [<your-variable>]
...
>>>
```

This does a type check on `your-variable` and if it's a dictionary, creates a list of one so you can always through it and not need two ways of access the same sets of data, e.g. when there is one VLAN, and when there is multiple VLANs, when there is one neighbor, and when there are multiple neighbors, etc.

##### Step 21

Print the name for VLAN 10:

```python
>>> print(vlans['TABLE_vlanbriefxbrief']['ROW_vlanbriefxbrief'][1]['vlanshowbr-vlanname'])
VLAN0010
```

Remember, when only ONE element exists (not just for VLANs), a dictionary is returned.  When MORE THAN ONE exists, a list is returned.  


### Task 2 - Gather Neighbors Script

In this task, you will write a script that queries two Cisco Nexus switches for their CDP neighbors.

The final data structure should be a dictionary.  Each key will be the hostname of the device.  The value will be a list of dictionaries - each of these dictionaries should have the following keys:  `neighbor_interface`, `neighbor`, and `local_interface`.

Before you query both devices and create the final script, you will start with testing on the Python shell.


##### Step 1

Run the command `show cdp neighbors` for `nxos-spine1`.  Store the **"JSON"** results in a variable called `data` and print it using `json.dumps`.

You'll notice this process becomes repetitive, so you'd want to store a few of these statements in a re-usable object like a function if you wanted to use this for production.

```python
>>>
>>> payload = {
...     "ins_api": {
...         "version": "1.0",
...         "type": "cli_show",
...         "chunk": "0",
...         "sid": "1",
...         "input": "show cdp neighbors",
...         "output_format": "json"
...     }
... }
>>>
>>> response = requests.post(url, data=json.dumps(payload), headers=headers, auth=auth, verify=False)
>>>
>>> data = json.loads(response.text)
>>>
>>> print(json.dumps(data, indent=4))
{
    "ins_api": {
        "type": "cli_show",
        "version": "1.0",
        "sid": "eoc",
        "outputs": {
            "output": {
                "input": "show cdp neighbors",
                "msg": "Success",
                "code": "200",
                "body": {
                    "neigh_count": 4,
                    "TABLE_cdp_neighbor_brief_info": {
                        "ROW_cdp_neighbor_brief_info": [
                            {
                                "ifindex": 436207616,
                                "device_id": "nxos-spine2.ntc.com(9N9ILWQL1JJ)",
                                "intf_id": "Ethernet1/1",
                                "ttl": "156",
                                "capability": [
                                    "router",
                                    "switch",
                                    "IGMP_cnd_filtering",
                                    "Supports-STP-Dispute"
                                ],
                                "platform_id": "N9K-C9300v",
                                "port_id": "Ethernet1/1"
                            },
                            {
                                "ifindex": 436208128,
                                "device_id": "nxos-spine2.ntc.com(9N9ILWQL1JJ)",
                                "intf_id": "Ethernet1/2",
                                "ttl": "156",
                                "capability": [
                                    "router",
                                    "switch",
                                    "IGMP_cnd_filtering",
                                    "Supports-STP-Dispute"
                                ],
                                "platform_id": "N9K-C9300v",
                                "port_id": "Ethernet1/2"
                            },
                            {
                                "ifindex": 436208640,
                                "device_id": "nxos-spine2.ntc.com(9N9ILWQL1JJ)",
                                "intf_id": "Ethernet1/3",
                                "ttl": "158",
                                "capability": [
                                    "router",
                                    "switch",
                                    "IGMP_cnd_filtering",
                                    "Supports-STP-Dispute"
                                ],
                                "platform_id": "N9K-C9300v",
                                "port_id": "Ethernet1/3"
                            },
                            {
                                "ifindex": 436209152,
                                "device_id": "nxos-spine2.ntc.com(9N9ILWQL1JJ)",
                                "intf_id": "Ethernet1/4",
                                "ttl": "158",
                                "capability": [
                                    "router",
                                    "switch",
                                    "IGMP_cnd_filtering",
                                    "Supports-STP-Dispute"
                                ],
                                "platform_id": "N9K-C9300v",
                                "port_id": "Ethernet1/4"
                            }
                        ]
                    }
                }
            }
        }
    }
}
>>>
```

We can see that **nxos-spine1** has 4+ neighbor entries pointing to the same device, **nxos-spine2**. That's because **nxos-spine1** and **nxos-spine2** are connected with 4 links.

We can also see the keys returned from the device do not match the keys we want for this lab.  We need to map `device_id` to `neighbor`, `port_id` to `neighbor_interface`, and `intf_id` to `local_interface`.

##### Step 2

Extract the neighbors object from `data` and save it as `cdp_neighbors`.

```python
>>> cdp_neighbors = data['ins_api']['outputs']['output']['body']['TABLE_cdp_neighbor_brief_info']['ROW_cdp_neighbor_brief_info']
>>>
```

There are two ways we can go about mapping the current dictionary keys to the desired keys.  We can use conditional if statements for each key or create a dictionary that maps them for us that provides a bit more scale.  Let's use the first option.

##### Step 3

As previously stated, Cisco returns a dictionary when there is a single element like when returning a single neighbor. We will introduce and use isinstance to check the data type of cdp_neighbors. If it is a dictionary, we'll make it a list of 1. If it's a list, it'll stay as is.

```
>>> if isinstance(cdp_neighbors, dict):
...     cdp_neighbors = [cdp_neighbors]
```


##### Step 4

Now create a new list that will store the **new** dictionary with the new values.

This list will be called `neighbors_list`.

```python
>>> neighbors_list = []
>>>
```

##### Step 5

Loop through each neighbor in `cdp_neighbors` (from the Cisco Nexus switch).  For each iteration, you will create a dictionary that will be appended to `neighbors_list`.

While building this dictionary, you will also convert keys as described above.

```python
>>> for neighbor in cdp_neighbors:
...      neighbor = {
...              "neighbor_interface": neighbor["port_id"],
...              "local_interface": neighbor["intf_id"],
...              "neighbor": neighbor["device_id"]
...      }
...      neighbors_list.append(neighbor)
...
>>>
```

##### Step 6

Pretty print `neighbors_list`.

```python
>>> print(json.dumps(neighbors_list, indent=4))
[
    {
        "neighbor_interface": "Ethernet1/1",
        "neighbor": "nxos-spine2.ntc.com(9N9ILWQL1JJ)",
        "local_interface": "Ethernet1/1"
    },
    {
        "neighbor_interface": "Ethernet1/2",
        "neighbor": "nxos-spine2.ntc.com(9N9ILWQL1JJ)",
        "local_interface": "Ethernet1/2"
    },
    {
        "neighbor_interface": "Ethernet1/3",
        "neighbor": "nxos-spine2.ntc.com(9N9ILWQL1JJ)",
        "local_interface": "Ethernet1/3"
    },
    {
        "neighbor_interface": "Ethernet1/4",
        "neighbor": "nxos-spine2.ntc.com(9N9ILWQL1JJ)",
        "local_interface": "Ethernet1/4"
    }
]
>>>
```

##### Challenge Exercise

Use the previous steps to build a script that outputs neighbors for **nxos-spine1** and **nxos-spine2** as such:


```
$ python cisco2.py
{
    "nxos-spine1": [
        {
            "neighbor_interface": "mgmt0",
            "local_interface": "mgmt0",
            "neighbor": "nxos-spine2(TB601325DFB)"
        },
        {
            "neighbor_interface": "Ethernet2/1",
            "local_interface": "Ethernet2/1",
            "neighbor": "nxos-spine2(TB601325DFB)"
        },
        {
            "neighbor_interface": "Ethernet2/2",
            "local_interface": "Ethernet2/2",
            "neighbor": "nxos-spine2(TB601325DFB)"
        },
        {
            "neighbor_interface": "Ethernet2/3",
            "local_interface": "Ethernet2/3",
            "neighbor": "nxos-spine2(TB601325DFB)"
        },
        {
            "neighbor_interface": "Ethernet2/4",
            "local_interface": "Ethernet2/4",
            "neighbor": "nxos-spine2(TB601325DFB)"
        }
    ],
    "nxos-spine2": [
        {
            "neighbor_interface": "mgmt0",
            "local_interface": "mgmt0",
            "neighbor": "nxos-spine1(TB6017D760B)"
        },
        {
            "neighbor_interface": "Ethernet2/1",
            "local_interface": "Ethernet2/1",
            "neighbor": "nxos-spine1(TB6017D760B)"
        },
        {
            "neighbor_interface": "Ethernet2/2",
            "local_interface": "Ethernet2/2",
            "neighbor": "nxos-spine1(TB6017D760B)"
        },
        {
            "neighbor_interface": "Ethernet2/3",
            "local_interface": "Ethernet2/3",
            "neighbor": "nxos-spine1(TB6017D760B)"
        },
        {
            "neighbor_interface": "Ethernet2/4",
            "local_interface": "Ethernet2/4",
            "neighbor": "nxos-spine1(TB6017D760B)"
        }
    ]
}

```


**Scroll for the solution**

```
.
























.
```



### Solution












Here is an example of a working script:

> There is no need to parameterize the command being sent or use functions, but this should give you a good idea how to start coding, and adding modularity, as you re-factor and optimize.  Even the script below could be modularized more.  Remember, this is just for learning purposes.

```python
import requests
import json
from requests.auth import HTTPBasicAuth
requests.packages.urllib3.disable_warnings()


def nxapi_request(device, command):
    auth = HTTPBasicAuth('ntc', 'ntc123')
    headers = {
        'Content-Type': 'application/json'
    }


    url = 'https://{}/ins'.format(device)


    payload = {
        "ins_api": {
            "version": "1.0",
            "type": "cli_show",
            "chunk": "0",
            "sid": "1",
            "input": command,
            "output_format": "json"
        }
    }

    response = requests.post(url, data=json.dumps(payload), headers=headers, auth=auth, verify=False)
    return response

def get_nxos_neighbors(response):

    data = json.loads(response.text)

    device_neighbors = data['ins_api']['outputs']['output']['body']['TABLE_cdp_neighbor_brief_info']['ROW_cdp_neighbor_brief_info']
    if isinstance(device_neighbors, dict):
        device_neighbors = [device_neighbors]

    neighbors_list = []
    for neighbor in device_neighbors:
        neighbor = {
             "neighbor_interface": neighbor["port_id"],
             "local_interface": neighbor["intf_id"],
             "neighbor": neighbor["device_id"]
        }
        neighbors_list.append(neighbor)

    return neighbors_list

def main():

    neighbors = {}

    devices = ['nxos-spine1', 'nxos-spine2']
    command = 'show cdp neighbors'
    for dev in devices:
        response = nxapi_request(dev, command)
        neighbors[dev] = get_nxos_neighbors(response)

    print(json.dumps(neighbors, indent=4))

if __name__ == "__main__":
    main()



```


And there you have it.  A complete script to go out and collect neighbor information from a Cisco DC network.

You can even combine this with a Jinja2 template if you'd like to create a CSV report of all your neighbors!
