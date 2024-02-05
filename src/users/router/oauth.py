from typing import Dict, List, Optional, Tuple, Type

import jwt
from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from httpx_oauth.integrations.fastapi import OAuth2AuthorizeCallback
from httpx_oauth.oauth2 import BaseOAuth2, OAuth2Token
from pydantic import BaseModel

from src.users import models, schemas
from src.users.authentication import AuthenticationBackend, Authenticator, Strategy
from src.users.exceptions import UserAlreadyExists
from src.users.jwt import SecretType, decode_jwt, generate_jwt
from src.users.manager import BaseUserManager, UserManagerDependency
from src.users.router.common import ErrorCode, ErrorModel

STATE_TOKEN_AUDIENCE = "fastapi-users:oauth-state"


class GoogleTokenData(BaseModel):
    access_token: str


class OAuth2AuthorizeResponse(BaseModel):
    authorization_url: str


def generate_state_token(
        data: Dict[str, str], secret: SecretType, lifetime_seconds: int = 3600
) -> str:
    data["aud"] = STATE_TOKEN_AUDIENCE
    return generate_jwt(data, secret, lifetime_seconds)


def get_oauth_router(
        oauth_client: BaseOAuth2,
        backend: AuthenticationBackend,
        get_user_manager: UserManagerDependency[models.UP, models.ID],
        state_secret: SecretType,
        associate_by_email: bool = False,
        is_verified_by_default: bool = False,
) -> APIRouter:
    router = APIRouter()

    @router.post("/authorize", response_model=GoogleTokenData)  # Define SomeResponseModel according to your needs
    async def authorize(
            access_token_data: GoogleTokenData,
            request: Request,
            user_manager: BaseUserManager[models.UP, models.ID] = Depends(get_user_manager),
            strategy: Strategy[models.UP, models.ID] = Depends(backend.get_strategy),
    ):
        access_token = access_token_data.access_token
        account_id, account_email = await oauth_client.get_id_email(access_token)

        if account_email is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email not available from OAuth provider.",
            )

        try:
            user = await user_manager.oauth_callback(
                oauth_client.name,
                access_token,
                account_id,
                account_email,
                None,  # Expires at
                None,  # Refresh token, if available
                request,
                associate_by_email=associate_by_email,
                is_verified_by_default=is_verified_by_default,
            )
        except UserAlreadyExists:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User already exists.",
            )

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User is inactive.",
            )

        # Authenticate
        response = await backend.login(strategy, user)
        await user_manager.on_after_login(user, request, response)
        return response

    return router
