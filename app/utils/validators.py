import re

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database import UserWord


def is_english_word(word:str) -> bool:
    '''Check - user's word is an English word'''
    return bool(re.fullmatch(r"[a-zA-Z'-]+", word) and isinstance(word, str))

async def is_word_in_db(tg_id: int, word: str, session: AsyncSession) -> bool:
    '''Check - user's word is in database already'''

    result = await session.execute(
        select(UserWord).where(
            (UserWord.tg_id == tg_id) &
            (UserWord.word == word.lower())
        )
    )
    return bool(result.scalar())
