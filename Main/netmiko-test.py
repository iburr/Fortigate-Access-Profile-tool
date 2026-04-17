from netmiko import ConnectHandler
from typing import Dict, List
import time as t

# =========
from colorama import init, Fore, Style
init(autoreset=True)
# =========

# Test connections for the devices in question
# Format: {"host": "IP", "username": "username", "password": "password"}
# Following script should not conflict with port binds if enabled via gui access
# Can test this in local enviorments of course.

Devices: List[Dict] = [
    # {"host": "", "username": "admin", "password": ""},
    # {"host": "", "username": "admin", "password": ""},
    # {"host": "__Public_IPAddr__", "username": "admin", "password": "__PW_Placeholder"},
    # {"host": "__Public_IPAddr__", "username": "admin", "password": "__PW_Placeholder"},
]



def accprofile_name(fw, Fortigate) -> str:
    
    # Plug in possible profile names
    possible_name = [
        "SupportAccess",
        "Support_Access",
        "SupporAccess",
        "Support Access",
    ]

    print("Checking profile...", end=" ")
    for name in possible_name: # Iterates through the List depening what profile it is looking for
        try: 
            output = fw.send_command(f'show system accprofile "{name}"', read_timeout=30)
            if "edit" in output.lower():
                print(f"Found {name}\n")
                return name
        except:
            pass
    print(f"\nNothing found check the firewall manually on host: {Fortigate['host']}\n")


def main():
    for Fortigate in Devices:
        print(f"\n Connecting to {Fortigate['username']} ({Fortigate['host']}) ...")

        # Global config layout
        device = {
            "device_type": "fortinet",  #  device in use ex/ arista_eos, cisco_ios, palo_alto_panos, zyxel_os
            "host": Fortigate["host"],
            "username": Fortigate["username"],
            "password": Fortigate["password"],
            "global_delay_factor": 1.5,
        }

        try:
            with ConnectHandler(**device) as fw:
                print(Fore.GREEN + "\n +++++ Connected ++++++ \n")

                #####################################
                profile_name = accprofile_name(fw, Fortigate) # Calls accprofile func into main
                config_commands = [
                    "config system accprofile\n",
                    f'edit "{profile_name}"\n',
                    "set sysgrp read-write\n",
                    "next\n",
                    "end\n",
                ]
                print(f"Applying for profile {profile_name}")
                #####################################

                for cmd in config_commands:
                    output = fw.send_config_set(cmd, exit_config_mode=True, read_timeout=100, delay_factor=2)
                    # timeout is set to 100 cause connection is being established over WAN, slower compared to LAN
                    print(output)

                print(Fore.GREEN + f" Changes are finished on {Fortigate['host']}\n")
        except Exception as e:
            # print(f"  Failed{e}\n")
            print(Fore.RED + f" Failed on {Fortigate['host']}: {e}\n")
        t.sleep(0.5)

    print("All connections have been established")


# Calls Logic first.. Cleaner
if __name__ == "__main__":
    main()
