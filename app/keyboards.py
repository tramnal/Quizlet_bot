from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


async def help_button() -> ReplyKeyboardMarkup:
    '''Shows help-button in the main menu'''
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text='💡 Справка')]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )


async def word_options() -> InlineKeyboardMarkup:
    '''Suggestions to user: show example, send audio or save the word'''
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='🟢 Добавить в словарь', callback_data='add')],
            [InlineKeyboardButton(text='📝 Пример использования', callback_data='example'),
             InlineKeyboardButton(text='🗣️ Прислать озвучку', callback_data='audio')]
        ]
    )
