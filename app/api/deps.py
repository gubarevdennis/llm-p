from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from typing import Generator

from app.db.session import AsyncSessionLocal
from app.core.security import decode_access_token
from app.core.errors import AppBaseError

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

async def get_db() -> Generator:
    async with AsyncSessionLocal() as session:
        yield session

async def get_current_user_id(token: str = Depends(oauth2_scheme)) -> int:
    try:
        payload = decode_access_token(token)
        return int(payload["sub"])
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )

# Функция-обертка для обработки ошибок доменного слоя
async def handle_errors(coro):
    try:
        return await coro
    except AppBaseError as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)