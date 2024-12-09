import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Token এবং Channel ID .env থেকে পড়া
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")  # যেমন: @YourChannelName

# Start Command Handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🎬 Welcome! Search for movies by typing their name.")

# Search Command Handler
async def search_movie(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text.lower()
    chat_id = update.effective_chat.id

    # Fetch channel messages
    found = False
    async for message in context.bot.get_chat_history(CHANNEL_ID, limit=50):
        if query in message.text.lower():
            # Forward message to user
            await context.bot.forward_message(chat_id=chat_id, from_chat_id=CHANNEL_ID, message_id=message.message_id)
            found = True

    if not found:
        await update.message.reply_text("❌ Sorry, no movies found matching your query!")

# Main Function
def main():
    # Application তৈরি করুন
    application = Application.builder().token(BOT_TOKEN).build()

    # Command এবং Message Handler যোগ করুন
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, search_movie))

    # Bot চালু করুন
    application.run_polling()

if __name__ == "__main__":
    main()
