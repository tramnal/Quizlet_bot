from sqlalchemy import select

from app.database import async_session, UserWord
from app.utils import DictionaryAPI, WordData


async def is_word_in_db(session, tg_id: int, word: str) -> UserWord | None:
    '''Check, is the word already in DB or not yet (reuse session)'''
    word = word.lower()
    return await session.scalar(
        select(UserWord).where(
            (UserWord.tg_id == tg_id) & (UserWord.word == word)
        )
    )

async def add_user_word(tg_id: int, word: str, transcription: str, translation: str, example: str, audio_url: str) -> bool:
    '''Returns False if word already in DB, otherwise adds the word and returns True'''
    word = word.lower()
    async with async_session() as session:
        if await is_word_in_db(session, tg_id, word):
            return False

        new_word = UserWord(
            tg_id=tg_id,
            word=word,
            transcription=transcription,
            translation=translation,
            example=example,
            audio_url=audio_url
        )
        session.add(new_word)
        await session.commit()
        return True

async def get_word_from_db_or_api(tg_id: int, word: str) -> WordData | None:
    '''Returns word data either from database or API'''
    word = word.lower()

    # Check the database
    async with async_session() as session:
        existing = await is_word_in_db(session, tg_id, word)
        if existing:
            return WordData(
                word=existing.word,
                transcription=existing.transcription,
                translation=existing.translation,
                example=existing.example,
                audio_url=existing.audio_url
            )
    
    # If not exist in DB - go to API
    api = DictionaryAPI(word)
    return await api.get_word_full_data()
