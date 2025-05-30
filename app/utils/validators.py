import re
from enum import Enum

from aiogram.types import Message

from app import keyboards as kb


class ValidationResult(Enum):
    '''Validation constants'''
    VALID = "valid"
    EMPTY = "empty"
    NOT_ENGLISH = "not_english"
    TOO_LONG = "too_long"


class WordValidator:
    '''User word validation'''
    def __init__(self, word: str):
        self.word = word.strip()

    def validate(self) -> ValidationResult:
        if not self.word or self.word.isspace():
            return ValidationResult.EMPTY
        if len(self.word) > 70:
            return ValidationResult.TOO_LONG
        if not re.fullmatch(r"[a-zA-Z'-]+", self.word):
            return ValidationResult.NOT_ENGLISH
        return ValidationResult.VALID


VALIDATION_MESSAGES: dict[ValidationResult, str] = {
    ValidationResult.EMPTY: '❗ Введи интересующее слово',
    ValidationResult.TOO_LONG: '🛑 Слишком длинное слово. Введи другое',
    ValidationResult.NOT_ENGLISH: '❌ 🇬🇧 Используй только английские буквы.'
}

async def validate_word(message: Message, word: str) -> str | None:
    '''Check the input. Returns None if incorrect'''
    word = word.strip()
    validation = WordValidator(word).validate()

    if validation != ValidationResult.VALID:
        await message.answer(VALIDATION_MESSAGES[validation], reply_markup=kb.help_button())
        return None

    return word
