import aiohttp
from typing import Any, Dict, Optional

from pydantic import BaseModel


class WordData(BaseModel):
    '''Data validation class'''

    word: str
    transcription: Optional[str] = None
    translation: Optional[str] = None
    example: Optional[str] = None
    audio_url: Optional[str] = None


class DictionaryAPI:
    def __init__(self, word: str):
        self.word = word.lower()
        self.dictionary_url = f'https://api.dictionaryapi.dev/api/v2/entries/en/{self.word}'
        self.translation_url = f'https://libretranslate.com/translate'
    
    async def _get_json(self, url: str, method: str = 'GET', payload: Optional[dict] = None) -> Optional[Dict[str, Any]]:
        '''Get data in json format'''

        async with aiohttp.ClientSession() as session:
            async with (session.post(url, json=payload) if method == 'POST' else session.get(url)) as resp:
                if resp.status == 200:
                    return await resp.json()
                return None

    async def get_word_data(self) -> Optional[Dict[str, Any]]:
        '''Get word data from dictionaryapi.dev'''
        data = await self._get_json(self.dictionary_url)
        return data[0] if data else None
    
    async def get_word_translation(self) -> Optional[str]:
        '''Trying to find word's translation in libretranslate.com API'''

        payload = {
            'q': self.word,
            'source': 'en',
            'target': 'ru',
            'format': 'text'
        }
        data = await self._get_json(self.translation_url, 'POST', payload)
        return data.get('translatedText') if data else None
            
    async def get_word_full_data(self) -> Optional[WordData]:
        '''Returns dict includes word's transcription, translation, example & audio link'''

        data = await self.get_word_data()
        if not data:
            return None

        # Extracting transcription and audio
        transcription = None
        audio_url = None
        phonetics = data.get('phonetics')
        if phonetics:
            transcription = phonetics[0].get('text')
            audio_url = phonetics[0].get('audio')
        
        # Extracting example in sentences
        example = None
        meanings = data.get('meanings')
        if example:
            examples = meanings[0].get('definitions')
            if examples:
                example = examples[0].get('example')

        return WordData(
            word=self.word,
            transcription=transcription,
            translation=await self.get_word_translation(),
            example=example,
            audio_url=audio_url
        )
