from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from todo_async import settings

engine: AsyncEngine = create_async_engine(
    settings.database_url,
    echo=False,  # cuidado com logs em produção
    pool_size=10,  # conexões fixas no pool
    max_overflow=20,  # conexões extras em picos
    pool_timeout=30,  # tempo máximo para esperar uma conexão
    pool_recycle=1800,  # recicla conexões antigas (30 min)
    future=True,
)

AsyncSessionLocal = async_sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

async def get_session() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
