# app/db/models.py
import datetime
from sqlalchemy import ForeignKey, String, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String, nullable=False)
    role: Mapped[str] = mapped_column(String, default="user")
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.now())

    # Связь с сообщениями
    messages: Mapped[list["ChatMessage"]] = relationship(
        "ChatMessage", 
        back_populates="user",
        cascade="all, delete-orphan"
    )

class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    role: Mapped[str] = mapped_column(String, nullable=False) # 'user' или 'assistant'
    content: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.now())

    # Связь с пользователем
    user: Mapped["User"] = relationship("User", back_populates="messages")