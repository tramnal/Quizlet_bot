import re

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database import UserWord


def is_english_word(word:str) -> bool:
    '''Check - user's word is an English word'''
    return bool(re.fullmatch(r"[a-zA-Z'-]+", word) and isinstance(word, str))
