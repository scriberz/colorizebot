# Скопируйте этот файл в config.py и заполните своими значениями
# Или используйте переменные окружения через .env файл

import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('TOKEN', 'YOUR_TELEGRAM_BOT_TOKEN')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', 'YOUR_GEMINI_API_KEY')

