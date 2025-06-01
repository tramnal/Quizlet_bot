import asyncio
from aiohttp import web
from aiogram import Bot, Dispatcher

from app import config, router
from app.database import Base, engine


async def init_database() -> None:
    '''Create database table asynchronously'''
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def healthcheck(_: web.Request) -> web.Response:
    '''Simple HTTP health check endpoint'''
    return web.Response(text='OK')

async def bot_start() -> None:
    '''Initialize and start bot using polling'''
    bot = Bot(token=config.BOT_TOKEN)
    dp = Dispatcher()
    dp.include_router(router)

    try:
        print('Bot is starting now...')
        await dp.start_polling(bot)
    finally:
        print('Bot has been shut down gracefully')

async def main() -> None:
    '''The main entry point'''
    await init_database()

    app = web.Application()
    app.router.add_get('/health', healthcheck)
    
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, host='0.0.0.0', port=8080)
    await site.start()

    await bot_start()


if __name__ == '__main__':
    asyncio.run(main())
