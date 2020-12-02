layout: true

.footer-picture[![Network to Code Logo](data/media/Footer2.PNG)]
.footnote-left[(C) 2018 Network to Code, LLC. All Rights Reserved. ]
.footnote-con[CONFIDENTIAL]

---

class: center, middle, title
.footer-picture[<img src="data/media/Footer1.PNG" alt="Blue Logo" style="alight:middle;width:350px;height:60px;">]

# Bonus Material

---

# Module Overview

- Concurrency

---

class: middle, segue

# Concurrency
### Refactoring for Efficiency

---

# Concurrency and Parallelism

Concurrency is switching between threads to improve performance

Parallelism is threads running at the same time

They can work together or seperatly to speed up your program

If you have a task to run against multiple devices, you can send all the requests without having to wait for the device response using concurrency.

---

# Concurrency

Many ways of doing this in Python, we will be using the `threading` module

You can define a function to perform an action or functionality

Then create a thread to run the created function

```python
import threading
from netmiko import ConnectHandler

def get_neighbors(hostname):
    device = ConnectHandler(host=device, username='ntc', password='ntc123', device_type='cisco_ios')
    neighbors_data = device.send_command("show lldp neighbors")
    print(neighbors_data)

devices = ["csr1", "csr2", "csr3"]
threads = []

for device in devices:
    t = threading.Thread(target=get_neighbors, args=(device))
    t.start()
    threads.append(t)

for thread in threads:
    thread.join()
```

---

# Why Concurrency Is Great For Network Automation

Many of the tasks in network automation aren't time critical, it doesn't matter if they take 20 ms to run or 20 minutes. 

That said, concurrency allows you to speed up your automations without having to get too crazy with optimizations. Many tools like ansible and nornir utilize concurrency to help run more efficiently.

Many tasks in network automation involve interacting with network devices. The time it takes to connect and recieve data from these devices is the majority of the time your automations will run.

With concurrency you can send all your requests at about the same time, removing most of the wait time in your tasks.

---

# Thread Safe Resources

As you get deeper into developing your own automations, you will find many more complex issues. For concurrency, resource sharing is one such issue.

Multiple threads can't access the same resource at the same time, so you can use thread safe types like Queues.

A Queue is basically a special list, you have a limited set of operations compared to the default python list. You can add items to one end of the Queue and remove them from the other. You can't access, add, or modify items in the middle of the Queue like a list. This limited feature set makes it easier for its operations to be thread safe, meaning that multiple threads can interact with it without running into issues.

In python we will create a Queue object, then utilize its `put` and `get` methods to add and remove from it.

---

# Thread Safe Resources

```python
import queue
import threading
from netmiko import ConnectHandler

q = queue.Queue()

def get_neighbors(q, hostname):
    device = ConnectHandler(host=device, username='ntc', password='ntc123', device_type='cisco_ios')
    q.put(device.send_command("show lldp neighbors"))

devices = ["csr1", "csr2", "csr3"]
threads = []

for device in devices:
    t = threading.Thread(target=get_neighbors, args=(q,device))
    t.start()
    threads.append(t)

for thread in threads:
    thread.join()

neighbor_data = q.get()
```

---

# Summary

- Concurrency helps reduce runtime by removing IO wait time
- Threads aren't running simultaneously, they are scheduled more efficiently
- Increases code efficiency, but can be difficult with more advanced use cases

---

# Lab Time

- Lab 23 - Refactoring with Concurrency
