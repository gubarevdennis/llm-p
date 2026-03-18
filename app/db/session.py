# app/db/session.py
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from app.core.config import settings

# Формируем строку подключения к SQLite
SQLALCHEMY_DATABASE_URL = f"sqlite+aiosqlite:///{settings.SQLITE_PATH}"

# Создаем асинхронный движок
engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},  # Требуется для SQLite
    echo=False # Установите True для отладки SQL-запросов в консоли
)

# Фабрика сессий
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False
)