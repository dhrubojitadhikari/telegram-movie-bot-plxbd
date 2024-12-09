import os
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, filters, CallbackContext

# Token এবং Channel ID .env থেকে পড়া
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")  # যেমন: @YourChannelName

# Start Command Handler
def start(update: Update, context: CallbackContext):
    update.message.reply_text("🎬 Welcome! Search for movies by typing their name.")

# Search Command Handler
def search_movie(update: Update, context: CallbackContext):
    query = update.message.text.lower()
    chat_id = update.effective_chat.id

    # Fetch channel messages
    messages = context.bot.get_chat_history(CHANNEL_ID, limit=50)  # শেষ ৫০টা মেসেজ পড়া
    found = False

    for message in messages:
        if query in message.text.lower():
            # Forward message to user
            context.bot.forward_message(chat_id=chat_id, from_chat_id=CHANNEL_ID, message_id=message.message_id)
            found = True

    if not found:
        update.message.reply_text("❌ Sorry, no movies found matching your query!")

# Main Function
def main():
    updater = Updater(BOT_TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, search_movie))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
