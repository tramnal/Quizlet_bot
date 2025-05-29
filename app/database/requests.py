from app.database import async_session
from sqlalchemy import select


async def set_user(tg_id):
    async with async_session() as session:
        user = await session.scalar(select(user).where(user.tg_id == tg_id))

    if not user:
        session.add(user(tg_id=tg_id))
        await session.commit()
        