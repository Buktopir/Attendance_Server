import httpx
from fastapi import FastAPI, Depends, HTTPException
from starlette.requests import Request
from src.auth.config import auth_backend
from src.auth.manager import google_oauth_client
from src.auth.models import User
from src.auth.router import fastapi_users
from src.auth.schemas import UserRead, UserCreate, UserUpdate
from src.config import SECRET

app = FastAPI()
app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/atdn",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"]
)

app.include_router(
    fastapi_users.get_oauth_router(google_oauth_client, auth_backend, SECRET),
    prefix="/auth/google",
    tags=["auth"],
)


current_user = fastapi_users.current_user()

@app.get("/protected-route")
def protected_route(user: User = Depends(current_user)):
    return f"Hello, {user.email}"


@app.post("/get-user-info/")
async def get_user_info(request: Request):
    # Получаем Access Token из тела запроса или заголовков
    body = await request.json()
    token = body.get('token')  # Исправлено на использование .get()

    if not token:
        raise HTTPException(status_code=400, detail="Google Access Token is required")

    # Запрашиваем информацию о пользователе из Google API асинхронно
    google_info_url = "https://www.googleapis.com/oauth2/v2/userinfo"
    headers = {"Authorization": f"Bearer {token}"}
    async with httpx.AsyncClient() as client:
        response = await client.get(google_info_url, headers=headers)

    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Failed to get user information from Google")

    user_info = response.json()
    print(user_info)

    return {"user_info": user_info}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)