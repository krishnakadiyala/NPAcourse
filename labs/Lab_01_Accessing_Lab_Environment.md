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






