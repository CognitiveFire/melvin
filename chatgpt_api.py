import openai
import json
import os
import time

# ✅ Load OpenAI API Key from Railway environment variables
openai.api_key = os.getenv("OPENAI_API_KEY")

if not openai.api_key:
    raise ValueError("❌ OpenAI API key is missing! Make sure it's set in Railway.")

# ✅ Load the formatted data
try:
    with open("formatted_data.json", "r", encoding="utf-8") as file:
        formatted_data = json.load(file)
except FileNotFoundError:
    print("❌ Error: formatted_data.json not found.")
    formatted_data = []
except json.JSONDecodeError:
    print("❌ Error: formatted_data.json is not formatted correctly.")
    formatted_data = []

# ✅ Function to send data to OpenAI's ChatGPT API
def get_chatgpt_response(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful AI assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1000
        )
        return response["choices"][0]["message"]["content"]
    except openai.error.OpenAIError as e:
        print(f"❌ OpenAI API error: {e}")
        return None

# ✅ Log responses to a file for later reference
log_filename = "chatgpt_responses.log"

def log_response(prompt, response):
    with open(log_filename, "a", encoding="utf-8") as log_file:
        log_entry = f"📝 Prompt: {prompt}\n💬 Response: {response}\n---\n"
        log_file.write(log_entry)
        print(log_entry)  # Show in Railway logs

# ✅ Process each formatted entry and send it to OpenAI
for item in formatted_data:
    print(f"🔍 Processing: {item['prompt']}")
    
    # Send request to OpenAI
    chat_response = get_chatgpt_response(item['prompt'])
    
    if chat_response:
        log_response(item['prompt'], chat_response)
    else:
        print("⚠️ Failed to get a response from ChatGPT.\n")

# ✅ Print completion message
print("🚀 All formatted data has been processed!")
print(f"📄 Responses saved in: {log_filename}")
