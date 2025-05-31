from enum import Enum


class ValidationResult(Enum):
    '''Validation outcomes with messages as values'''
    VALID = None
    EMPTY = '❗ Введи интересующее слово'
    TOO_LONG = '🛑 Слишком длинное слово. Введи другое'
    NOT_ENGLISH = '❌ 🇬🇧 Используй только английские буквы (допускается дефис в середине слова).'
    INVALID_PARTS = '⚠️ Каждая часть слова должна быть минимум из 2 букв'


class MenuButtons(str, Enum):
    EXPORT: str = '📤 Экспорт словаря'
    MY_WORDS: str = '📚 Мои слова'
    DELETE_WORD: str = '🗑️ Удалить слово'
    CLEAR_DICT: str = '🧹 Очистить словарь'
    CANCEL: str = '🔙 Отмена'
    HELP: str = '💡 Справка'
    ADD: str = '🟢 Добавить в словарь'
    EXAMPLE: str = '📝 Пример'
    AUDIO: str = '🗣️ Озвучка'
