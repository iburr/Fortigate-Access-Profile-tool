# Fortigate-Access-Profile-tool


A script that builds on top of my existing Fortigate script on my repo that automates updating the administrative access profile (`accprofile`) across multiple FortiGate firewalls.
Made with the intent for handling permissions of what certain Adminstatator groups can See/Do on the Firewall
I created this tool because manually updating the same profile on 70+ firewalls was time-consuming and error-prone — especially since the profile name can vary across devices. 

For ex/ within the Fortigates GUI sys settings  (`SupportAccess`, `Support Access`, `Support_Access`, etc.).

### Features
- Automatically detects the accprofile name on each firewall
- Handles multiple naming variations without manual intervention
- Applies consistent `sysgrp read-write` permissions but is not limited to what the script can edit within the permissions for that profile. 
- Colored console output for easy reading
- Easy to maintain and extend

### Technologies Used
- Python 3
- Netmiko
- Colorama (for colored output)

### Requirements
- Python 3.8+
- Netmiko (`pip install netmiko`)
- Colorama (`pip install colorama`)

### Setup

1. Clone or download the repository
2. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   ```
   ```powershell
   python -m venv venv

   .\venv\Scripts\Activate.ps1
   ```
