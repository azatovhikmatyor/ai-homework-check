import requests
from dotenv import load_dotenv
import os
from utils import logger

load_dotenv(dotenv_path=".env")

def split_text(text):
    """
    Splits the given text into chunks no longer than 4096 characters (Telegram's limit).
    """
    max_length = 4096
    return [text[i:i + max_length] for i in range(0, len(text), max_length)]

class Telegram:
    BOT_TOKEN = os.getenv("BOT_TOKEN")

    def __init__(self, chat_id, message):
        self.chat_id = chat_id
        self.message = message
        self.url = f"https://api.telegram.org/bot{self.BOT_TOKEN}/sendMessage"

    def send_message(self, message):
        """
        Sends a single message to the specified chat ID.
        """
        payload = {
            "chat_id": self.chat_id,
            "text": message
        }
        response = requests.post(self.url, json=payload, timeout=20)
        if response.status_code == 200:
            print(f"Message sent successfully to chat ID: {self.chat_id}")
        else:
            logger.error(f"Failed to send message to chat ID {self.chat_id}, {response.text}")

    def send_feedback(self):
        """
        Splits the message into manageable chunks and sends them sequentially.
        """
        message_chunks = split_text(self.message)
        for chunk in message_chunks:
            self.send_message(chunk)


if __name__ == "__main__":

    chat_id = "606689265"

    user = Telegram(chat_id=chat_id, message="message")
    user.send_feedback()
