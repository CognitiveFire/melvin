import json
import os

# Check if the file exists before reading
if not os.path.exists("scraped_data.json"):
    print("Error: scraped_data.json not found. Run the scraper first!")
    exit()

# Load scraped data
with open("scraped_data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Format and clean up the scraped content
formatted_data = []
for page in data:
    if isinstance(page, dict):  # Ensure we're working with a dictionary
        formatted_data.append({
            "URL": page.get("url", "N/A"),
            "Title": page.get("title", "No Title"),
            "Content": page.get("text", "").replace("\n", " ").strip()  # Remove newlines
        })

# Save formatted data
with open("formatted_data.json", "w", encoding="utf-8") as f:
    json.dump(formatted_data, f, indent=4, ensure_ascii=False)

print("Formatted data saved to formatted_data.json.")
