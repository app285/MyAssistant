from flask import Flask, request
import os
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from groq import Groq

app = Flask(__name__)

TOKEN = os.getenv("TELEGRAM_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Telegram va Groq sozlamalari
application = Application.builder().token(TOKEN).build()
groq_client = Groq(api_key=GROQ_API_KEY)

# Global flag (app bir marta ishga tushishi uchun)
_initialized = False

async def initialize_application():
    global _initialized
    if not _initialized:
        await application.initialize()
        _initialized = True

async def start(update: Update, context):
    await update.message.reply_text("Assalomu alaykum! Bot ishlayapti.")

async def handle_message(update: Update, context):
    try:
        chat_completion = groq_client.chat.completions.create(
            messages=[{"role": "user", "content": update.message.text}],
            model="llama3-70b-8192",
        )
        answer = chat_completion.choices[0].message.content
        await update.message.reply_text(answer)
    except Exception as e:
        await update.message.reply_text("Xatolik yuz berdi.")

application.add_handler(CommandHandler("start", start))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

@app.route("/", methods=["POST", "GET"])
def webhook():
    if request.method == "POST":
        try:
            json_data = request.get_json(force=True)
            
            # Asinxron funksiyani Flask ichida to'g'ri bajarish
            async def process():
                await initialize_application()
                update = Update.de_json(json_data, application.bot)
                await application.process_update(update)

            asyncio.run(process())
            return "OK", 200
        except Exception as e:
            print(e)
            return "ERROR", 500
    return "Bot ishlayapti!"

if __name__ == "__main__":
    app.run()
