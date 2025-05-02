# fgtrules.py

## 📄 Description

`fgtrules.py` is a Python script designed to extract, parse, and merge interface and routing table information from Fortigate firewalls. The result is a comprehensive CSV inventory file that includes interface configurations and associated static/BGP routes.

This tool is particularly useful for network administrators and engineers who need to audit or document Fortigate device configurations in a structured, machine-readable format.

---

## 🧰 Features

- Parses interface definitions from `show system interface` output
- Extracts IPv4, IPv6, VLAN, VDOM, status, and LAG information
- Parses routing table data from `get router info routing-table all` output
- Supports static and BGP routes, including recursive and directly connected paths
- Outputs a clean, structured CSV file linking interfaces and their routes

---

## 📦 Requirements

- Python 3.6 or higher  
- No external dependencies (uses only Python standard library)

---

## 📁 Input Files

You will need two CLI output files from your Fortigate firewall(s):

1. **Interface Configuration File**  
   Exported with:  
   ```shell
   show system interface


2. **Routing Table File**
   Exported with:

   ```shell
   get router info routing-table all


Save these files as `fortigate_config.txt` and `fortigate_route.txt`, or choose your own names and pass them as arguments to the script.

---

## ▶️ Usage

```bash
python fgtrules.py <config_file> <route_file> <output_file.csv>
```

**Example:**

```bash
python fgtrules.py fortigate_config.txt fortigate_route.txt inventory.csv
```

This will produce a CSV file (`inventory.csv`) containing merged data from interfaces and routes.

---

## 🧪 Example Output Columns

The output CSV file contains the following fields:

| Column        | Description                                |
| ------------- | ------------------------------------------ |
| FW            | Placeholder for firewall name              |
| IP FW         | Placeholder for firewall IP                |
| Fortimanager  | Placeholder for FortiManager association   |
| Fortianalyzer | Placeholder for FortiAnalyzer association  |
| VDOM          | Virtual domain name                        |
| Type          | Interface type (physical, vlan, loopback…) |
| Vlan          | VLAN ID if applicable                      |
| Interface     | Name of the interface                      |
| Network       | IPv4 network (CIDR) or DHCP                |
| Zone          | Placeholder for zone information           |
| Destination   | Destination prefix (from route table)      |
| Gateway       | Next-hop IP address                        |
| Protocole     | Routing protocol (S, S\*, B...)            |
| Status        | Interface status (up or down)              |
| LAG           | If part of LAG, the associated interface   |
| IPv6          | IPv6 address if present                    |

---

## ⚠️ Notes

* You must run this script in the same folder as your config and route files, or provide full paths.
* This script uses regular expressions to match and extract values — ensure that CLI output formatting has not been altered.
* `[DEBUG]` print statements are included for visibility into matching logic.

---

## 👨‍💻 Author

**0xmr-cy**
GitHub: [https://github.com/0xmr-cy](https://github.com/0xmr-cy)

---

## 🪪 License

This project is licensed under the **GNU General Public License v3.0**
See [LICENSE](https://www.gnu.org/licenses/gpl-3.0.en.html) for more details.

---

## 📆 Version History

* **v1.3 - 25/04/2025**

  * Improved BGP route matching
  * Added IPv6 support
  * Enhanced debug output

