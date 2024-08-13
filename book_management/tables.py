from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import sessionmaker
from book_management.models import Base

# Import your async engine and session setup
from book_management.database import engine, AsyncSessionLocal, get_db

async def create_tables():
    async with engine.begin() as conn:
        # Use the metadata of your base to create all tables
        await conn.run_sync(Base.metadata.create_all)

# Call this function during application initialization or as a separate setup script
