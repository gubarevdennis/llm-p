from datetime import datetime, timedelta, timezone
from typing import Any

# Библиотеки для криптографии
from jose import JWTError, jwt
from passlib.context import CryptContext

# Импортируем настройки из центрального конфигурационного файла
from app.core.config import settings

# Настройки Хеширования паролей
# Используем стандартный bcrypt, но можно настроить на PBKDF2, если нужно
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Проверяет, соответствует ли простой пароль хешированному."""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Хеширует пароль."""
    return pwd_context.hash(password)

# Настройки JWT (JSON Web Tokens)

def create_access_token(data: dict[str, Any], expires_delta: timedelta | None = None) -> str:
    """
    Генерирует JWT Access Token.
    
    data: Словарь, который будет включен в payload (например, user_id, role).
    expires_delta: Опциональное время жизни токена.
    """
    to_encode = data.copy()
    
    # Установка времени истечения
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        
    to_encode.update({"exp": expire})
    to_encode.update({"iat": datetime.now(timezone.utc)})
    
    # Кодирование токена
    encoded_jwt = jwt.encode(
        to_encode, 
        settings.JWT_SECRET, 
        algorithm=settings.JWT_ALG
    )
    return encoded_jwt

def decode_access_token(token: str) -> dict[str, Any]:
    """
    Декодирует JWT токен, валидирует подпись и срок действия.
    Возвращает декодированный payload.
    """
    credentials_exception = {
        "code": "unauthorized",
        "message": "Could not validate credentials"
    }
    
    try:
        # Декодирование токена
        payload = jwt.decode(
            token, 
            settings.JWT_SECRET, 
            algorithms=[settings.JWT_ALG]
        )
        
        # Проверка данных, которые должны быть в токене
        sub: str = payload.get("sub")
        role: str = payload.get("role")
        
        if sub is None or role is None:
            raise credentials_exception
            
        return payload
        
    except JWTError:
        # Если токен просрочен, неверная подпись и т.д.
        raise credentials_exception