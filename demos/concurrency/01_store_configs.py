import threading

from netmiko import ConnectHandler

# Declare devices to automate (inventory)
INV = {
    "csr1": {
        "device_type": "cisco_ios",
        "username": "ntc",
        "password": "ntc123",
        "conf_command": "show run"
    },
    "csr2": {
        "device_type": "cisco_ios",
        "username": "ntc",
        "password": "ntc123",
        "conf_command": "show run"
    },
    "csr3": {
        "device_type": "cisco_ios",
        "username": "ntc",
        "password": "ntc123",
        "conf_command": "show run"
    },
    "nxos-spine1": {
        "device_type": "cisco_nxos",
        "username": "ntc",
        "password": "ntc123",
        "conf_command": "show run"
    },
    "nxos-spine2": {
        "device_type": "cisco_nxos",
        "username": "ntc",
        "password": "ntc123",
        "conf_command": "show run"
    }
}

# Function to run command against device and return the output
def run_command(device, username, password, device_type, command, parse=False):
    # Connect to device using netmiko
    print("Connecting to device {} ...".format(device))
    conn = ConnectHandler(host=device, username=username, password=password, device_type=device_type)

    # Send command 'term len 0' to set CLI output length
    conn.send_command("term len 0")

    # Send command 'show run' to get device configuration
    print("Sending 'show run' command ...")
    if parse:
        output = conn.send_command(command, use_textfsm=True)
    else:
        output = conn.send_command(command)

    return output

def store_config(device):
    # Get config from device
    output = run_command(device, INV[device]["username"], INV[device]["password"], INV[device]["device_type"], INV[device]["conf_command"])

    # Store config in file
    with open("configs/{}.cfg".format(device), "w") as f:
        f.write(output)

def main():
    # Retrieve and store configs from NXOS and CSR devices
    threads = []

    for device in INV:
        t = threading.Thread(target=store_config, args=(device,))
        t.start()
        threads.append(t)
        
    for thread in threads:
        thread.join()

if __name__ == "__main__":
    main()
