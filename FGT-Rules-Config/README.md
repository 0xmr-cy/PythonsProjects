This Python script parses FortiGate firewall configuration files and extracts firewall policies into a CSV format. It is useful for auditing, reporting, or migrating FortiGate firewall policies.

## Features

- Extracts policy blocks from `config firewall policy` sections.
- Saves output to a CSV file (`policies-out2.csv`).
- Automatically detects and organizes all unique keys used in policy definitions.

## Requirements

- Python 3.x

## Usage

```bash
python fortigate.py policy-conf.txt
```

Replace policy-conf.txt with the path to your FortiGate configuration file.

##Output

The output file policies-out2.csv will contain:

A header row with id followed by all detected policy keys (e.g. srcintf, dstintf, action, etc.).
One line per policy, with values extracted from the configuration.

##Example

Given a FortiGate config snippet like:

config firewall policy
    edit 1
        set srcintf "port1"
        set dstintf "port2"
        set action accept
    next
    edit 2
        set srcintf "port3"
        set dstintf "port4"
        set action deny
    next
end
The resulting CSV will look like:

id,srcintf,dstintf,action
1,port1,port2,accept
2,port3,port4,deny

##License

This project is licensed under the GNU General Public License v3.0 - see the LICENSE file for details.
