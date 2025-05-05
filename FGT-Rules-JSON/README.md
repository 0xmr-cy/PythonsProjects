# 🔄 fgtrules.py

**A utility script to convert Fortinet firewall policy JSON exports into a structured CSV file.**

## 📄 Description

`fgtrules.py` is a command-line Python script designed to assist network and security engineers by transforming JSON exports of Fortinet firewall rules into a readable CSV format. This is particularly useful for audits, reporting, or rule analysis.

## 🚀 Features

- Parses JSON policy export from Fortinet firewalls
- Automatically detects all present fields
- Preserves logical order for common Fortinet rule attributes
- Converts list values into comma-separated strings
- Outputs clean, readable CSV files

## 📦 Requirements

- Python 3.7 or later

All dependencies used are part of the Python standard library (`argparse`, `json`, `csv`).

## 🛠 Usage

```bash
python fgtrules.py input_file.json output_file.csv
