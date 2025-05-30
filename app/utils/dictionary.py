import aiohttp
from pydantic import BaseModel


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
        self.translation_url = f'https://libretranslate.com/translate'
    
    async def _get_json(self, url: str, method: str = 'GET', payload: dict | None = None) -> dict | None:
        '''Get data in json format'''
        async with aiohttp.ClientSession() as session:
            try:
                async with (session.post(url, json=payload) if method == 'POST' else session.get(url)) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        print(f"\n🟡 Ответ от API ({url}):\n{data}\n")  # 🖨️ отладка
                        return data
            except aiohttp.ClientError as e:
                print(f"🔴 Ошибка aiohttp: {e}")
                return None
        return None

    async def get_word_data(self) -> dict | None:
        '''Get word data from dictionaryapi.dev'''
        data = await self._get_json(self.dictionary_url)
        if isinstance(data, list) and data:
            return data[0]
        return None
    
    async def get_word_translation(self) -> str | None:
        '''Trying to find word's translation in libretranslate.com API'''
        payload = {
            'q': self.word,
            'source': 'en',
            'target': 'ru',
            'format': 'text'
        }
        data = await self._get_json(self.translation_url, 'POST', payload)
        print(f"🔵 Ответ LibreTranslate: {data}")
        return data.get('translatedText') if data else None
            
    async def get_word_full_data(self) -> WordData | None:
        '''Returns dict includes word's transcription, translation, example & audio link'''
        data = await self.get_word_data()
        if not data:
            return None

        # Extracting transcription and audio
        transcription = None
        audio_url = None
        phonetics = data.get('phonetics')
        if phonetics and isinstance(phonetics, list):
            for item in phonetics:
                if not transcription and item.get('text'):
                    transcription = item['text']
                if not audio_url and item.get('audio'):
                    audio_url = item['audio']
        
        # Just in case if URL isn't start with protocol
        if audio_url and audio_url.startswith('//'):
            audio_url = 'https:' + audio_url
        
        # Extracting example in sentences
        example = None
        meanings = data.get('meanings')
        if meanings and isinstance(meanings, list):
            definitions = meanings[0].get('definitions')
            if definitions and isinstance(definitions, list):
                example = definitions[0].get('example')

        translation = await self.get_word_translation()

        return WordData(
            word=self.word,
            transcription=transcription,
            translation=translation,
            example=example,
            audio_url=audio_url
        )
