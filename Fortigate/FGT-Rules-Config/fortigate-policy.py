#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Name        : fortigate-policy.py
Description : Script allowing the transposition of Fortinet rules from an export config file in a CSV file 
Autor       : 0xmr-cy
Date        : 02/04/2025
Version     : 1.0
License     : GNU General Public License v3.0

Copyright (c) 2025 0xmr-cy
"""

import sys
import re
import csv

# Output file
output = "policies-out2.csv"

# Dictionaries to store policies and view keys
policies = {}
seen_keys = set()
order_keys = []

# Flags and counters
in_policy_block = False
policyid = None

# Read from the file passed as an argument
if len(sys.argv) < 2:
    print("Usage: python fortigate.py policy-conf.txt")
    sys.exit(1)

input_file = sys.argv[1]

with open(input_file, 'r') as infile:
    for line in infile:
        line = line.strip()

        if in_policy_block:
            match_edit = re.match(r'^edit\s+(\d+)', line, re.IGNORECASE)
            match_set = re.match(r'^set\s+(\S+)\s+(.*)', line, re.IGNORECASE)
            match_end = re.match(r'^end', line, re.IGNORECASE)

            if match_edit:
                policyid = int(match_edit.group(1))
                policies[policyid] = {}
            elif match_set and policyid is not None:
                key, value = match_set.group(1), match_set.group(2).strip('"').strip()
                if key not in seen_keys:
                    seen_keys.add(key)
                    order_keys.append(key)
                policies[policyid][key] = value
            elif match_end:
                in_policy_block = False

        elif re.match(r'^config firewall policy', line, re.IGNORECASE):
            in_policy_block = True

# Writing to the CSV file
with open(output, 'w', newline='') as outfile:
    writer = csv.writer(outfile)
    # Writing the header
    writer.writerow(['id'] + order_keys)

    # Writing policies
    for policy_id in sorted(policies.keys()):
        row = [policy_id]
        for key in order_keys:
            row.append(policies[policy_id].get(key, ''))
        writer.writerow(row)
