import asyncpg
import os
from dotenv import load_dotenv


load_dotenv()


class Database:
    def __init__(self):
        self.pool = None

    async def create_pool(self):
        '''Create connections pool (call with bot's initialization)'''
        self.pool = await asyncpg.create_pool(
            host=os.getenv('PGHOST'),
            database=os.getenv('PGDATABASE'),
            user=os.getenv('PGUSER'),
            password=os.getenv('PGPASSWORD'),
            ssl='require'
        )

    async def create_tables(self):
        '''Create table with first running'''
        async with self.pool.acquire() as conn:
            await conn.execute('''
                CREATE TABLE IF NOT EXISTS user_words (
                    id SERIAL PRIMARY KEY,
                    user_id BIGINT NOT NULL,
                    word TEXT NOT NULL,
                    transcription TEXT,
                    translation TEXT,
                    created_at TIMESTAMP DEFAULT NOW(),
                    UNIQUE (user_id, word)
                );
            ''')

    async def save_word(self, user_id: int, word: str, transcription: str = None, translation: str = None):
        '''Try to save the word to DB. Returns True if saved, False if exists'''
        async with self.pool.acquire() as conn:
            await conn.execute("""
                INSERT INTO user_words (user_id, word, transcription, translation)
                VALUES ($1, $2, $3, $4)
            """, user_id, word, transcription, translation)
