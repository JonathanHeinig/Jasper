from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import random

TOKEN = "8518491594:AAH_RhH7UnjNZQJ38RHtVY8Uk23g2a1qLxQ"
CHAT_ID = 6986851797

words = [
    ("Abundant", "שופע", "There is abundant evidence supporting the theory."),
    ("Reluctant", "מהסס", "He was reluctant to admit his mistake."),
    ("Vivid", "חי, מוחשי", "She gave a vivid description of the event."),
]

async def send_word(context: ContextTypes.DEFAULT_TYPE):
    word = random.choice(words)

    text = f"""
📘 Word: {word[0]}
📖 Translation: {word[1]}
✏️ Example: {word[2]}
"""

    await context.bot.send_message(chat_id=CHAT_ID, text=text)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("הבוט התחיל לעבוד 💪")

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    # שליחה כל 8 שעות (3 פעמים ביום)
    app.job_queue.run_repeating(send_word, interval=28800, first=5)

    app.run_polling()

if __name__ == "__main__":
    main()
