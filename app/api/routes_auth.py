from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db, get_current_user_id, handle_errors
from app.repositories.users import UserRepository
from app.usecases.auth import AuthUseCase
from app.schemas.auth import RegisterRequest, TokenResponse
from app.schemas.user import UserPublic

router = APIRouter(prefix="/auth", tags=["Auth"])

def get_auth_usecase(db: AsyncSession = Depends(get_db)):
    return AuthUseCase(UserRepository(db))

@router.post("/register", response_model=UserPublic)
async def register(data: RegisterRequest, uc: AuthUseCase = Depends(get_auth_usecase)):
    return await handle_errors(uc.register(data))

@router.post("/login", response_model=TokenResponse)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), uc: AuthUseCase = Depends(get_auth_usecase)):
    return await handle_errors(uc.login(form_data.username, form_data.password))

@router.get("/me", response_model=UserPublic)
async def get_me(user_id: int = Depends(get_current_user_id), uc: AuthUseCase = Depends(get_auth_usecase)):
    return await handle_errors(uc.get_user_profile(user_id))