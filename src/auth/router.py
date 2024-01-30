import uuid

from fastapi_users import FastAPIUsers

from src.auth.config import auth_backend
from src.auth.manager import get_user_manager
from src.auth.models import User

fastapi_users = FastAPIUsers[User, uuid.UUID](get_user_manager, [auth_backend])

