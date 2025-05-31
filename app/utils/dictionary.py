import aiohttp
from pydantic import BaseModel
from googletrans import Translator
from enum import Enum

from app.config import config


class WordLookupResult(Enum):
    '''Results answers after checkup the word'''
    WIKI = '🤔 Возможно, это имя собственное. Попробуй прочитать об этом в Википедии:\n{}'
    NOT_FOUND = '❌ Возможно, это слово не существует. Проверь ввод и попробуй снова.'


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
        '''Generic HTTP request and getting data in JSON'''
        async with aiohttp.ClientSession() as session:
            try:
                async with session.request(method, url, json=payload, headers=headers) as resp:
                    text = await resp.text()
                    print(f"\n🟡 Запрос: {method} {url}")
                    if payload:
                        print(f"📦 Payload: {payload}")
                    print(f"🔵 Статус: {resp.status}")
                    print(f"🟠 Ответ (текст): {text}")
                    if resp.status == 200:
                        return await resp.json()
            except aiohttp.ClientError as e:
                print(f"🔴 aiohttp ошибка: {e}")
        return None

    async def _check_wiki_url(self, url: str) -> bool:
        '''Check if Wikipedia article exists for the word'''
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url) as resp:
                    return resp.status == 200
            except aiohttp.ClientError:
                return False

    async def get_word_data(self) -> dict | None:
        '''Get word data from dictionaryapi.dev'''
        return await self._get_json(self.dictionary_url)

    async def get_word_translation(self) -> str | None:
        '''Use "googletrans" library to translate word'''
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

    def _parse_phonetics(self, data: dict) -> tuple[str | None, str | None]:
        '''Parse transcription & audio_url from dictionaryapi.dev's data'''
        phonetics = data.get('phonetics', [])
        transcription, audio_url = None, None

        for item in phonetics:
            if not transcription and item.get('text'):
                transcription = item['text']
            if not audio_url and item.get('audio'):
                audio_url = item['audio']
        
        # Fix link from dictionaryapi.dev
        if audio_url and audio_url.startswith('//'):
            audio_url = 'https:' + audio_url

        return transcription, audio_url
    
    def _parse_example(self, data: dict) -> str | None:
        '''Parse example from dictionaryapi.dev's data'''
        meanings = data.get('meanings', [])
        for meaning in meanings:
            for definition in meaning.get('definitions', []):
                example = definition.get('example')
                if example:
                    return example
        return None

    async def get_word_full_data(self) -> WordData | None:
        '''
        Returns dict includes word's transcription, translation, example & audio link.
        Returns wiki-link for proper nouns if link exists,
        otherwise says word probably doesn't exist.
        '''
        data = await self.get_word_data()

        if not data or not isinstance(data, list):
            wiki_url = f'https://en.wikipedia.org/wiki/{self.word.capitalize()}'
            if await self._check_wiki_url(wiki_url):
                return WordData(
                    word=self.word,
                    translation=WordLookupResult.WIKI.value.format(wiki_url)
                )
            return WordData(
                word=self.word,
                translation=WordLookupResult.NOT_FOUND.value
            )

        data = data[0]

        transcription, audio_url = self._parse_phonetics(data)
        example = self._parse_example(data)
       
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
