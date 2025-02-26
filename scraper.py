import requests
from bs4 import BeautifulSoup
import json
from urllib.parse import urljoin, urlparse

# Set of visited URLs to avoid duplicates
visited_urls = set()

def scrape_website(url, base_url, depth=1, max_depth=3):
    if url in visited_urls or depth > max_depth:
        return {}

    print(f"Scraping: {url}")
    visited_urls.add(url)

    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            print(f"Failed to fetch {url}: {response.status_code}")
            return {}

        soup = BeautifulSoup(response.text, "html.parser")

        content = {
            "url": url,
            "title": soup.title.string if soup.title else "No Title",
            "text": " ".join([p.text.strip() for p in soup.find_all("p")])[:1000],
        }

        links = []
        for a_tag in soup.find_all("a", href=True):
            link = urljoin(base_url, a_tag["href"])
            if is_valid_internal_link(link, base_url):
                links.append(link)

        for link in links:
            scrape_website(link, base_url, depth + 1, max_depth)

        return content

    except requests.exceptions.RequestException as e:
        print(f"Error scraping {url}: {e}")
        return {}

def is_valid_internal_link(link, base_url):
    parsed_link = urlparse(link)
    parsed_base = urlparse(base_url)
    return parsed_link.netloc == parsed_base.netloc and link not in visited_urls

BASE_URL = "https://www.n60.ai/"
scraped_data = scrape_website(BASE_URL, BASE_URL)

with open("scraped_data.json", "w", encoding="utf-8") as f:
    json.dump(list(visited_urls), f, indent=4, ensure_ascii=False)

print("Scraping complete. Data saved to scraped_data.json.")
