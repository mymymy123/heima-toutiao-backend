from sqlalchemy.ext.asyncio import create_async_engine,AsyncSession,async_sessionmaker

ASYNC_URL='mysql+aiomysql://root:root123@localhost:3306/news_app?charset=utf8mb4'
ASYNC_ENGINE=create_async_engine(
    url=ASYNC_URL,
    echo=True,
    pool_size=10,
    max_overflow=20
)


AsyncSessionLocal=async_sessionmaker(
    bind=ASYNC_ENGINE,
    class_=AsyncSession,
    expire_on_commit=False

)

async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()