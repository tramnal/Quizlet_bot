import aiohttp
from typing import Optional


class UserWordData:
    def __init__(self, word: str):
        self.word = word
        self.dictionary_url = f'https://api.dictionaryapi.dev/api/v2/entries/en/{word}'
        self.translation_url = f'https://libretranslate.com/translate'

    async def get_word_data(self) -> Optional[dict]:
        '''Trying to get data from dictionaryapi.dev'''
        async with aiohttp.ClientSession() as session:
            async with session.get(self.dictionary_url) as resp:
                if resp.status == 200:
                    data = resp.json()
                    return data[0] if data else None
                return None
    
    async def get_word_translation(self) -> Optional[dict]:
        '''Trying to find word's translation in libretranslate.com API'''

        payload = {
            'q': self.word,
            'source': 'en',
            'target': 'ru',
            'format': 'text'
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(self.translation_url, json=payload) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    return data.get('translatedText')
                return None
            
    async def get_word_full_data(self) -> Optional[dict]:
        '''Returns dict includes word's transcription, translation, example & audio link'''

        data = await self.get_word_data()
        if not data:
            return None
        
        transcription = None
        example = None
        audio_url = None

        phonetics = data.get('phonetics')
        if phonetics:
            transcription = phonetics[0].get('text')
            audio_url = phonetics[0].get('audio')
        
        meanings = data.get('meanings')
        if example:
            examples = meanings[0].get('definitions')
            if examples:
                example = examples[0].get('example')
        
        translation = await self.get_word_translation()

        return {
            "word": self.word,
            "transcription": transcription,
            "translation": translation,
            "example": example,
            "audio_url": audio_url
        }
