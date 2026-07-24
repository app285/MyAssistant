import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from groq import Groq

TOKEN = os.getenv("TELEGRAM_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

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

def main():
    application = Application.builder().token(TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot ishga tushdi...")
    application.run_polling()

if __name__ == "__main__":
    main()
