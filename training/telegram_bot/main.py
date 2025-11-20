from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext

# Your bot token from BotFather
BOT_TOKEN = "7911993686:AAFJJx1MO85thuENDq1qWemNZRlyhBt2kco"

# Function to handle the /start command
async def start(update: Update, context: CallbackContext):
    # Get the user's chat_id
    chat_id = update.effective_chat.id
    username = update.effective_chat.username
    print(update.effective_chat)
    print(f"User: {username}, Chat ID: {chat_id}")
    
    # Send a welcome message
    await update.message.reply_text("Hello! You have successfully interacted with this bot.")
    
    # Store chat_id in your database (this example just prints it)
    with open("chat_ids.txt", "a") as file:
        file.write(f"{username},{chat_id}\n")

def main():
    # Create the Application object
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Add a command handler for /start
    application.add_handler(CommandHandler("start", start))
    
    # Start the bot
    application.run_polling()

if __name__ == "__main__":
    main()
