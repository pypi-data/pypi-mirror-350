"""
Модуль с кастомными исключениями для библиотеки avito_api.
"""
from typing import Any, Optional


class AvitoApiError(Exception):
    """Базовое исключение для всех ошибок API Авито."""

    def __init__(self, message: str = "Ошибка API Авито", status_code: Optional[int] = None,
                 details: Optional[dict[str, Any]] = None):
        self.status_code = status_code
        self.details = details
        message_with_details = f"{message}"
        if status_code:
            message_with_details += f" (код: {status_code})"
        if details:
            message_with_details += f", детали: {details}"
        super().__init__(message_with_details)


class AuthError(AvitoApiError):
    """Ошибка авторизации."""

    def __init__(self, message: str = "Ошибка авторизации", **kwargs):
        super().__init__(message, **kwargs)


class TokenExpiredError(AuthError):
    """Срок действия токена истек."""

    def __init__(self, message: str = "Срок действия токена истек", **kwargs):
        super().__init__(message, **kwargs)


class ForbiddenError(AvitoApiError):
    """Доступ запрещен (403)."""

    def __init__(self, message: str = "Доступ запрещен", **kwargs):
        super().__init__(message, **kwargs)


class NotFoundError(AvitoApiError):
    """Ресурс не найден (404)."""

    def __init__(self, message: str = "Ресурс не найден", **kwargs):
        super().__init__(message, **kwargs)


class ValidationError(AvitoApiError):
    """Ошибка валидации данных."""

    def __init__(self, message: str = "Ошибка валидации данных", errors: Optional[list[dict[str, Any]]] = None, **kwargs):
        self.errors = errors
        details = f", ошибки: {errors}" if errors else ""
        super().__init__(f"{message}{details}", **kwargs)


class RateLimitError(AvitoApiError):
    """Превышен лимит запросов к API."""

    def __init__(self, message: str = "Превышен лимит запросов к API", **kwargs):
        super().__init__(message, **kwargs)


class ServerError(AvitoApiError):
    """Внутренняя ошибка сервера (5xx)."""

    def __init__(self, message: str = "Внутренняя ошибка сервера", **kwargs):
        super().__init__(message, **kwargs)


class NetworkError(AvitoApiError):
    """Ошибка сети при выполнении запроса."""

    def __init__(self, message: str = "Ошибка сети при выполнении запроса",
                 original_exception: Optional[Exception] = None, **kwargs):
        self.original_exception = original_exception
        message_with_original = f"{message}"
        if original_exception:
            message_with_original += f": {str(original_exception)}"
        super().__init__(message_with_original, **kwargs)


class ConfigError(AvitoApiError):
    """Ошибка конфигурации клиента."""

    def __init__(self, message: str = "Ошибка конфигурации клиента", **kwargs):
        super().__init__(message, **kwargs)
