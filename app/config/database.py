import logging
import os
from typing import AsyncGenerator

from dotenv import load_dotenv
from fastapi import HTTPException
from sqlalchemy import text
from sqlalchemy.exc import OperationalError, SQLAlchemyError
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL_PROD")

# SQLAlchemy Base for model declarations
Base = declarative_base()

# Create the async engine
engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    future=True,
    pool_size=20,  # Larger base pool
    max_overflow=20,  # Allows up to 40 total
    pool_timeout=60,  # Wait up to 60s for a connection
)

# Create a session factory
async_session = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


# Dependency for getting DB session
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        # Ping the DB to ensure the connection is alive
        await session.execute(text("SELECT 1"))
        logging.info("Database connection established successfully")
        yield session
