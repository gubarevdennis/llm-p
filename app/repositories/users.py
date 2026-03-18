# app/repositories/users.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError

from app.db.models import User
from app.core.errors import ConflictError, NotFoundError
from app.schemas.user import UserPublic

class UserRepository:
    def __init__(self, db: AsyncSession):
        self._db = db

    async def get_by_email(self, email: str) -> User | None:
        result = await self._db.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    async def get_by_id(self, user_id: int) -> User | None:
        result = await self._db.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()

    async def create(self, email: str, password_hash: str, role: str = "user") -> User:
        new_user = User(
            email=email,
            password_hash=password_hash,
            role=role
        )
        self._db.add(new_user)
        try:
            await self._db.commit()
            await self._db.refresh(new_user)
            return new_user
        except IntegrityError:
            # В случае, если email все же оказался занят после первой проверки
            await self._db.rollback()
            raise ConflictError(detail=f"Пользователь с email {email} уже существует.")

    async def get_public_profile(self, user_id: int) -> UserPublic:
        user = await self.get_by_id(user_id)
        if not user:
            raise NotFoundError(detail=f"Пользователь с ID {user_id} не найден.")
        
        # Возвращаем публичную схему, from_attributes=True позволяет это сделать
        return UserPublic.model_validate(user)