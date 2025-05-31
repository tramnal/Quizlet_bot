from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def help_button() -> InlineKeyboardMarkup:
    '''Shows help-button for additional info and rules'''
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='💡 Справка', callback_data='help')]
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
