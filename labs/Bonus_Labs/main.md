# Ansible Bonus Labs

[Dynamic Device Discovery with Dynamic Groups](Device_Discovery_Dynamic_Groups.md)

This lab walks through gathering facts and then creating ad-hoc and dynamic groups based on data such as OS version so you can automate different tasks on different OS versions within the same playbook.

[Exploring Dynamic Inventory](Dynamic_Inventory.md)

Eventually you outgrow using inventory files and should think about using a Source of Truth database like NetBox, an NMS, or another existing CMDB.  This lab walks through what it is like to use an external source for inventory and variables.

[Using Useful Jinja2 Filters](Using_Jinja2_Filters.md)

Understanding how to use Jinja filter will save you YEARS in your Ansible journey in terms of manipulating, accessing, and managing data.  This is a must.

[Managing Configurations with NAPALM](Build_Push.md)

The course covered Jinja templating and NAPALM independently, but this provides a look at managing several configuration stanzas, re-building configurations, and then deploying with NAPALM.  Take a look at the Junos example for a full example.


[Parsing Show Commands - 01](Parsing_Show_Commands.md)

Walks through ways to parse text ("show commands") into structured data.  

[Parsing Show Commands - 02](Parser_Templates.md)

Walks through more ways to parse text ("show commands") into structured data.  

**Create Custom Modules and Jinja Filters**

This is an advanced topic and there is no associated lab guide.  There is a playbook that uses a custom module and one that uses a custom filter.  They can be found in the `./custom/library` and `./customer/filter_plugins` sub-directories respectively.  [View the directory here](./custom).



