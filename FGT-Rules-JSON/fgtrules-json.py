#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Name        : fgtrules-json.py
Description : Script allowing the transposition of Fortinet rules into JSON export in a CSV file 
Autor       : 0xmr-cy
Date        : 28/04/2025
Version     : 1.1
License     : GNU General Public License v3.0

Copyright (c) 2025 0xmr-cy
"""

import json
import csv
import argparse

def main():
    parser = argparse.ArgumentParser(description='Convert JSON file to CSV')
    parser.add_argument('input_json', help='Path to the input JSON file')
    parser.add_argument('output_csv', help='Path to the output CSV file')
    args = parser.parse_args()

    # Lecture du fichier JSON
    with open(args.input_json, 'r', encoding='utf-8') as f:
        json_data = json.load(f)

    # Déterminer dynamiquement tous les champs rencontrés (avec un ordre de base)
    base_fields = [
        "Policy", "From", "To", "Source", "Destination", "Schedule", "Service", "Action",
        "IP Pool", "NAT", "Type", "Security Profiles", "Log", "Bytes", "Interface Pair"
    ]
    
    # Générer dynamiquement les colonnes existantes selon le JSON
    fieldnames = list({key for entry in json_data for key in entry.keys()})
    # Garder l'ordre défini dans base_fields, les autres seront ajoutés à la fin
    ordered_fieldnames = base_fields + [f for f in fieldnames if f not in base_fields]

    # Écriture dans le CSV
    with open(args.output_csv, mode='w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=ordered_fieldnames)
        writer.writeheader()

        for entry in json_data:
            # Convertir les listes en chaînes séparées par des virgules
            row = {key: ', '.join(value) if isinstance(value, list) else value for key, value in entry.items()}
            # Ajouter les champs manquants avec une valeur vide
            for field in ordered_fieldnames:
                row.setdefault(field, "")
            writer.writerow(row)

    print(f"Conversion completed. CSV file generated : {args.output_csv}")

if __name__ == "__main__":
    main()
