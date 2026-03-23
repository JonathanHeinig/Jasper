import json
import requests
import os
import sys

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

if not TOKEN or not CHAT_ID:
    print("Missing TELEGRAM_TOKEN or TELEGRAM_CHAT_ID")
    sys.exit(1)

# ---------- טעינת מאגר מילים ----------
with open("wordsTwo.json", encoding="utf-8") as f:
    words = json.load(f)

# ---------- טעינת מצב ----------
if not os.path.exists("state.json"):
    state = {"index": 0}
    with open("state.json", "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)
else:
    with open("state.json", encoding="utf-8") as f:
        state = json.load(f)

index = state.get("index", 0)

# אם עברנו את הסוף — חוזרים להתחלה
index = index % len(words)

# 🔥 כאן היה חסר
word_data = words[index]

# ---------- בניית הודעה ----------
message = (
    f"📚 Daily Word of the Day\n\n"
    f"🔤 Word: {word_data['word']}\n"
    f"🇮🇱 Translation: {word_data['translation']}\n"
    f"💬 Example: {word_data['example']}"
)

# ---------- שליחה לטלגרם ----------
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

# ---------- עדכון אינדקס ----------
state["index"] = index + 1

with open("state.json", "w", encoding="utf-8") as f:
    json.dump(state, f, ensure_ascii=False, indent=2)

print("State updated.")
