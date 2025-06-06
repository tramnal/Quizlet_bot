from sqlalchemy import select, delete

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

async def add_user_word(
        tg_id: int,
        word: str,
        transcription: str,
        translation: str,
        example: str,
        audio_url: str
        ) -> bool:
    '''
    Returns False if word already in database,
    otherwise adds the word and returns True
    '''
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

async def get_all_user_words(tg_id: int) -> list[UserWord]:
    '''Returns user words or replies there is no words yet'''
    async with async_session() as session:
        user_words = select(UserWord).where(UserWord.tg_id == tg_id).order_by(UserWord.word)
        result = await session.execute(user_words)
        return result.scalars().all()
    
async def delete_word_from_db(tg_id: int, word: str) -> bool:
    '''Deletes written word from database'''
    async with async_session() as session:
        del_action = delete(UserWord).where(
            UserWord.tg_id == tg_id,
            UserWord.word == word.lower().strip()
        )
        result = await session.execute(del_action)
        await session.commit()
        return result.rowcount > 0
    
async def clear_user_db(tg_id: int) -> bool:
    '''Deletes all user words from database'''
    async with async_session() as session:
        await session.execute(delete(UserWord).where(UserWord.tg_id == tg_id))
        await session.commit()
