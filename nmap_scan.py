import sys
import subprocess
import xml.etree.ElementTree as ET
import json

if "-t" not in sys.argv:
    print("Usage: python nmap_scan.py -t <target>")
    sys.exit(1)

target = sys.argv[sys.argv.index("-t") + 1]

output_file = "nmap_output.xml"

subprocess.run(
    ["nmap", "-sV", "-oX", output_file, target],
    check=False
)

tree = ET.parse(output_file)
root = tree.getroot()

results = {
    "target": target,
    "ports": []
}

for port in root.iter("port"):
    port_id = port.get("portid")
    protocol = port.get("protocol")

    service = port.find("service")
    if service is not None:
        name = service.get("name")
        version = service.get("version")
    else:
        name = None
        version = None

    results["ports"].append({
        "port": port_id,
        "protocol": protocol,
        "service": name,
        "version": version
    })

with open("nmap_report.json", "w") as f:
    json.dump(results, f, indent=4)

print("[+] Nmap scan completed")