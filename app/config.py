import os
from dataclasses import dataclass
from dotenv import load_dotenv


load_dotenv()

@dataclass
class Settings:
    BOT_TOKEN: str = os.getenv('BOT_TOKEN')
    DB_URL: str = os.getenv('DATABASE_URL')
    TWINWORD_API_KEY: str = os.getenv('TWINWORD_API_KEY')

config = Settings()
