#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Name        : import-quarantine.py
Description : Script allowing the import of a list of IPs into the quarantine of a Fortigate 
Autor       : 0xmr-cy
Date        : 02/04/2025
Version     : 1.0
License     : GNU General Public License v3.0

Copyright (c) 2025 0xmr-cy
"""

import paramiko
import argparse

def push_commands(target_ip, username, password, vdom, ip_addresses):
    # Create an SSH client instance
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        # Connect to the target device via SSH
        client.connect(target_ip, username=username, password=password)
        shell = client.invoke_shell()

        # If a VDOM is specified, enter VDOM configuration mode
        if vdom:
            config_commands = [
                'config vdom',
                f'edit {vdom}'
            ]
            for command in config_commands:
                shell.send(command + '\n')
                while not shell.recv_ready():
                    pass
                output = shell.recv(1024).decode()
                print(output)

        # Execute quarantine command for each IP address
        for ip_address in ip_addresses:
            command = f"diagnose user banned-ip add src4 {ip_address} 0 admin\n"
            shell.send(command)
            while not shell.recv_ready():
                pass
            output = shell.recv(1024).decode()
            print(output)

        # Exit VDOM config mode if it was used
        if vdom:
            shell.send('end\n')
            while not shell.recv_ready():
                pass
            output = shell.recv(1024).decode()
            print(output)

        # Close SSH connection
        client.close()

    except paramiko.AuthenticationException:
        print(f"SSH authentication failed for device {target_ip}")
    except paramiko.SSHException as e:
        print(f"SSH error on device {target_ip}: {str(e)}")
    except Exception as e:
        print(f"General error while connecting to {target_ip}: {str(e)}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Push quarantine IPs to a FortiGate device.")
    parser.add_argument('--ip', required=True, help="IP address of the FortiGate device")
    parser.add_argument('--username', required=True, help="SSH username")
    parser.add_argument('--password', required=True, help="SSH password")
    parser.add_argument('--vdom', required=False, help="VDOM name (optional)")
    parser.add_argument('--file', default='adresses_ip.txt', help="File containing IP addresses to quarantine")

    args = parser.parse_args()

    # Read IP addresses from the file
    with open(args.file, 'r') as file:
        ip_list = file.read().splitlines()

    # Call the function with the provided arguments
    push_commands(args.ip, args.username, args.password, args.vdom, ip_list)
