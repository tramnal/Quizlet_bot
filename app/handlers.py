from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

import app.keyboards as kb
from app.database import db_requests as rq
from app.utils import WordData, validate_word

router = Router()

GREETINGS = {'привет', 'здравствуй', 'hello', 'hi', 'hey', 'хай', 'эй', 'здоров'}

async def send_greeting(message: Message, state: FSMContext) -> None:
    '''Sends greeting message and help button'''
    await state.clear()
    await message.answer(
        '👋 Привет! Я Quizlet-бот, который поможет тебе в изучении английского.\n\n'
        '📨 Отправь мне английское слово, и я покажу тебе его транскрипцию и перевод.\n\n'
        'ℹ️ О других возможностях и правилах, касающихся слов, ты можешь узнать, нажав на "Справку".',
        reply_markup=kb.help_button()
    )

@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext) -> None:
    '''Handles /start command, greets user and prompts for a word'''
    await send_greeting(message, state)

@router.message(lambda message: message.text and any(message.text.lower().startswith(greet) for greet in GREETINGS))
async def greetings(message: Message, state: FSMContext) -> None:
    '''Handles other informal greets from user'''
    await send_greeting(message, state)

@router.callback_query(F.data == 'help')
async def help(callback: CallbackQuery) -> None:
    '''Display help info'''
    await callback.message.edit_text(
        'ℹ️ Что я умею:\n'
        '🇬🇧 Найти и показать тебе перевод и транскрипцию английского слова\n'
        '📘 Привести пример использования\n'
        '🔊 Прислать озвучку найденного слова\n'
        '💾 Сохранить слово в словарь\n\n'
        '❗ Вводи английские слова (без цифр, символов, знаков препинания и пробелов)'
    )
    await callback.answer()

@router.message()
async def handle_word(message: Message, state: FSMContext) -> None:
    '''The main handler. Validates word, fetches data and show buttons'''
    word = await validate_word(message, message.text)
    if not word:
        return
    
    tg_id = message.from_user.id
    word_data: WordData = await rq.get_word_from_db_or_api(tg_id, word)

    if not word_data:
        await message.answer('⚠️ Не удалось найти слово. Попробуй другое.')
        return
    
    await state.update_data(word_data=word_data.model_dump())
    await message.answer(
        f"📘 <b>{word_data.word}</b>\n"
        f"🔊 Транскрипция: <i>{word_data.transcription or '-нет транскрипции-'}</i>\n"
        f"🌍 Перевод: <i>{word_data.translation or '-нет перевода-'}</i>\n",
        reply_markup=kb.word_options(),
        parse_mode='HTML'
    )

@router.callback_query(F.data == 'example')
async def send_example(callback: CallbackQuery, state: FSMContext) -> None:
    '''Sends example using in sentences'''
    await callback.answer('🔄 Ищу пример...')

    data = await state.get_data()
    example = data.get('word_data', {}).get('example')

    if example:
        await callback.message.answer(f'📖 Пример использования: {example}')
    else:
        await callback.message.answer(f'⚠️ Пример не найден.')

@router.callback_query(F.data == 'audio')
async def send_audio(callback: CallbackQuery, state: FSMContext) -> None:
    '''Sends pronunciation audio of word'''
    await callback.answer('🔊 Готовлю озвучку...')

    data = await state.get_data()
    audio_url = data.get('word_data', {}).get('audio_url')

    if audio_url:
        await callback.message.answer_audio(audio_url)
    else:
        await callback.message.answer(f'⚠️ Озвучка не найдена.')
    
@router.callback_query(F.data == 'add')
async def add_to_db(callback: CallbackQuery, state: FSMContext) -> None:
    '''Save word data to database'''
    data = await state.get_data()
    word_data = data.get('word_data')
    tg_id = callback.from_user.id

    added = await rq.add_user_word(
        tg_id=tg_id,
        word=word_data['word'],
        transcription=word_data.get('transcription') or '',
        translation=word_data.get('translation') or '',
        example=word_data.get('example') or '',
        audio_url=word_data.get('audio_url') or ''
    )

    if added:
        await callback.answer('✅ Слово сохранено!')
    else:
        await callback.answer('📚 Слово уже в словаре', show_alert=True)
