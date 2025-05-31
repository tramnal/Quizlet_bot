from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

from utils import MenuButtons

def main_menu():
    '''Shows the main control keyboard'''
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=MenuButtons.MY_WORDS),
             KeyboardButton(text=MenuButtons.EXPORT)],
            [KeyboardButton(text=MenuButtons.DELETE_WORD),
             KeyboardButton(text=MenuButtons.CLEAR_DICT),
             KeyboardButton(text=MenuButtons.HELP)],
        ],
        resize_keyboard=True
    )

def help_keyboard() -> InlineKeyboardMarkup:
    '''Shows help-button for additional info and rules'''
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=MenuButtons.HELP, callback_data='help')]
        ]
    )

def word_options() -> InlineKeyboardMarkup:
    '''Suggestions to user: show example, send audio or save the word'''
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=MenuButtons.ADD, callback_data='add')],
            [InlineKeyboardButton(text=MenuButtons.EXAMPLE, callback_data='example'),
             InlineKeyboardButton(text=MenuButtons.AUDIO, callback_data='audio')]
        ]
    )

def cancel_button():
    '''Cancels deleting if user changed mind'''
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=MenuButtons.CANCEL)]],
        resize_keyboard=True,
        one_time_keyboard=True
    )

def confirm_clear_dict() -> ReplyKeyboardMarkup:
    '''Confirms clear user's database'''
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text='✅ Да'), KeyboardButton(text=MenuButtons.CANCEL)]
        ],
        resize_keyboard=True
    )
