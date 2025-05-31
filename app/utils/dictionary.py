import aiohttp
from pydantic import BaseModel
from googletrans import Translator

from app.config import config


class WordData(BaseModel):
    '''Data validation class'''
    word: str
    transcription: str | None = None
    translation: str | None = None
    example: str | None = None
    audio_url: str | None = None


class DictionaryAPI:
    def __init__(self, word: str):
        self.word = word.lower()
        self.dictionary_url = f'https://api.dictionaryapi.dev/api/v2/entries/en/{self.word}'
        self.translator = Translator()
        self.twinword_url = f'https://twinword-word-graph-dictionary.p.rapidapi.com/example/?entry={self.word}'
        self.twinword_key = config.TWINWORD_API_KEY

    async def _get_json(self, url: str, method: str = 'GET', payload: dict | None = None,
                        headers: dict | None = None) -> dict | None:
        '''Get data in json format'''
        async with aiohttp.ClientSession() as session:
            try:
                if method == 'POST':
                    async with session.post(url, json=payload, headers=headers) as resp:
                        status = resp.status
                        text = await resp.text()
                else:
                    async with session.get(url, headers=headers) as resp:
                        status = resp.status
                        text = await resp.text()

                print(f"\n🟡 Запрос: {method} {url}")
                if payload:
                    print(f"📦 Payload: {payload}")
                print(f"🔵 Статус: {status}")
                print(f"🟠 Ответ (текст): {text}")

                if status == 200:
                    return await resp.json()

            except aiohttp.ClientError as e:
                print(f"🔴 aiohttp ошибка: {e}")
                return None

        return None

    async def get_word_data(self) -> dict | None:
        '''Get word data from dictionaryapi.dev'''
        return await self._get_json(self.dictionary_url)

    async def get_word_translation(self) -> str | None:
        '''Use googletrans library to translate word'''
        try:
            result = await self.translator.translate(self.word, src='en', dest='ru')
            print(f"🔵 Перевод с Google Translate: {result.text}")
            return result.text
        except Exception as e:
            print(f"🔴 Ошибка перевода: {e}")
            return None

    async def get_example_from_twinword(self) -> str | None:
        '''Fallback: Get example sentence from Twinword API if there is no via dictionaryapi.dev'''
        headers = {
            'X-RapidAPI-Key': self.twinword_key,
            'X-RapidAPI-Host': 'twinword-word-graph-dictionary.p.rapidapi.com'
        }
        data = await self._get_json(self.twinword_url, headers=headers)
        if data and 'example' in data:
            examples = data['example']
            if isinstance(examples, list) and examples:
                return examples[0]
        return None

    async def get_word_full_data(self) -> WordData | None:
        '''
        Returns dict includes word's transcription, translation, example & audio link.
        Returns wiki-link for proper nouns.
        '''
        data = await self.get_word_data()
        if not data or not isinstance(data, list):
            wiki_url = f'https://en.wikipedia.org/wiki/{self.word.capitalize()}'
            return WordData(
                word=self.word,
                translation=f'🤔 Возможно, это имя собственное. Попробуй прочитать об этом в Википедии:\n{wiki_url}'
            )
        data = data[0]

        # Extract transcription and audio
        transcription = None
        audio_url = None
        phonetics = data.get('phonetics')
        if phonetics and isinstance(phonetics, list):
            for item in phonetics:
                if not transcription and item.get('text'):
                    transcription = item['text']
                if not audio_url and item.get('audio'):
                    audio_url = item['audio']
        
        # Fix link from dictionaryapi.dev
        if audio_url and audio_url.startswith('//'):
            audio_url = 'https:' + audio_url

        # Extract example
        example = None
        meanings = data.get('meanings')
        if meanings and isinstance(meanings, list):
            definitions = meanings[0].get('definitions')
            if definitions and isinstance(definitions, list):
                example = definitions[0].get('example')

        if not example:  # fallback via TwinwordAPI
            example = await self.get_example_from_twinword()

        translation = await self.get_word_translation()

        return WordData(
            word=self.word,
            transcription=transcription,
            translation=translation,
            example=example,
            audio_url=audio_url
        )
