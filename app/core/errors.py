from typing import Any

# Базовый класс для всех ошибок приложения
class AppBaseError(Exception):
    """Базовый класс для всех пользовательских исключений в приложении."""
    
    # Код ошибки, который может быть полезен для логирования или фронтенда
    status_code: int = 500
    
    def __init__(self, detail: Any, status_code: int = None):
        self.detail = detail
        if status_code is not None:
            self.status_code = status_code
        super().__init__(self.detail)

# Типовые исключения для бизнес-логики
class ConflictError(AppBaseError):
    """HTTP 409 Conflict: Ресурс уже существует (например, email)."""
    def __init__(self, detail: str = "Conflict"):
        super().__init__(detail=detail, status_code=409)

class UnauthorizedError(AppBaseError):
    """HTTP 401 Unauthorized: Неверные учетные данные."""
    def __init__(self, detail: str = "Неверное имя пользователя или пароль"):
        super().__init__(detail=detail, status_code=401)

class ForbiddenError(AppBaseError):
    """HTTP 403 Forbidden: У пользователя нет прав доступа к ресурсу."""
    def __init__(self, detail: str = "Доступ запрещен"):
        super().__init__(detail=detail, status_code=403)

class NotFoundError(AppBaseError):
    """HTTP 404 Not Found: Ресурс не найден."""
    def __init__(self, detail: str = "Ресурс не найден"):
        super().__init__(detail=detail, status_code=404)

# Исключения для внешних сервисов
class ExternalServiceError(AppBaseError):
    """Ошибка при взаимодействии со сторонними сервисами"""
    def __init__(self, detail: str = "Ошибка внешнего сервиса"):
        # Обычно возвращаем 502 Bad Gateway или 500
        super().__init__(detail=detail, status_code=502)