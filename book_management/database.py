from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from book_management.config import Config

DATABASE_URL = Config.SQLALCHEMY_DATABASE_URI

# Create an asynchronous engine
engine = create_async_engine(DATABASE_URL, echo=True)

# Create a configured "Session" class
AsyncSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)

# Dependency
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
