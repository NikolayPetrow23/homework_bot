import os
from dotenv import load_dotenv

load_dotenv()

bot_token = os.getenv('TELEGRAM_TOKEN')
practicum_token = os.getenv('PRACTICUM_TOKEN')
id_chat = os.getenv('TELEGRAM_CHAT_ID')
