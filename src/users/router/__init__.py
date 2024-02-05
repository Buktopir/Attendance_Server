from src.users.router.auth import get_auth_router
from src.users.router.common import ErrorCode
from src.users.router.register import get_register_router
from src.users.router.reset import get_reset_password_router
from src.users.router.users import get_users_router
from src.users.router.verify import get_verify_router

__all__ = [
    "ErrorCode",
    "get_auth_router",
    "get_register_router",
    "get_reset_password_router",
    "get_users_router",
    "get_verify_router",
]

try:  # pragma: no cover
    from src.users.router.oauth import get_oauth_router  # noqa: F401

    __all__.append("get_oauth_router")
except ModuleNotFoundError:  # pragma: no cover
    pass
