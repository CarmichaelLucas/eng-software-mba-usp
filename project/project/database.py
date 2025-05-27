from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from project import settings

engine = create_async_engine(settings.database_url)


async def get_session():
    async with AsyncSession(engine, expire_on_commit=False) as session:
        yield session
