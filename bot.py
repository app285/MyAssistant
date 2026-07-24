import asyncio
import os
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from groq import Groq

app = Flask(__name__)

# Environment variables orqali olish (xavfsizroq)
TOKEN = os.getenv("TELEGRAM_TOKEN", "8766736354:AAE732xf0BLuD76PUIuBYj5DS2QGedW_0TY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "8766736354:AAE732xf0BLuD76PUIuBYj5DS2QGedW_0TY")

# Global Application (serverless uchun bir marta yaratiladi)
application = Application.builder().token(TOKEN).build()
groq_client = Groq(api_key=GROQ_API_KEY)

# Handlerlar
async def start(update: Update, context):
    await update.message.reply_text("Assalomu alaykum! Men ishlayapman. Groq orqali javob beraman.")

async def handle_message(update: Update, context):
    user_text = update.message.text
    try:
        chat_completion = groq_client.chat.completions.create(
            messages=[{"role": "user", "content": user_text}],
            model="llama3-70b-8192",
        )
        answer = chat_completion.choices[0].message.content
        await update.message.reply_text(answer)
    except Exception as e:
        await update.message.reply_text(f"Xatolik: {str(e)}")

# Handlerlarni qo'shish (bir marta)
application.add_handler(CommandHandler("start", start))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

@app.route("/", methods=["POST", "GET"])
async def webhook():
    if request.method == "POST":
        try:
            json_data = request.get_json(force=True)
            update = Update.de_json(json_data, application.bot)
            
            # Har bir request uchun to'g'ri ishlov berish
            await application.initialize()
            await application.process_update(update)
            await application.shutdown()  # muhim!
            
            return "OK", 200
        except Exception as e:
            print(f"Error: {e}")
            return "ERROR", 500
    return "Bot is running and alive! ✅"

# Vercel uchun asinxron qo'llab-quvvatlash
if __name__ == "__main__":
    app.run()