import sys
import subprocess
import json

print("===================================")
print("Recon and OSINT Framework v1\n")

args = sys.argv

if "-u" not in args:
    print("Usage: python main.py -u <url> [-p parameter]")
    sys.exit(1)

target = args[args.index("-u") + 1]

param = None
if "-p" in args:
    param = args[args.index("-p") + 1]

results = {
    "target": target,
    "crawler": [],
    "xss": [],
    "sqli": [],
    "nmap": [],
    "shodan": []
}

print("[*] Running crawler...")
subprocess.run(
    ["python", "crawler.py", "-u", target, "-o", "crawler_output.txt"],
    check=False
)

print("[*] Running XSS scanner...")
subprocess.run(
    ["python", "xss_scanner.py", "-u", target],
    check=False
)

if param:
    print("[*] Running SQLi scanner...")
    subprocess.run(
        ["python", "sqli_scanner.py", "-u", target, "-p", param],
        check=False
    )
else:
    print("[!] SQLi skipped (no parameter provided)")

print("[*] Running Nmap scan...")
subprocess.run(
    ["python", "nmap_scan.py", "-t", target],
    check=False
)

print("[*] Running Shodan OSINT scan...")
subprocess.run(
    ["python", "shodan_scan.py", "-t", target],
    check=False
)

with open("recon_report.txt", "w") as f:
    f.write(f"Target: {target}\n\n")
    f.write("Crawler output: crawler_output.txt\n")
    f.write("XSS output: xss_report.txt\n")
    if param:
        f.write(f"SQLi tested parameter: {param}\n")
    else:
        f.write("SQLi not executed\n")
    f.write("Nmap output: nmap_report.json\n")
    f.write("Shodan output: shodan_report.json\n")

with open("recon_report.json", "w") as f:
    json.dump(results, f, indent=4)

print("\nRecon completed.")
