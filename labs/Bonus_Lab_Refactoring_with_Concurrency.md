# Bonus Lab - Re-factoring Code with Concurrency

In the previous sections we learned more ways of interacting with network deices using their command lines and APIs. Now you'll refactor that process to utilize concurrency to reduce IO wait time.

### Task 1 - Improve the Backup Script

##### Step 1

We will begin with a backup script that looks like this:

```python
#! /usr/bin/env python

from netmiko import ConnectHandler

def connect_to_device(hostname):
    print("Connecting to device | {}".format(hostname))
    net_d = ConnectHandler(host=hostname, username='ntc', password='ntc123', device_type='cisco_ios')

    return net_d

def save_config(device, hostname):
    print("Saving configuration | {}".format(hostname))
    device.send_command("wr mem")

def backup_config(device, hostname):
    print("Backing up configuration | {}".format(hostname))
    device.send_command("term len 0")
    config = device.send_command("show run")

    return config

def write_to_file(hostname, show_run):
    print("Writing config to file | {}\n".format(hostname))
    with open("configs/{}.cfg".format(hostname), "w") as config_file:
        config_file.write(show_run)

def main():
    devices = ['csr1', 'csr2', 'csr3']

    for device in devices:
        net_device = connect_to_device(device)

        save_config(net_device, device)

        config = backup_config(net_device, device)

        write_to_file(device, config)

        net_device.disconnect()

if __name__ == "__main__":
    main()

```

Open this script and save it as `backup_conncurrent.py`

##### Step 2

To utilize concurrency in python we will use the `threading` module, add an import for it at the top of the file. 

The different actions performed on each device can be moved into a single function. We will do this so that we can pass a single function into our Threads as the target action. We could create individual threads for each action seperately but that wouldn't help us much more since these threads will already break when waiting on input. This also allows us to keep a safe ordering of the tasks each device goes through.

Create `automate_device_config(device)`.  Simply put everything from the for loop in `main()` inside this function, then call it from the for loop passing in the device.

It should look like this:

```python
#! /usr/bin/env python
import threading

from netmiko import ConnectHandler

def connect_to_device(hostname):
    print("Connecting to device | {}".format(hostname))
    net_d = ConnectHandler(host=hostname, username='ntc', password='ntc123', device_type='cisco_ios')

    return net_d

def save_config(device, hostname):
    print("Saving configuration | {}".format(hostname))
    device.send_command("wr mem")

def backup_config(device, hostname):
    print("Backing up configuration | {}".format(hostname))
    device.send_command("term len 0")
    config = device.send_command("show run")

    return config

def write_to_file(hostname, show_run):
    print("Writing config to file | {}\n".format(hostname))
    with open("configs/{}.cfg".format(hostname), "w") as config_file:
        config_file.write(show_run)

def automate_device_config(device):
    net_device = connect_to_device(device)

    save_config(net_device, device)

    config = backup_config(net_device, device)

    write_to_file(device, config)

    net_device.disconnect()

def main():
    devices = ['csr1', 'csr2', 'csr3']

    for device in devices:
        automate_device_config(device)

if __name__ == "__main__":
    main()
```

##### Step 3

Now that we have the functionality separated, we can instead run it as its own thread. To start we will need a list to keep track of our threads. This will be important so that we can close each thread once its finished. 

Define an empty list called `threads` above the for loop in the `main` function like this:

```python
def main():
    devices = ['csr1', 'csr2', 'csr3']

    threads = []
    for device in devices:
        automate_device_config(device)
```

##### Step 4

Next we will change the line that calls `automate_device_config` to instead create a thread that will run the function.

Add the following line to create the thread using the `threading` module:


```python
def main():
    devices = ['csr1', 'csr2', 'csr3']

    threads = []
    for device in devices:
        t = threading.Thread(target=automate_device_config, args=(device,))

```

The thread object is stored in the variable `t`. The `target=` defines the function that will serve as the threads functionality. The `args=` takes in any arguments that need to be passed to the function in the thread. This argument is taken in as a tuple, which is why the `device` variable is wrapped as `(device,)`.

##### Step 5

Now that the thread is created, we need to use its `start()` method to allow it to start executing. When we run `start()`, the thread won't necessarily start running that instant, concurrency allows us to save IO wait time by scheduling our execution better. Since the main program that created the thread is still running, that thread most likely won't start executing until the main code stops. 

Add the call to `start()` after the thread is created:

```python
def main():
    devices = ['csr1', 'csr2', 'csr3']

    threads = []
    for device in devices:
        t = threading.Thread(target=automate_device_config, args=(device,))
        t.start()

```

##### Step 6

From here we could let the for loop continue and it would create each thread that we need and start them. The problem with this is we would only have a reference to our last thread since the variable `t` would be overwritten with each iteration of the loop. To solve this we will append each thread to the list of threads we defined before like this:

```python
def main():
    devices = ['csr1', 'csr2', 'csr3']

    threads = []
    for device in devices:
        t = threading.Thread(target=automate_device_config, args=(device,))
        t.start()
        threads.append(t)
```

Once that for loop finishes running now, a thread for each CSR device will be created, started, and stored in our `threads` list. Now we need to stop our main program from running and wait to give the threads time to execute. To do this we will use the threads `join` method, which waits for the thread to finish executing before continuing. 

We need to call `join` on each thread since we don't know which thread will finish executing first. Add a for loop that will call the `join` method on each thread in our `threads` list:

```python
def main():
    devices = ['csr1', 'csr2', 'csr3']

    threads = []
    for device in devices:
        t = threading.Thread(target=automate_device_config, args=(device,))
        t.start()
        threads.append(t)
    
    for thread in threads:
        thread.join()

```

And thats it, with those few changes we've now enabled our python code to run more efficiently by allowing multiple runs of our task to happen as others are waiting for input from their devices. 

The code at this point should look like this:

```python
#! /usr/bin/env python
import threading

from netmiko import ConnectHandler

def connect_to_device(hostname):
    print("Connecting to device | {}".format(hostname))
    net_d = ConnectHandler(host=hostname, username='ntc', password='ntc123', device_type='cisco_ios')

    return net_d

def save_config(device, hostname):
    print("Saving configuration | {}".format(hostname))
    device.send_command("wr mem")

def backup_config(device, hostname):
    print("Backing up configuration | {}".format(hostname))
    device.send_command("term len 0")
    config = device.send_command("show run")

    return config

def write_to_file(hostname, show_run):
    print("Writing config to file | {}\n".format(hostname))
    with open("configs/{}.cfg".format(hostname), "w") as config_file:
        config_file.write(show_run)

def automate_device_config(device):
    net_device = connect_to_device(device)

    save_config(net_device, device)

    config = backup_config(net_device, device)

    write_to_file(device, config)

    net_device.disconnect()

def main():
    devices = ['csr1', 'csr2', 'csr3']

    threads = []
    for device in devices:
        t = threading.Thread(target=automate_device_config, args=(device,))
        t.start()
        threads.append(t)
    
    for thread in threads:
        thread.join()

if __name__ == "__main__":
    main()
```

Just by running the original sequential code vs. the new concurrent code you can probably see a difference, but to see exactly how much faster our code is running we can time the `main` function.

Add the following code to the `main` function and the import for the `time` module:

```python
import time 

# ...

def main():
    start_time = time.time()
    devices = ['csr1', 'csr2', 'csr3']

    threads = []
    for device in devices:
        t = threading.Thread(target=automate_device_config, args=(device,))
        t.start()
        threads.append(t)
    
    for thread in threads:
        thread.join()
    end_time = time.time()
    print(f"Execution time: {end_time - start_time}")

```

You can go ahead and run this a few times in both the current concurrent mode, as well as changing it back to run sequentially. It won't be exact, but the concurrent code should run faster by a factor of the number of devices were automating. Since the longest part of our code by far is the wait time to connect and get data from devices, we are able to send all our requests first and simply wait at the same time, making the time faster by the number of devices automated. 

In addition to seeign how much faster our code now runs, we can see anther interesting behavior of our concurrent code. When we run it, the order in which the threads complete will not always be the same. The order will depend on which threads are selected to execute first and which devices return their data fastest. 

To test this we can add a print statment to the `automate_device_config` function that indicates when that devices is finished automating:

```python
def automate_device_config(device):
    net_device = connect_to_device(device)

    save_config(net_device, device)

    config = backup_config(net_device, device)

    write_to_file(device, config)

    net_device.disconnect()

    print(f"Device {device} finished successfully.")
```

After making this change you can run the script a few times and see the order in which the devices finish their tasks. It may look like the devices are finishing in their starting order most of the time, but this is usually just due to the order of the scheduling and the fact that all the devices should return their data in similar times due to our environment. 

Final Script should look like this:

```python
#! /usr/bin/env python
import threading
import time

from netmiko import ConnectHandler

def connect_to_device(hostname):
    print("Connecting to device | {}".format(hostname))
    net_d = ConnectHandler(host=hostname, username='ntc', password='ntc123', device_type='cisco_ios')

    return net_d

def save_config(device, hostname):
    print("Saving configuration | {}".format(hostname))
    device.send_command("wr mem")

def backup_config(device, hostname):
    print("Backing up configuration | {}".format(hostname))
    device.send_command("term len 0")
    config = device.send_command("show run")

    return config

def write_to_file(hostname, show_run):
    print("Writing config to file | {}\n".format(hostname))
    with open("configs/{}.cfg".format(hostname), "w") as config_file:
        config_file.write(show_run)

def automate_device_config(device):
    net_device = connect_to_device(device)

    save_config(net_device, device)

    config = backup_config(net_device, device)

    write_to_file(device, config)

    net_device.disconnect()

    print(f"Device {device} finished successfully.")

def main():
    start_time = time.time()
    devices = ['csr1', 'csr2', 'csr3']

    threads = []
    for device in devices:
        t = threading.Thread(target=automate_device_config, args=(device,))
        t.start()
        threads.append(t)
    
    for thread in threads:
        thread.join()
    end_time = time.time()
    print(f"Execution time: {end_time - start_time}")

if __name__ == "__main__":
    main()
```