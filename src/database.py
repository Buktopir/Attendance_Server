from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from src.config import POSTGRES_URI

engine = create_async_engine(POSTGRES_URI)
async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)