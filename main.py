import asyncio
from aiogram import Bot, Dispatcher

from app.handlers import router
from app.database.models import Base, engine
from app.config import config

async def init_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def main():
    await init_database()
    
    bot = Bot(token=config.BOT_TOKEN)
    dp = Dispatcher()
    dp.include_router(router)

    try:
        print('Bot is starting now...')
        await dp.start_polling(bot)
    finally:
        print('Bot has been shut down gracefully')


if __name__ == '__main__':
    asyncio.run(main())
