import json
import requests
import threading
import queue

from requests.auth import HTTPBasicAuth
requests.packages.urllib3.disable_warnings()

# Declare devices to automate (inventory)
INV = {
    "nxos-spine1": {
        "device_type": "cisco_nxos",
        "username": "ntc",
        "password": "ntc123",
        "command": "show cdp neighbors"
    },
    "nxos-spine2": {
        "device_type": "cisco_nxos",
        "username": "ntc",
        "password": "ntc123",
        "command": "show cdp neighbors"
    }
}

def get_neighbors_data(q, device):
    auth = HTTPBasicAuth('ntc', 'ntc123')
    headers = {
        "Content-Type": "application/json"
    }
    payload = {
        "ins_api": {
            "version": "1.0",
            "type": "cli_show",
            "chunk": "0",
            "sid": "1",
            "input": "show cdp neighbors",
            "output_format": "json"
        }
    }
    url = "https://nxos-spine1/ins"

    response = requests.post(url, data=json.dumps(payload), headers=headers, auth=auth, verify=False)
    q.put((device, response.json()))

def parse_neighbor_data(q):
    parsed_data = {}
    while(not q.empty()):
        device, neighbor_data = q.get()
        parsed_data[device] = []

        data = neighbor_data["ins_api"]["outputs"]["output"]["body"]["TABLE_cdp_neighbor_brief_info"]["ROW_cdp_neighbor_brief_info"]
        for item in data:
            parsed_data[device].append({"device_id": item["device_id"], "intf_id": item["intf_id"], "port_id": item["port_id"]})

    return parsed_data

def print_neighbor_info(parsed_data):
    for device in parsed_data:
        print(f"Device: {device}")
        for item in parsed_data[device]:
            print(f"  Device ID: {item['device_id']}  Interface ID: {item['intf_id']}  Port ID: {item['port_id']}")

def main():
    # Get CDP Neighbor Data
    q = queue.Queue()
    threads = []

    # Retrieve data from each device
    for device in INV:
        t = threading.Thread(target=get_neighbors_data, args=(q, device))
        t.start()
        threads.append(t)

    for thread in threads:
        thread.join()

    # Parse data
    data = parse_neighbor_data(q)

    # Print Data
    print_neighbor_info(data)

if __name__ == "__main__":
    main()
