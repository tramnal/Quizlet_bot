from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton


def main_menu():
    '''Shows the main control keyboard'''
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text='📚 Мои слова'),
             KeyboardButton(text='📤 Экспорт словаря')],
            [KeyboardButton(text='🗑️ Удалить слово'),
             KeyboardButton(text='🧹 Очистить словарь'),
             KeyboardButton(text='💡 Справка')],
        ],
        resize_keyboard=True
    )

def help_keyboard() -> InlineKeyboardMarkup:
    '''Shows help-button for additional info and rules'''
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='💡 Справка', callback_data='help')],
            [InlineKeyboardButton(text='📚 Мой словарь', callback_data='my_dict')]
        ]
    )

def word_options() -> InlineKeyboardMarkup:
    '''Suggestions to user: show example, send audio or save the word'''
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='🟢 Добавить в словарь', callback_data='add')],
            [InlineKeyboardButton(text='📝 Пример', callback_data='example'),
             InlineKeyboardButton(text='🗣️ Озвучка', callback_data='audio')]
        ]
    )

def cancel_button():
    '''Cancels deleting if user changed mind'''
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text='🔙 Отмена')]],
        resize_keyboard=True,
        one_time_keyboard=True
    )

def confirm_clear_dict() -> ReplyKeyboardMarkup:
    '''Confirms clear user's database'''
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text='✅ Да'), KeyboardButton(text='🔙 Отмена')]
        ],
        resize_keyboard=True
    )
