"""
Вспомогательные функции для библиотеки avito_api.
"""
import time
from datetime import datetime, timezone
from typing import Any, Optional, Tuple, Type, TypeVar, Callable

import pydantic
from pydantic import BaseModel

from .exceptions import (
    AuthError, ForbiddenError, NetworkError, NotFoundError,
    RateLimitError, ServerError, ValidationError
)
from .config import logger

T = TypeVar('T', bound=BaseModel)

# возвращает UTC timestamp в секундах
get_timestamp = lambda dt: int(dt.replace(tzinfo=timezone.utc).timestamp()) if isinstance(dt, datetime) else None


def naive_utcnow() -> datetime:
    """
    Возвращает текущее время в UTC
    """
    return datetime.now(tz=timezone.utc).replace(tzinfo=None)


def parse_model(model_class: Type[T], data: dict[str, Any]) -> T:
    """
    Парсит данные в Pydantic-модель и логирует возможные ошибки.

    Args:
        model_class: Класс Pydantic-модели для парсинга
        data: Словарь с данными для парсинга

    Returns:
        Экземпляр Pydantic-модели

    Raises:
        ValidationError: Если данные не соответствуют схеме модели
    """
    try:
        return model_class.parse_obj(data)
    except pydantic.ValidationError as e:
        error_msg = f"Ошибка валидации данных для модели {model_class.__name__}: {str(e)}"
        logger.error(error_msg)
        validation_errors = e.errors()
        raise ValidationError(error_msg, errors=validation_errors)


def handle_response_error(
    status_code: int,
    response_data: Optional[dict[str, Any]] = None
) -> None:
    """
    Обрабатывает ошибки ответа API и вызывает соответствующие исключения.

    Args:
        status_code: HTTP-код ответа
        response_data: Данные ответа, если есть

    Raises:
        AuthError: При ошибке авторизации (401)
        ForbiddenError: При ошибке доступа (403)
        NotFoundError: При ошибке не найден (404)
        RateLimitError: При превышении лимитов запросов (429)
        ServerError: При ошибке сервера (5xx)
        ValidationError: При ошибке валидации (400) с деталями ошибок полей
    """
    error_message = "Неизвестная ошибка"
    error_details = None

    if response_data and isinstance(response_data, dict):
        error_data = response_data.get('error', {})
        if isinstance(error_data, dict):
            error_message = error_data.get('message', error_message)
            error_details = error_data.get('fields')

    if status_code == 400:
        raise ValidationError(
            message=f"Ошибка валидации: {error_message}",
            errors=error_details
        )
    elif status_code == 401:
        raise AuthError(
            message=f"Ошибка авторизации: {error_message}",
            status_code=status_code,
            details=error_details
        )
    elif status_code == 403:
        raise ForbiddenError(
            message=f"Доступ запрещен: {error_message}",
            status_code=status_code
        )
    elif status_code == 404:
        raise NotFoundError(
            message=f"Ресурс не найден: {error_message}",
            status_code=status_code
        )
    elif status_code == 429:
        raise RateLimitError(
            message=f"Превышен лимит запросов: {error_message}",
            status_code=status_code
        )
    elif 500 <= status_code < 600:
        raise ServerError(
            message=f"Ошибка сервера: {error_message}",
            status_code=status_code
        )
    else:
        raise NetworkError(
            message=f"Непредвиденная ошибка HTTP {status_code}: {error_message}"
        )


def retry_with_backoff(max_retries: int = 3, base_delay: float = 1.0) -> Callable:
    """
    Декоратор для повторной попытки выполнения функции с экспоненциальной задержкой.

    Args:
        max_retries: Максимальное количество повторных попыток
        base_delay: Базовая задержка между попытками в секундах

    Returns:
        Декорированная функция
    """

    def decorator(func: Callable) -> Callable:
        def wrapper(*args, **kwargs):
            retries = 0
            last_exception = None

            while retries <= max_retries:
                try:
                    return func(*args, **kwargs)
                except (NetworkError, ServerError, RateLimitError) as e:
                    last_exception = e
                    retries += 1

                    if retries > max_retries:
                        break

                    # Экспоненциальная задержка с небольшим случайным временем
                    delay = base_delay * (2 ** (retries - 1))
                    logger.warning(
                        f"Повторная попытка {retries}/{max_retries} после ошибки: {str(e)}. "
                        f"Следующая попытка через {delay:.2f} секунд"
                    )
                    time.sleep(delay)
                except Exception as e:
                    # Для других исключений не применяем повторные попытки
                    raise e

            # Если все попытки не удались, вызываем последнее исключение
            if last_exception:
                raise last_exception

        return wrapper

    return decorator


def format_form_data(data: dict[str, Any]) -> dict[str, str]:
    """
    Форматирует данные для отправки в форме application/x-www-form-urlencoded.

    Args:
        data: Словарь с данными

    Returns:
        Словарь с данными в строковом формате
    """
    formatted_data = {}

    for key, value in data.items():
        if value is None:
            continue

        if isinstance(value, bool):
            formatted_data[key] = str(value).lower()
        elif isinstance(value, (list, tuple)):
            formatted_data[key] = ','.join(str(item) for item in value)
        else:
            formatted_data[key] = str(value)

    return formatted_data


def is_token_expired(expires_at: int, threshold: int = 300) -> bool:
    """
    Проверяет, истек ли токен или истечет в ближайшее время.

    Args:
        expires_at: Время истечения токена в формате timestamp
        threshold: Порог в секундах для обновления токена до истечения

    Returns:
        True, если токен истек или истечет в ближайшее время, иначе False
    """
    now = get_timestamp(naive_utcnow())
    return now + threshold >= expires_at


def extract_rate_limits(headers: dict[str, str]) -> Tuple[Optional[int], Optional[int]]:
    """
    Извлекает информацию о лимитах запросов из заголовков ответа.

    Args:
        headers: Заголовки ответа

    Returns:
        Кортеж (лимит, оставшееся количество запросов)
    """
    limit = headers.get('X-RateLimit-Limit')
    remaining = headers.get('X-RateLimit-Remaining')

    return (
        int(limit) if limit and limit.isdigit() else None,
        int(remaining) if remaining and remaining.isdigit() else None
    )
