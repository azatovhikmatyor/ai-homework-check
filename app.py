from telegram import Update
from telegram.ext import Application, CommandHandler,ContextTypes, CallbackContext, MessageHandler, filters
from dotenv import load_dotenv
import os
import sqlite3

load_dotenv(dotenv_path=".env")

BOT_TOKEN = os.getenv("BOT_TOKEN")

# con.execute("""
#     create table users(
#         telegram_id text primary key,
#         username text,
#         first_name text,
#         last_name text);
# """)

# Function to handle the /start command
async def start(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    username = update.effective_user.username
    first_name = update.effective_user.first_name or ""
    last_name = update.effective_user.last_name or ""

    con = sqlite3.connect('db.sqlite3')
    db_id = con.execute("SELECT telegram_id FROM users where telegram_id=?;", (user_id,)).fetchone()
    if db_id is None:
        con.execute("""
            INSERT INTO users(telegram_id, username, first_name, last_name)
            VALUES (?, ?, ?, ?);
        """, (user_id, username, first_name, last_name)
        )
    
        print(f"User: {username} saved in the database.")
        con.commit()
    con.close()

    await update.message.reply_text("Hello! You have successfully interacted with this bot.")


from all import check_homework
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = str(update.effective_user.id)
    lesson_number = 3
    subject = 'ml'

    res = check_homework(user_id=user_id, lesson_number=lesson_number, subject=subject)
    await update.message.reply_text(f"Your Score: {res['score']}\n{res['feedback']}")


def main():
    # Create the Application object
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Add a command handler for /start
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Start the bot
    print("Bot started")
    application.run_polling()

if __name__ == "__main__":
    main()
