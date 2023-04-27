__all__ = [
    'async_session_maker'
]


from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.engine import URL
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession
from sqlalchemy.orm import sessionmaker
from config import DATABASE, HOST, USERNAME, PASSWORD, PORT


postgres_url = URL.create(
        drivername='postgresql+asyncpg',
        username=USERNAME,
        password=PASSWORD,
        host=HOST,
        port=PORT,
        database=DATABASE
    )


engine: AsyncEngine = create_async_engine(url=postgres_url, echo=True)
async_session_maker: AsyncSession = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
