import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

# Set of visited URLs to avoid duplicates
visited_urls = set()

# Function to scrape a webpage and find internal links
def scrape_website(url, base_url, depth=1, max_depth=3):
    if url in visited_urls or depth > max_depth:
        return {}

    print(f"Scraping: {url}")  # Debugging output
    visited_urls.add(url)  # Mark as visited

    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            print(f"Failed to fetch {url}: {response.status_code}")
            return {}

        soup = BeautifulSoup(response.text, "html.parser")

        # Extract relevant content
        content = {
            "url": url,
            "title": soup.title.string if soup.title else "No Title",
            "text": " ".join([p.text.strip() for p in soup.find_all("p")])[:1000],  # Limit text length
        }

        # Find all internal links
        links = []
        for a_tag in soup.find_all("a", href=True):
            link = urljoin(base_url, a_tag["href"])  # Resolve relative links
            if is_valid_internal_link(link, base_url):
                links.append(link)

        # Recursively scrape each found link
        for link in links:
            scrape_website(link, base_url, depth + 1, max_depth)

        return content

    except requests.exceptions.RequestException as e:
        print(f"Error scraping {url}: {e}")
        return {}

# Function to check if a link is an internal link
def is_valid_internal_link(link, base_url):
    parsed_link = urlparse(link)
    parsed_base = urlparse(base_url)

    return (
        parsed_link.netloc == parsed_base.netloc  # Only scrape same domain
        and link not in visited_urls  # Avoid re-scraping
    )

# Base URL of the website
BASE_URL = "https://www.n60.ai/"

# Start scraping
scraped_data = scrape_website(BASE_URL, BASE_URL)

print("Scraping complete.")

import json

# Convert set to list before saving
scraped_pages = list(visited_urls)

# Save scraped data
with open("scraped_data.json", "w", encoding="utf-8") as f:
    json.dump(scraped_pages, f, indent=4, ensure_ascii=False)

print("Scraping complete. Data saved to scraped_data.json.")



