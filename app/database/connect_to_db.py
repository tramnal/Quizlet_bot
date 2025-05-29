from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncAttrs, AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

from app import config

DATABASE_URL = config.DB_URL

engine = create_async_engine(DATABASE_URL)

async_session = async_sessionmaker(engine, expire_on_commit=False)


class Base(AsyncAttrs, DeclarativeBase):
    pass

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    '''Generate working session with database'''
    async with async_session() as session:
        yield session
