from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from fastapi_users_db_sqlalchemy.access_token import SQLAlchemyBaseAccessTokenTable
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON, Boolean
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.orm import Mapped, declared_attr, mapped_column
from datetime import datetime

Base = declarative_base()


class User(SQLAlchemyBaseUserTable, Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)

class AccessToken(SQLAlchemyBaseAccessTokenTable, Base):
    __tablename__ = 'access_token'
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
