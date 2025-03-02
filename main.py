from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging

# Enable logging to see errors
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Define your start command
def start(update, context):
    update.message.reply_text('Hello! I am your music bot. Send me a music command!')

def main():
    # Your bot's API Token
    token = 'YOUR_BOT_API_TOKEN'
    updater = Updater(token, use_context=True)

    dispatcher = updater.dispatcher

    # Define your handlers
    dispatcher.add_handler(CommandHandler("start", start))

    # Start the bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
