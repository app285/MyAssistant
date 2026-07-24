from flask import Flask, request
import os
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from groq import Groq

app = Flask(__name__)

# Environment Variables orqali olish
TOKEN = os.getenv("TELEGRAM_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

application = Application.builder().token(TOKEN).build()
groq_client = Groq(api_key=GROQ_API_KEY)

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
async def webhook():
    if request.method == "POST":
        try:
            update = Update.de_json(request.get_json(force=True), application.bot)
            await application.initialize()
            await application.process_update(update)
            await application.shutdown()
            return "OK", 200
        except Exception as e:
            print(e)
            return "ERROR", 500
    return "Bot ishlayapti!"

if __name__ == "__main__":
    app.run()
