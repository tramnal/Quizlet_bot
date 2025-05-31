from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, ContentType, BufferedInputFile
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

import app.keyboards as kb
from app.database import db_requests as rq
from app.utils import WordData, validate_word, export_to_csv, MenuButtons

router = Router()


class DeleteStates(StatesGroup):
    waiting_for_word = State()
    confirm = State()


GREETINGS = {'привет', 'здравствуй', 'hello', 'hi', 'hey', 'хай', 'эй', 'здоров'}

async def send_greeting(message: Message, state: FSMContext) -> None:
    '''Sends greeting message and help button'''
    await state.clear()
    await message.answer(
        '👋 Привет! Я Quizlet-бот, который поможет тебе в изучении английского.\n\n'
        '📨 Отправь мне английское слово, и я покажу тебе его транскрипцию и перевод.\n\n'
        'ℹ️ О других возможностях и правилах, касающихся слов, ты можешь узнать, нажав на "Справку".',
        reply_markup=kb.main_menu()
    )

@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext) -> None:
    '''Handles /start command, greets user and prompts for a word'''
    await send_greeting(message, state)

@router.message(lambda message: message.text and any(message.text.lower().startswith(greet) for greet in GREETINGS))
async def greetings(message: Message, state: FSMContext) -> None:
    '''Handles other informal greets from user'''
    await send_greeting(message, state)

@router.message(F.text == 'Егор')
async def joke(message: Message) -> None:
    '''Пасхалка для Егорыча:)'''
    await message.answer_photo(
        photo='https://imgur.com/a/rpuoDjk',
        caption='Текнолоджыйя!',
        reply_markup=kb.main_menu()
    )

@router.message(F.text == MenuButtons.HELP)
async def help(message: Message) -> None:
    '''Display help info'''
    await message.answer(
        'ℹ️ Что я умею:\n\n'
        '🇬🇧 Найти и показать тебе перевод и транскрипцию английского слова\n'
        '📘 Привести пример использования\n'
        '🔊 Прислать озвучку найденного слова\n'
        '💾 Сохранить слово в словарь\n'
        '📁 Прислать твой словарь в файле, чтоб ты мог загрузить его на quizlet.com\n\n'
        '❗ Вводи английские слова (без цифр, символов, знаков препинания и пробелов)'
    )

@router.message(F.text == MenuButtons.MY_WORDS)
async def show_user_words(message: Message) -> None:
    '''Shows user words saved in database'''
    tg_id = message.from_user.id
    words = await rq.get_all_user_words(tg_id)

    if not words:
        await message.answer('📭 У тебя пока нет сохранённых слов...',
                                      reply_markup=kb.main_menu())
        return
    
    msg = '📚 <b>Твои слова:</b>\n\n' + '\n'.join(f'• {w.word}' for w in words)
    await message.answer(msg, parse_mode='HTML')
    await message.answer(
        '❔ Что хочешь делать дальше?\n'
        'Можешь перейти по одной из кнопок меню,\n'
        'либо продолжай вводить английские слова и добавлять их в словарь',
        reply_markup=kb.main_menu()
    )

@router.message(F.text == MenuButtons.DELETE_WORD)
async def ask_word_to_del(message: Message, state: FSMContext) -> None:
    '''Asks user to input the word for deleting'''
    await message.answer("✂️ Введи слово, которое хочешь удалить из словаря:",
                         reply_markup=kb.cancel_button())
    await state.set_state(DeleteStates.waiting_for_word)

@router.message(DeleteStates.confirm, F.text == MenuButtons.CANCEL)
async def cancel_clear_dict(message: Message, state: FSMContext):
    '''Cancels clear user's database'''
    await state.clear()
    await message.answer("❌ Очистка словаря отменена.", reply_markup=kb.main_menu())

@router.message(F.text == MenuButtons.CANCEL)
async def cancel_delete(message: Message, state: FSMContext) -> None:
    '''Cancels deleting the word'''
    await state.clear()
    await message.answer("❌ Удаление отменено.", reply_markup=kb.main_menu())

@router.message(F.text == MenuButtons.CLEAR_DICT)
async def ask_clear_dict(message: Message, state: FSMContext):
    '''Asks confirmation to clear user's dict'''
    await state.set_state(DeleteStates.confirm)
    await message.answer("⚠️ Ты точно хочешь удалить все слова из своего словаря?",
                         reply_markup=kb.confirm_clear_dict())

@router.message(F.text == MenuButtons.EXPORT)
async def send_csv(message: Message) -> None:
    '''Sends user dict in csv file'''
    tg_id = message.from_user.id
    csv_dict = await export_to_csv(tg_id)

    if csv_dict == None:
        await message.answer('📭 У тебя пока нет сохранённых слов...',
                             reply_markup=kb.main_menu())
        return
    
    await message.answer_document(
        document=BufferedInputFile(
            file=csv_dict.read(),
            filename='my_words.csv'
        ),
        caption='📄 Вот твой словарь. Можешь загрузить его на quizlet.com,\n'
        'чтобы создать карточки для изучения'
    )

@router.message(DeleteStates.confirm, F.text == '✅ Да')
async def confirm_clear_dict(message: Message, state: FSMContext):
    '''Confirms clear user's dict'''
    tg_id = message.from_user.id
    await rq.clear_user_db(tg_id)
    await state.clear()
    await message.answer('👌 Словарь очищен', reply_markup=kb.main_menu())

@router.message(DeleteStates.waiting_for_word)
async def delete_word(message: Message, state: FSMContext) -> None:
    '''Deletes user word if exists.'''
    word = message.text.strip().lower()
    tg_id = message.from_user.id

    deleted = await rq.delete_word_from_db(tg_id, word)
    if deleted:
        await message.answer(f'✅ Слово <b>{word}</b> удалено из словаря.',
                             parse_mode='HTML',
                             reply_markup=kb.main_menu())
    else:
        await message.answer(f'⚠️ Слово <b>{word}</b> не найдено в твоём словаре.',
                             parse_mode='HTML',
                             reply_markup=kb.main_menu())

    await state.clear()

@router.message(F.content_type == ContentType.TEXT)
async def handle_word(message: Message, state: FSMContext) -> None:
    '''The main handler. Validates word, fetches data and show buttons'''
    word = await validate_word(message, message.text)
    if not word:
        return
    
    tg_id = message.from_user.id
    word_data: WordData = await rq.get_word_from_db_or_api(tg_id, word)

    if not word_data.transcription and not word_data.example and not word_data.audio_url:
        await message.answer(
            f'⚠️ Не удалось найти подробностей по слову <b>{word_data.word}</b>\n\n'
            f'{word_data.translation}',
            parse_mode='HTML'
        )
        return
    
    await state.update_data(word_data=word_data.model_dump())
    await message.answer(
        f"📘 <b>{word_data.word}</b>\n"
        f"🔊 <u>Транскрипция</u>: <b>{word_data.transcription or '-нет транскрипции-'}</b>\n"
        f"🌍 <u>Перевод</u>: <b>{word_data.translation or '-нет перевода-'}</b>\n",
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
        await callback.message.answer(f'📖 Пример использования: {example}',
                                      reply_markup=kb.main_menu())
    else:
        await callback.message.answer(f'⚠️ Пример не найден.',
                                      reply_markup=kb.main_menu())

@router.callback_query(F.data == 'audio')
async def send_audio(callback: CallbackQuery, state: FSMContext) -> None:
    '''Sends pronunciation audio of word'''
    await callback.answer('🔊 Готовлю озвучку...')

    data = await state.get_data()
    audio_url = data.get('word_data', {}).get('audio_url')

    if audio_url:
        await callback.message.answer_audio(audio_url,
                                            reply_markup=kb.main_menu())
    else:
        await callback.message.answer(f'⚠️ Озвучка не найдена.',
                                      reply_markup=kb.main_menu())
    
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
        await callback.message.answer(text='👀 Хочешь ввести новое слово или заглянуть в словарь?',
                                      reply_markup=kb.main_menu())
    else:
        await callback.answer('📚 Слово уже в словаре', show_alert=True)
        await callback.message.answer(text='👀 Хочешь ввести новое слово или заглянуть в словарь?',
                                      reply_markup=kb.main_menu())

@router.message()
async def unsupported_message(message: Message) -> None:
    '''Handles another messages from user, like audio, voice, loco, pics and etc.'''
    await message.answer('⚠️ Я понимаю только текстовые сообщения — пришли, пожалуйста, английское слово.',
                         reply_markup=kb.main_menu())
