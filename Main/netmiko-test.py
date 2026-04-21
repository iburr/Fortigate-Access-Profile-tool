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
    {"host": "192.168.25.1", "username": "admin", "password": "admin"},
    # {"host": "192.168.30.1", "username": "admin", "password": "admin"},
    # {"host": "192.168.31.1", "username": "admin", "password": ""},
    # {"host": "", "username": "admin", "password": ""},
    # {"host": "__Public_IPAddr__", "username": "admin", "password": "__PW_Placeholder"},
    # {"host": "__Public_IPAddr__", "username": "admin", "password": "__PW_Placeholder"},
]



def accprofile_name(fw, Fortigate):
    
    # Plug in possible profile names
    possible_name = [
        "SupportAccess",
        "Support_Access",
        "SupporAccess",
        "Support Access",
    ]

    # List for duplicate admin profiles 
    duplicate_counter = []


    print("Checking profile...", end=" \n")
    for name in possible_name: # Iterates through the possible_name List depening what profile it is looking for
        try: 
            output = fw.send_command(f'show system accprofile "{name}"', read_timeout=30)

            if "edit" in output.lower():
                print(f"\nFound {name} applying chages to {name}...")
                
                config_commands = [
                    "config system accprofile\n",
                    f'edit "{name}"\n',
                    "set sysgrp read-write\n",
                    "next\n",
                    "end\n",
                ]
                    
                running_config = fw.send_config_set(config_commands, exit_config_mode=True, read_timeout=100, delay_factor=2)
                duplicate_counter.append(name)
                print(running_config)
        except:
            pass


    if duplicate_counter:
        print(Fore.CYAN + f"\nUpdated {len(duplicate_counter)} profiles: {', '.join(duplicate_counter)} on {Fortigate['host']}")
        return duplicate_counter
    else:
        print(Fore.YELLOW + f"No Matching profile found on: {Fortigate['host']}")
        return []



def main():
    for Fortigate in Devices:
        print(f"\nConnecting to {Fortigate['username']} ({Fortigate['host']}) ...")

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
                updated_name = accprofile_name(fw, Fortigate) # Calls accprofile func into main
                if updated_name:
                    print(Fore.GREEN + f"Changes are finished on {Fortigate['host']}")
                else:
                    pass
                #####################################

        except Exception as e:
            print(Fore.RED + f"\nFailed on {Fortigate['host']}: {e}\n")
        t.sleep(0.5)

    print("\nAll connections have been established")


# Calls Logic first.. Cleaner
if __name__ == "__main__":
    main()
