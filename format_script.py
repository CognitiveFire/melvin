import json

# Load scraped data
try:
    with open("scraped_data.json", "r", encoding="utf-8") as infile:
        scraped_data = json.load(infile)
except FileNotFoundError:
    print("Error: scraped_data.json not found.")
    scraped_data = []
except json.JSONDecodeError as e:
    print(f"Error reading scraped_data.json: {e}")
    scraped_data = []

# Check if data exists
if not scraped_data:
    print("Error: scraped_data.json is empty or not formatted correctly")
else:
    formatted_data = []

    for item in scraped_data:
        formatted_entry = {
            "prompt": f"Summarize this article: {item.get('title', 'No Title')}",
            "completion": item.get("text", "No Content")
        }
        formatted_data.append(formatted_entry)

    # Save formatted data
    with open("formatted_data.json", "w", encoding="utf-8") as outfile:
        json.dump(formatted_data, outfile, indent=4, ensure_ascii=False)

    print("✅ Formatted data saved to formatted_data.json!")
