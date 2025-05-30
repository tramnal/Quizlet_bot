from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

import app.keyboards as kb
from database import db_requests as rq
from utils import DictionaryAPI, WordData, WordValidator, ValidationResult

router = Router()

GREETINGS = {'привет', 'здравствуй', 'hello', 'hi', 'hey', 'хай', 'эй', 'здоров'}

class WordStates(StatesGroup):
    '''FSM for saving data state during dialog with user'''
    waiting_word = State()


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    '''Handles /start command, greets user and prompts for a word'''
    await state.clear()
    await message.answer(
        'Привет! Я Quzilet-бот, который поможет тебе в изучении английского.\n\n'
        'Отправь мне английское слово, и я покажу тебе его транскрипцию и перевод.\n\n'
        'О других возможностях и правилах, касающихся слов, ты можешь узнать нажав на "Справку".',
        reply_markup=kb.help_button()
    )


@router.message(F.text == 'Каталог')
async def catalog(message: Message):
    await message.answer('Выберите категорию товара', reply_markup=await kb.categories())


@router.callback_query(F.data.startswith('category_'))
async def category(callback: CallbackQuery):
    await callback.answer('Вы выбрали категорию')
    await callback.message.answer('Выберите товар по категории',
                                  reply_markup=await kb.items(callback.data.split('_')[1]))
