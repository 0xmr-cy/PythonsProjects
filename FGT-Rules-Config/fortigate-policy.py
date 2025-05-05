#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Name        : fgtrules.py
Description : Script allowing the transposition of Fortinet rules into JSON export in a CSV file 
Autor       : 0xmr-cy
Date        : 28/04/2025
Version     : 1.1
License     : GNU General Public License v3.0

Copyright (c) 2025 0xmr-cy
"""

import sys
import re
import csv

# Fichier de sortie
output = "policies-out2.csv"

# Dictionnaires pour stocker les politiques et les clés vues
policies = {}
seen_keys = set()
order_keys = []

# Flags et compteurs
in_policy_block = False
policyid = None

# Lire depuis le fichier passé en argument
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

# Écriture dans le fichier CSV
with open(output, 'w', newline='') as outfile:
    writer = csv.writer(outfile)
    # Écriture de l'en-tête
    writer.writerow(['id'] + order_keys)

    # Écriture des politiques
    for policy_id in sorted(policies.keys()):
        row = [policy_id]
        for key in order_keys:
            row.append(policies[policy_id].get(key, ''))
        writer.writerow(row)
