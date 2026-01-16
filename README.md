# 🔍 Recon and OSINT Framework v1

Recon and OSINT Framework v1 is a Python-based CLI framework that automates
multiple reconnaissance and OSINT tasks into a single execution flow.

It combines web crawling, vulnerability scanning, network scanning,
and external OSINT lookups to provide a broader view of a target.

---

## Overview

Reconnaissance is not limited to a single technique.
Modern recon often involves combining application-level scanning,
network-level scanning, and external intelligence sources.

This framework brings those pieces together by automating:
- Web crawling
- XSS scanning
- Optional SQL injection testing
- Nmap scanning
- Shodan OSINT lookups

All modules are executed from one entry point.

---

## Features

- Centralized recon and OSINT orchestration
- Automated web crawler execution
- Integrated XSS scanner
- Optional SQL injection testing
- Network scanning via Nmap
- OSINT data collection via Shodan
- Consolidated text and JSON reporting
- Modular design for future expansion

---

## How It Works

The framework accepts a target URL and an optional parameter.

Execution flow:
1. Crawls the target website and saves discovered pages
2. Runs XSS scanning against the target
3. Executes SQL injection testing if a parameter is provided
4. Performs an Nmap scan on the target
5. Collects OSINT data using Shodan
6. Generates summary reports in text and JSON format

Each module is executed using subprocess calls, keeping orchestration
simple and readable.

---

## Usage

Run the framework like this  
python main.py -u <url>

To include SQL injection testing  
python main.py -u <url> -p <parameter>

The framework automatically handles which modules should run.

---

## Output

The framework generates:
- `crawler_output.txt` for discovered pages
- `xss_report.txt` for XSS findings
- SQLi scan output (if executed)
- `nmap_report.json` for network scan results
- `shodan_report.json` for OSINT data
- `recon_report.txt` as a human-readable summary
- `recon_report.json` as a structured report

---

## Requirements

- Python 3.x
- requests library
- All dependent scripts available in the same directory:
  - crawler.py
  - xss_scanner.py
  - sqli_scanner.py
  - nmap_scan.py
  - shodan_scan.py

Install dependencies if needed  
pip install requests

---

## Notes

- SQL injection testing is skipped if no parameter is provided
- Shodan module requires a valid API key
- Output quality depends on individual scanner modules
- Intended strictly for learning and authorized testing

---

## Final Thoughts

This framework focuses on understanding how recon and OSINT
fit together into a single workflow.

Once you can automate recon,
you stop thinking like a tool user
and start thinking like a tool builder.
