# app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

# Импорты инфраструктурных компонентов
from app.db.session import engine
from app.db.base import Base
from app.core.config import settings

# Импорты роутеров (которые мы создали как заглушки выше)
from app.api.routes_auth import router as auth_router
from app.api.routes_chat import router as chat_router

# Контекстный менеджер для запуска/завершения (Startup/Shutdown)
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Событие Startup
    print("🚀 Приложение запускается. Инициализация БД...")
    
    # Создание таблиц БД
    async with engine.begin() as conn:
        # В продакшене это лучше делать через Alembic, но по требованию используем create_all
        await conn.run_sync(Base.metadata.create_all)
    
    print("✅ Структура базы данных готова.")
    
    yield
    
    # Событие Shutdown (для чистого закрытия соединений, если нужно)
    await engine.dispose()
    print("🛑 Приложение завершает работу.")

# Функция создания приложения
def create_app() -> FastAPI:
    
    # 1. Настройка CORS
    # В реальном проекте здесь бы использовались настройки из settings
    origins = [
        "http://localhost",
        "http://localhost:8080",
        "http://127.0.0.1:8080",
    ]
    
    app = FastAPI(
        title=settings.APP_NAME,
        version="1.0.0",
        lifespan=lifespan # Внедряем менеджер жизненного цикла
    )

    # Добавление CORS Middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # 2. Подключение роутеров
    app.include_router(auth_router)
    app.include_router(chat_router)

    # 3. Технический endpoint
    @app.get("/health", tags=["Health Check"])
    def health_check():
        """Проверка работоспособности приложения и окружения."""
        return {
            "status": "ok",
            "environment": "development" if settings.SQLITE_PATH == "./app.db" else "production",
            "app_name": settings.APP_NAME
        }
        
    return app

# Создание экземпляра приложения
app = create_app()