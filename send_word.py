import json
import requests
import os
import sys


TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

if not TOKEN or not CHAT_ID:
    print("Missing TELEGRAM_TOKEN or TELEGRAM_CHAT_ID")
    sys.exit(1)


with open("words.json", encoding="utf-8") as f:
    words = json.load(f)


with open("state.json", encoding="utf-8") as f:
    state = json.load(f)

index = state.get("index", 0)


if index >= len(words):
    index = 0

word_data = words[index]


message = (
    f"📚 Daily Word of the Day\n\n"
    f"🔤 Word: {word_data['word']}\n"
    f"🇮🇱 Translation: {word_data['translation']}\n"
    f"💬 Example: {word_data['example']}"
)


url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

payload = {
    "chat_id": CHAT_ID,
    "text": message
}

response = requests.post(url, data=payload)

if response.status_code != 200:
    print("Failed to send message:", response.text)
    sys.exit(1)

print("Message sent successfully.")


state["index"] = index + 1

with open("state.json", "w", encoding="utf-8") as f:
    json.dump(state, f, ensure_ascii=False, indent=2)

print("State updated.")
