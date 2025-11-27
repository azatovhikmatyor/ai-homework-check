from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext
from dotenv import load_dotenv
import os


load_dotenv(dotenv_path=".env")

BOT_TOKEN = os.getenv("BOT_TOKEN")

# Function to handle the /start command
async def start(update: Update, context: CallbackContext):
    # Get the user's chat_id
    chat_id = update.effective_chat.id
    username = update.effective_chat.username or "Unknown"
    first_name = update.effective_chat.first_name or ""
    last_name = update.effective_chat.last_name or ""
    fullName = f"{first_name} {last_name}".strip()
    
    print(f"Name: {fullName}, User: {username}, Chat ID: {chat_id}")
    
    # Send a welcome message
    await update.message.reply_text("Hello! You have successfully interacted with this bot.")
    
    # Store chat_id in your database (this example just prints it)
    with open("chat_ids.txt", "a", encoding="utf-8") as file:
        file.write(f"{fullName},{username},{chat_id}\n")



def main():
    # Create the Application object
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Add a command handler for /start
    application.add_handler(CommandHandler("start", start))
    
    # Start the bot
    application.run_polling()

if __name__ == "__main__":
    main()
