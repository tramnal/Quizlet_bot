import os
from dotenv import load_dotenv


load_dotenv()

class Settings:
    BOT_TOKEN: str = os.getenv('BOT_TOKEN')
    DB_URL: str = os.getenv('DATABASE_URL')

config = Settings()
