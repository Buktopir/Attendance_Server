from fastapi import Depends
from src.users.db import SQLAlchemyUserDatabase
from src.users.db.acces_token import SQLAlchemyAccessTokenDatabase
from src.users.authentication.strategy.db import AccessTokenDatabase, DatabaseStrategy
from sqlalchemy.ext.asyncio import AsyncSession
from src.auth.models import User, AccessToken, OAuthAccount
from src.dependencies import get_async_session


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User, OAuthAccount)


async def get_access_token_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyAccessTokenDatabase(session, AccessToken)




def get_database_strategy(
    access_token_db: AccessTokenDatabase[AccessToken] = Depends(get_access_token_db),
) -> DatabaseStrategy:
    return DatabaseStrategy(access_token_db, lifetime_seconds=10)
