from sqlalchemy import select

from database import async_session, UserWord


async def add_user_word(tg_id: int, word: str, transcription: str, translation: str, example: str, audio_url: str):
    '''Returns False if word already in DB, else - adds the word and returns True'''
    
    async with async_session() as session:
        existing = await session.scalar(
            select(UserWord).where(
                (UserWord.tg_id == tg_id) & (UserWord.word == word)
            )
        )

        if existing:
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



