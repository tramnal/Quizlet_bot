import aiohttp


async def get_user_word_data(word: str) -> dict | None:
    '''Trying to find word's data in dictionary API'''

    url = f'https://api.dictionaryapi.dev/api/v2/entries/en/{word}'
    async with aiohttp.ClientSession as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                return await resp.json()
            return None
