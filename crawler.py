import requests
from bs4 import BeautifulSoup
import sys
from urllib.parse import urlparse

print("====================================")
print("Basic Web Crawler\n")

args = sys.argv

if "-u" not in args:
    print("Usage: python crawler.py -u <url> [-o output.txt]")
    sys.exit(1)

url = args[args.index("-u") + 1]

output_file = None
if "-o" in args:
    output_file = args[args.index("-o") + 1]

visited = []

# extract base domain
base_domain = urlparse(url).netloc

def get_links(url):
    links = []

    try:
        response = requests.get(url)
    except:
        return links

    soup = BeautifulSoup(response.text, "html.parser")

    for a in soup.find_all("a"):
        href = a.get("href")

        if href and href.startswith("http"):
            link_domain = urlparse(href).netloc

            # ONLY same domain
            if link_domain == base_domain:
                links.append(href)

    return links

def crawl(url):
    if url in visited:
        return

    print("Visiting:", url)
    visited.append(url)

    links = get_links(url)

    for link in links:
        crawl(link)

crawl(url)

if output_file:
    with open(output_file, "w") as f:
        for u in visited:
            f.write(u + "\n")

print("\nDone.")
print("Total pages found:", len(visited))