from app.database.models import Base
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession


engine = create_async_engine(url='sqlite+aiosqlite:///db.sqlite3')
async_session = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


async def create_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)