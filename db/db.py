from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from config import DB_USER, DB_HOST, DB_PASSWORD, DB_NAME

from db.models import Base

DATABASE_URL = f'postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'

engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


async def recreate_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
