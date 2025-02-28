import requests
from bs4 import BeautifulSoup
import json
from urllib.parse import urljoin, urlparse

# Set of visited URLs to avoid duplicates
visited_urls = set()
scraped_data = []  # Store scraped content

def scrape_website(url, base_url, depth=1, max_depth=3):
    if url in visited_urls or depth > max_depth:
        return

    print(f"Scraping: {url}")
    visited_urls.add(url)

    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            print(f"Failed to fetch {url}: {response.status_code}")
            return

        soup = BeautifulSoup(response.text, "html.parser")

        # Extract page content
        content = {
            "url": url,
            "title": soup.title.string if soup.title else "No Title",
            "text": " ".join([p.text.strip() for p in soup.find_all("p")])[:1000],
        }

        # Save the extracted content
        scraped_data.append(content)

        # Find and scrape internal links
        links = []
        for a_tag in soup.find_all("a", href=True):
            link = urljoin(base_url, a_tag["href"])
            if is_valid_internal_link(link, base_url):
                links.append(link)

        for link in links:
            scrape_website(link, base_url, depth + 1, max_depth)

    except requests.exceptions.RequestException as e:
        print(f"Error scraping {url}: {e}")

def is_valid_internal_link(link, base_url):
    parsed_link = urlparse(link)
    parsed_base = urlparse(base_url)
    return parsed_link.netloc == parsed_base.netloc and link not in visited_urls

BASE_URL = "https://www.n60.ai/"

# Start scraping
scrape_website(BASE_URL, BASE_URL)

# Save extracted data to JSON
with open("scraped_data.json", "w", encoding="utf-8") as f:
    json.dump(scraped_data, f, indent=4, ensure_ascii=False)

print("✅ Scraping complete. Data saved to scraped_data.json.")
import json
import openai
import os



# Formatter
print("Starting formatter...")
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))  # New client
with open("scraped_data.json", "r", encoding="utf-8") as f:
    raw_data = json.load(f)
response = client.chat.completions.create(  # New API call
    model="gpt-4",
    messages=[{"role": "user", "content": f"Format this data into a readable summary: {raw_data}"}]
)
formatted = response.choices[0].message.content
with open("formatted_data.json", "w", encoding="utf-8") as f:
    json.dump(formatted, f, indent=4, ensure_ascii=False)
print("Formatted data saved to formatted_data.json")

import json
import openai
import os
from datetime import datetime  # Add this

# Your scraper code here
# ...

# Save extracted data to JSON
with open("scraped_data.json", "w", encoding="utf-8") as f:
    json.dump(scraped_data, f, indent=4, ensure_ascii=False)
print("✅ Scraping complete. Data saved to scraped_data.json.")

import json
import openai
import os
from datetime import datetime  # Add this

# Your scraper code here

# Save extracted data to JSON


import json
import openai
import os
import subprocess
from datetime import datetime

# Scraper code
# ...
with open("scraped_data.json", "w", encoding="utf-8") as f:
    json.dump(scraped_data, f, indent=4, ensure_ascii=False)
print("✅ Scraping complete. Data saved to scraped_data.json.")

# Formatter
print("Starting formatter...")
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
with open("scraped_data.json", "r", encoding="utf-8") as f:
    raw_data = json.load(f)
response = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": f"Format this data into a readable summary: {raw_data}"}]
)
formatted = response.choices[0].message.content
output = {
    "timestamp": datetime.now().isoformat(),
    "formatted_data": formatted
}
with open("formatted_data.json", "w", encoding="utf-8") as f:
    json.dump(output, f, indent=4, ensure_ascii=False)
print("Formatted data saved to formatted_data.json")

# Commit and push to GitHub
subprocess.run(["git", "add", "formatted_data.json"], check=True)
subprocess.run(["git", "commit", "-m", "Updated formatted_data.json with timestamp"], check=True)
subprocess.run(["git", "push", "origin", "main"], check=True)
print("Pushed formatted_data.json to GitHub")