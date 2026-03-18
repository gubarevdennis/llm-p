# app/usecases/auth.py
from datetime import timedelta
from app.repositories.users import UserRepository
from app.schemas.auth import RegisterRequest, TokenResponse
from app.schemas.user import UserPublic
from app.core.security import verify_password, get_password_hash, create_access_token
from app.core.errors import ConflictError, UnauthorizedError

class AuthUseCase:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def register(self, data: RegisterRequest) -> UserPublic:
        # 1. Проверка существования
        existing_user = await self.user_repo.get_by_email(data.email)
        if existing_user:
            raise ConflictError(detail=f"Email {data.email} уже зарегистрирован.")

        # 2. Хеширование и создание
        hashed_password = get_password_hash(data.password)
        new_user = await self.user_repo.create(
            email=data.email,
            password_hash=hashed_password
        )
        
        # 3. Возврат публичного профиля
        return await self.user_repo.get_public_profile(new_user.id)

    async def login(self, email: str, password: str) -> TokenResponse:
        # 1. Поиск пользователя
        user = await self.user_repo.get_by_email(email)
        if not user:
            raise UnauthorizedError()

        # 2. Проверка пароля
        if not verify_password(password, user.password_hash):
            raise UnauthorizedError()

        # 3. Создание токена
        access_token = create_access_token(
            data={"sub": str(user.id), "role": user.role},
            expires_delta=timedelta(minutes=30) # Можно использовать другое время
        )
        
        return TokenResponse(access_token=access_token)

    async def get_user_profile(self, user_id: int) -> UserPublic:
        # Репозиторий уже выбрасывает NotFoundError
        return await self.user_repo.get_public_profile(user_id)