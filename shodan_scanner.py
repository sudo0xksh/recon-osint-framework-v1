import sys
import shodan
import json
import socket
import os

print("===================================")
print("Shodan OSINT Scanner\n")

args = sys.argv

if "-t" not in args:
    print("Usage: python shodan_scan.py -t <target>")
    sys.exit(1)

target = args[args.index("-t") + 1]

api_key = os.getenv("SHODAN_API_KEY")
if not api_key:
    print("SHODAN_API_KEY not set")
    sys.exit(1)

try:
    ip = socket.gethostbyname(target)
except:
    print("Could not resolve target")
    sys.exit(1)

api = shodan.Shodan(api_key)

try:
    result = api.host(ip)

    data = {
        "target": target,
        "ip": ip,
        "organization": result.get("org"),
        "isp": result.get("isp"),
        "ports": result.get("ports"),
        "banners": []
    }

    for service in result.get("data", []):
        data["banners"].append({
            "port": service.get("port"),
            "product": service.get("product"),
            "version": service.get("version")
        })

    with open("shodan_report.json", "w") as f:
        json.dump(data, f, indent=4)

    print("[+] Shodan data saved to shodan_report.json")

except shodan.APIError as e:
    print("Shodan error:", e)
