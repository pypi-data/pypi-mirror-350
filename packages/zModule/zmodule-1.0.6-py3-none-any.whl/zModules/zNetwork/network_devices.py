from typing import Union
import subprocess
import re

def get_network_devices() -> Union[str, list]:

    """
    Returns a list of all devices on the local network with IP and MAC addresses.
    Uses arp -a on Windows.

    :param: None
    :return: List with Tuples: "IP": ip, "MAC": mac
    """

    devices = []
    
    try:

        result = subprocess.run(["arp", "-a"], capture_output = True, text = True) #! run arp -a
        arp_output = result.stdout #! formate output

        for line in arp_output.split('\n'): #! for every line

            match = re.search(r"(\d+\.\d+\.\d+\.\d+)\s+([0-9a-f-]+)", line) #! search IP and MAC format with regex

            if match:

                ip = match.group(1) #! first regex group
                mac = match.group(2).replace('-', ':') #! second regex group
                devices.append({"IP": ip, "MAC": mac.upper()}) #! append to list
                
        return devices
    
    except Exception:

        return "Error"
