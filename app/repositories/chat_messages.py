# app/repositories/chat_messages.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import desc

from app.db.models import ChatMessage

class ChatRepository:
    def __init__(self, db: AsyncSession):
        self._db = db

    async def add_message(self, user_id: int, role: str, content: str) -> ChatMessage:
        new_message = ChatMessage(
            user_id=user_id,
            role=role,
            content=content
        )
        self._db.add(new_message)
        await self._db.commit()
        await self._db.refresh(new_message)
        return new_message

    async def get_history(self, user_id: int, max_count: int) -> list[ChatMessage]:
        # Получаем последние max_count сообщений, отсортированные по времени создания
        stmt = (
            select(ChatMessage)
            .where(ChatMessage.user_id == user_id)
            .order_by(desc(ChatMessage.created_at))
            .limit(max_count)
        )
        
        result = await self._db.execute(stmt)
        # Возвращаем список, который нужно будет отсортировать
        history = result.scalars().all()
        
        # Возвращаем в хронологическом порядке - самые старые первыми
        return sorted(history, key=lambda m: m.created_at)

    async def clear_history(self, user_id: int) -> None:
        # Удаление всех сообщений пользователя
        await self._db.execute(
            ChatMessage.__table__.delete().where(ChatMessage.user_id == user_id)
        )
        await self._db.commit()