# FortiGate IP Quarantine Script

This Python script allows you to automatically add IP addresses to quarantine on a FortiGate device via SSH. It is especially useful for network administrators managing FortiGate firewalls.

## Features

- **SSH Connectivity**:  
  Connect to FortiGate devices using SSH with customizable username, password, and IP address.
  
- **VDOM Support**:  
  Supports FortiGate VDOM (Virtual Domain) configuration. You can specify the VDOM you wish to apply the commands to, or skip it if not needed.

- **Batch IP Quarantine**:  
  The script reads IP addresses from a text file and executes the quarantine command on each IP address, blocking potential threats.

## Usage

To run the script, use the following command:
```bash
python push_commands.py --ip <device_ip> --username <ssh_username> --password <ssh_password> --vdom <vdom_name> --file <ip_file.txt>
```
### Arguments:

- `--ip`: **Required**  
  The IP address of the FortiGate device you want to connect to.

- `--username`: **Required**  
  Your SSH username for the FortiGate device.

- `--password`: **Required**  
  Your SSH password for the FortiGate device.

- `--vdom`: **Optional**  
  The name of the VDOM you want to configure. If omitted, the script will configure the global settings.

- `--file`: **Optional**  
  The path to a text file containing a list of IP addresses to quarantine. Default is `adresses_ip.txt`.

  
## Important Notes

FortiOS Versions Before 7.2:
In FortiOS versions prior to 7.2, the command used to quarantine IPs is diagnose user quarantine add src4 {ip_address} 0 admin. If you are using a FortiGate device with a version before 7.2, you will need to update the script to use this command instead of the newer diagnose user banned-ip add command.
In the script, you can modify the line:
```bash
command = f"diagnose user banned-ip add src4 {ip_address} 0 admin\n"
```
to:
```bash
command = f"diagnose user quarantine add src4 {ip_address} 0 admin\n"
```
FortiOS 7.2 and Later:
The script is compatible with FortiOS version 7.2 and above, where the diagnose user quarantine add command works as expected.

## Dependencies

Python 3.x
paramiko for SSH communication.
You can install the required package using pip:
```bash
pip install paramiko
```
## License

This script is distributed under the GNU General Public License v3.0.
See LICENSE for more details.

## Points to Keep in Mind
Ensure you have access to the FortiGate device via SSH.
Always test on a non-production device before applying changes to live systems.
Make sure you have the correct permissions to execute quarantine commands on the FortiGate device.
For older versions of FortiOS (pre-7.2), ensure the script is updated as described above.
