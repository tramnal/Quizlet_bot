from sqlalchemy import select

from database import async_session, UserWord


async def set_user(tg_id):
    async with async_session() as session:
        user = await session.scalar(select(UserWord).where(UserWord.tg_id == tg_id))

    if not user:
        session.add(UserWord(tg_id=tg_id))
        await session.commit()



