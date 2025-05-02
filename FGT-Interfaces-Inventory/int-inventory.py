#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Name        : fgtrules.py
Description : Script to inventory the interfaces and routes of a Fortigate
Autor       : 0xmr-cy
Date        : 25/04/2025
Version     : 1.3
License     : GNU General Public License v3.0

Copyright (c) 2025 0xmr-cy
"""

import csv
import re
import sys

# --------- Step 1: Parse interface configuration ---------
def parse_interfaces(config_file):
    interfaces = []

    with open(config_file, 'r') as file:
        config_data = file.read()

    # Match each "edit" section (individual interface definition)
    matches = re.findall(r'edit "(.*?)"(.*?)next', config_data, re.DOTALL)
    for name, content in matches:
        interface = {
            "FW": "",
            "IP FW": "",
            "Fortimanager": "",
            "Fortianalyzer": "",
            "VDOM": "",
            "Type": "",
            "Vlan": "",
            "Interface": name,
            "Network": "",
            "Zone": "",
            "Destination": "",
            "Gateway": "",
            "Protocole": "",
            "Status": "up",
            "LAG": "",
            "IPv6": ""
        }

        # Extract IPv4 address and netmask
        ip_match = re.search(r'set ip (\d+\.\d+\.\d+\.\d+) (\d+\.\d+\.\d+\.\d+)', content)
        if ip_match:
            ip_addr, netmask = ip_match.groups()
            interface["Network"] = f"{ip_addr}/{netmask}"
        elif re.search(r'set mode dhcp', content):
            interface["Network"] = "DHCP"

        # Extract IPv6 address if present
        ipv6_match = re.search(r'config ipv6\s+set ip6-address ([\da-fA-F:]+/\d+)', content)
        if ipv6_match:
            interface["IPv6"] = ipv6_match.group(1)

        # Extract VLAN ID
        vlan_match = re.search(r'set vlanid (\d+)', content)
        if vlan_match:
            interface["Vlan"] = vlan_match.group(1)

        # Extract interface type
        type_match = re.search(r'set type (\w+)', content)
        if type_match:
            interface["Type"] = type_match.group(1)

        # Extract VDOM name
        vdom_match = re.search(r'set vdom "(.*?)"', content)
        if vdom_match:
            interface["VDOM"] = vdom_match.group(1)

        # Check if interface is down
        status_match = re.search(r'set status (\w+)', content)
        if status_match and status_match.group(1) == 'down':
            interface["Status"] = "down"

        # Check if it's a member of a LAG
        lag_match = re.search(r'set interface "(.*?)"', content)
        if lag_match:
            interface["LAG"] = lag_match.group(1)

        interfaces.append(interface)

    return interfaces

# --------- Step 2: Parse routing table ---------
def read_routes(route_file):
    routes = []

    with open(route_file, 'r') as f:
        for line in f:
            line = line.strip()

            # Match standard static route
            match_simple = re.match(r'^(S\*?)\s+(\d+\.\d+\.\d+\.\d+/\d+)\s+\[\d+/\d+\]\s+via\s+(\S+)\s+(\S+),\s+\[\d+/\d+\]', line)
            if match_simple:
                print(f"[DEBUG] Match trouvé: {match_simple.groups()}")  # Pour déboguer
                Protocol, Destination, Gateway, Interface = match_simple.groups()
                routes.append({'Destination': Destination, 'Gateway': Gateway, 'Protocole': Protocol, 'Interface': Interface})
                continue

            # Match BGP route with recursive resolution
            match_complex = re.match(r'^(B)\s+(\d+\.\d+\.\d+\.\d+/\d+)\s+\[\d+/\d+\]\s+via\s+(\S+)\s+\(recursive is directly connected, ([^)]+)\),.*$', line)
            if match_complex:
                print(f"[DEBUG] Match trouvé: {match_complex.groups()}")  # Pour déboguer
                Protocol, Destination, Gateway, Interface = match_complex.groups()
                routes.append({'Destination': Destination, 'Gateway': Gateway, 'Protocole': Protocol, 'Interface': Interface})
                continue

            # Passer à la ligne suivante
            # Match static route: S       10.2.0.0/16 [240/0] via VPN-PRIMARY tunnel 87.254.104.10, [1/0]
            match_static = re.match(r'^(S\*?)\s+(\d+\.\d+\.\d+\.\d+/\d+)\s+\[\d+/\d+\]\s+via\s+(\S+)(?:\s+tunnel)?\s+(\d+\.\d+\.\d+\.\d+),',line)
            if match_static:
                print(f"[DEBUG] Match trouvé: {match_static.groups()}")  # Pour déboguer
                Protocole, Destination, Interface, Gateway = match_static.groups()
                routes.append({'Destination': Destination, 'Gateway': Gateway, 'Protocole': Protocol, 'Interface': Interface})
                continue

            # Match BGP route with recursive resolution:
            # B 10.2.1.0/24 [20/0] via 10.1.10.254 (recursive via VPN-PRIMARY tunnel 87.254.104.10), ...
            match_bgp_recursive = re.match(r'^(B)\s+(\d+\.\d+\.\d+\.\d+/\d+)\s+\[\d+/\d+\]\s+via\s+(\d+\.\d+\.\d+\.\d+)\s+\(recursive via\s+(\S+)\s+tunnel\s+(\d+\.\d+\.\d+\.\d+)\),',line)
            if match_bgp_recursive:
                print(f"[DEBUG] Match trouvé: {match_bgp_recursive.groups()}")  # Pour déboguer
                Protocole, Destination, Gateway, Interface, TunnelGateway = match_bgp_recursive.groups()
                routes.append({'Destination': Destination, 'Gateway': Gateway, 'Protocole': Protocol, 'Interface': Interface})
                continue

            # Match BGP route with directly connected recursive: 
            # B 10.2.3.0/24 [20/0] via 10.1.10.254 (recursive is directly connected, VLAN10)
            match_bgp_direct = re.match(r'^(B)\s+(\d+\.\d+\.\d+\.\d+/\d+)\s+\[\d+/\d+\]\s+via\s+(\d+\.\d+\.\d+\.\d+)\s+\(recursive is directly connected,\s+([^)]+)\)',line)
            if match_bgp_direct:
                print(f"[DEBUG] Match trouvé: {match_bgp_direct.groups()}")  # Pour déboguer
                Protocole, Destination, Gateway, Interface = match_bgp_direct.groups()
                routes.append({'Destination': Destination, 'Gateway': Gateway, 'Protocole': Protocol, 'Interface': Interface})
                continue
    return routes

# --------- Step 3: Merge interfaces and routes into a CSV file ---------
def merge_data(interfaces, routes, output_file):
    # Define CSV headers
    fieldnames = [
        'FW', 'IP FW', 'Fortimanager', 'Fortianalyzer', 'VDOM', 'Type', 'Vlan', 'Interface',
        'Network', 'Zone', 'Destination', 'Gateway', 'Protocole', 'Status', 'LAG', 'IPv6'
    ]

    # Organize routes by associated interface
    routes_by_interface = {}
    for route in routes:
        iface = route['Interface']
        routes_by_interface.setdefault(iface, []).append(route)

    # Write final merged CSV
    with open(output_file, mode='w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for interface in interfaces:
            iface_name = interface['Interface']
            if iface_name in routes_by_interface:
                for route in routes_by_interface[iface_name]:
                    row = {**interface, **route}
                    writer.writerow(row)
            else:
                writer.writerow(interface)

    print(f"[INFO] Merged file written: {output_file}")

# --------- Main program entry point ---------
if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python script.py <config_file> <route_file> <output_file>")
        sys.exit(1)

    config_file = sys.argv[1]
    route_file = sys.argv[2]
    output_file = sys.argv[3]

    print("[INFO] Reading configuration file...")
    interfaces = parse_interfaces(config_file)

    print("[INFO] Reading route file...")
    routes = read_routes(route_file)

    print("[INFO] Merging data...")
    merge_data(interfaces, routes, output_file)

    print("[OK] CSV file generated:", output_file)
