# app/core/config.py

from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Название приложения
    APP_NAME: str = "llm-p"
    
    # Окружение
    ENVIRONMENT: str = "development"

    # Настройки JWT
    JWT_SECRET: str
    JWT_ALG: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # Настройки базы данных
    SQLITE_PATH: str = "./app.db"

    # Настройки OpenRouter
    OPENROUTER_API_KEY: str
    OPENROUTER_BASE_URL: str = "https://openrouter.ai/api/v1"
    OPENROUTER_MODEL: str = "google/gemini-2.0-flash-lite-preview:free"
    OPENROUTER_SITE_URL: str = "https://your-site-url.com"
    OPENROUTER_APP_NAME: str = "llm-p-app"

    # Конфигурация чтения из .env
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"  # Игнорировать лишние поля в .env
    )

# Создаем единственный экземпляр настроек
settings = Settings()