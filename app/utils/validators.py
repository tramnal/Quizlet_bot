import re
from enum import Enum


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
