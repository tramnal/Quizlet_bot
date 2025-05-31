import re

from aiogram.types import Message

from utils import ValidationResult
from app import keyboards as kb


class WordValidator:
    '''User word validation'''
    BASE_REGEX = re.compile(r'^(?!-+$)[a-zA-Z-]{2,}$')

    def __init__(self, word: str):
        self.word = word.strip()

    def validate(self) -> ValidationResult:
        if not self.word:
            return ValidationResult.EMPTY
        if len(self.word) > 70:
            return ValidationResult.TOO_LONG
        if not self.BASE_REGEX.fullmatch(self.word):
            return ValidationResult.NOT_ENGLISH
        if "-" in self.word and any(len(part) < 2 for part in self.word.split("-")):
            return ValidationResult.INVALID_PARTS
        return ValidationResult.VALID


async def validate_word(message: Message, word: str) -> str | None:
    '''Check the input. Returns None if incorrect'''
    word = word.strip()
    validation = WordValidator(word).validate()

    if validation != ValidationResult.VALID:
        await message.answer(validation.value, reply_markup=kb.main_menu())
        return None

    return word
