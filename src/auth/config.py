from fastapi_users.authentication import BearerTransport, AuthenticationBackend

from src.auth.database import get_database_strategy

bearer_transport = BearerTransport(tokenUrl="auth/atdn/login")

auth_backend = AuthenticationBackend(
    name="atdn",
    transport=bearer_transport,
    get_strategy=get_database_strategy
)