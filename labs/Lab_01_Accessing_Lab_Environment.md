## Lab 1 - Accessing the Lab Environment

### Task 1 - Understand the Lab Topology

You will primarily access the Linux jump host for all labs in the course.

![Lab Topology](images/lab-topology.png)


### Task 2 - Accessing the Lab Environment

Obtain your Public IP Address from the Course Instructor
*  This is the public IP of your Linux jump host
*  You will be able to access all network devices by name through this jump host when the network labs start

As of December 2018, your Linux jump host will be accessible at the following address:

```
jump-host.pod<pod-number>.ntc.cloud.tesuto.com
```

Username: **ntc**
Password: **ntc123**

You can access the Jump Host via SSH or RDP (for a full desktop experience)

Using a Linux based OS, use the following command:

```
ssh ntc@jump-host.pod<pod-number>.ntc.cloud.tesuto.com
```

Otherwise, you can use a standard SSH client such as Putty or SecureCRT.


### Task 3 - Verify Name Resolution on the Jump Host

Although many devices are still turned down for Day 1 of the training, verify that `/etc/hosts` is set properly.

You should be able to ping every device by name (as shown in the diagram).  

> Note: you are at least verifying name to IP mappings even though devices are down.  Control+C will stop the ping requests.

```
ping csr1
ping csr2
ping csr3
ping vmx1
ping vmx2
ping vmx3
ping nxos-spine1
ping nxos-spine2
ping eos-spine1
ping eos-spine2
ping eos-leaf1
ping eos-leaf2

```




