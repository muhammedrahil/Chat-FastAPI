from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from typing import AsyncGenerator

DATABASE_URL = "postgresql+asyncpg://postgres:Zaigo%4025@localhost:5432/customfield_db"

# pool_size = (CPU cores * 2) + effective_concurrent_users // 5


# Application Type	Concurrent Users	Recommended pool_size
# Small App	            10-50	            5-10
# Medium App	        50-200	            10-30
# Large App	            200-1000	        30-80
# Enterprise App	    1000+	            80-150


engine = create_async_engine(DATABASE_URL,
                            pool_size=10,       # 10 connections in the pool
                            max_overflow=5,     # 5 extra connections allowed if needed
                            pool_timeout=30,    # Wait 30 seconds before failing if pool is full
                            pool_recycle=1800,  # Refresh stale connections every 30 minutes
                            echo=True)

async_session_maker = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Dependency to get the database session
async def get_db() -> AsyncGenerator[AsyncSession, None]:  # ✅ Correct return type
    async with async_session_maker() as session:
        yield session  