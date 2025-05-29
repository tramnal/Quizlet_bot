import asyncio, os
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

from app.handlers import router
from app.database.models import async_main

async def main():
    await async_main()
    load_dotenv()
    bot = Bot(token=os.getenv('BOT_TOKEN'))
    dp = Dispatcher()
    dp.include_router(router)

    try:
        print('Bot is starting now...')
        await dp.start_polling(bot)
    finally:
        print('Bot has been shut down gracefully')


if __name__ == '__main__':
    asyncio.run(main())
