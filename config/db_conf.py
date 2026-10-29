from sqlalchemy.ext.asyncio import async_sessionmaker,AsyncSession,create_async_engine
from sqlalchemy.orm import sessionmaker

ASYNC_DATABASE_URL = "mysql+aiomysql://root:@localhost:3306/db?charset=utf8"
async_engine = create_async_engine(ASYNC_DATABASE_URL,  echo=True,pool_size=10,max_overflow=20)
AsyncSession = sessionmaker(bind=async_engine,expire_on_commit=False,class_=AsyncSession)
async def get_db():
    async with AsyncSession as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()









