"""
Базовый класс клиента API Авито.
"""
import json
from abc import ABC, abstractmethod
from datetime import timedelta
from typing import Any, Optional, Type, TypeVar, Union

from pydantic import BaseModel, Field

from ..config import ClientConfig, DEFAULT_CONFIG, logger
from ..exceptions import (
    AuthError, AvitoApiError
)
from ..utils import extract_rate_limits, handle_response_error, parse_model, get_timestamp, naive_utcnow

T = TypeVar('T', bound=BaseModel)


class AccessTokenResponse(BaseModel):
    """Базовый ответ с информацией о токене."""

    access_token: str = Field(..., description="Ключ для временной авторизации в системе")
    expires_at: int = Field(..., description="Время окончания жизни ключа в секундах, UTC")
    token_type: str = Field(..., description="Тип ключа авторизации")


class BaseApiClient(ABC):
    """
    Абстрактный базовый класс для клиента API Авито.

    Attributes:
        config: Конфигурация клиента
        client_id: Идентификатор клиента
        client_secret: Секрет клиента
        access_token: Токен доступа
        refresh_token: Токен обновления
        token_expires_at: Время истечения токена в формате timestamp
        token_type: Тип токена (Bearer)
    """

    def __init__(
        self,
        client_id: str,
        client_secret: str,
        access_token: Optional[str] = None,
        refresh_token: Optional[str] = None,
        token_expires_at: Optional[int] = None,
        config: Optional[ClientConfig] = None,
    ):
        """
        Инициализирует клиент API Авито.

        Args:
            client_id: Идентификатор клиента
            client_secret: Секрет клиента
            access_token: Опциональный токен доступа (если уже есть)
            refresh_token: Опциональный токен обновления (если уже есть)
            token_expires_at: Опциональное время истечения токена (если уже есть)
            config: Опциональная конфигурация клиента
        """
        self.config = config or DEFAULT_CONFIG
        self.config.setup_logging()

        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.token_expires_at = token_expires_at
        self.token_type = "Bearer"

        logger.debug(
            f"Инициализирован клиент API Авито. "
            f"ID: {client_id}, token: {'установлен' if access_token else 'не установлен'}"
        )

    @abstractmethod
    async def _request_async(
        self,
        method: str,
        url: str,
        params: Optional[dict[str, Any]] = None,
        data: Optional[dict[str, Any]] = None,
        json_data: Optional[dict[str, Any]] = None,
        headers: Optional[dict[str, str]] = None,
        auth_required: bool = True,
        form_encoded: bool = False,
        multipart: bool = False,
        files: Optional[dict[str, Any]] = None,
    ) -> dict[str, Any]:
        """
        Выполняет асинхронный HTTP-запрос к API.

        Args:
            method: HTTP-метод (GET, POST, и т.д.)
            url: URL-адрес эндпоинта
            params: Параметры запроса
            data: Данные запроса
            json_data: JSON-данные запроса
            headers: Заголовки запроса
            auth_required: Требуется ли авторизация
            form_encoded: Использовать ли application/x-www-form-urlencoded
            multipart: Использовать ли multipart/form-data
            files: Файлы для отправки

        Returns:
            Словарь с данными ответа
        """
        pass

    @abstractmethod
    def _request_sync(
        self,
        method: str,
        url: str,
        params: Optional[dict[str, Any]] = None,
        data: Optional[dict[str, Any]] = None,
        json_data: Optional[dict[str, Any]] = None,
        headers: Optional[dict[str, str]] = None,
        auth_required: bool = True,
        form_encoded: bool = False,
        multipart: bool = False,
        files: Optional[dict[str, Any]] = None,
    ) -> dict[str, Any]:
        """
        Выполняет синхронный HTTP-запрос к API.

        Args:
            method: HTTP-метод (GET, POST, и т.д.)
            url: URL-адрес эндпоинта
            params: Параметры запроса
            data: Данные запроса
            json_data: JSON-данные запроса
            headers: Заголовки запроса
            auth_required: Требуется ли авторизация
            form_encoded: Использовать ли application/x-www-form-urlencoded
            multipart: Использовать ли multipart/form-data
            files: Файлы для отправки

        Returns:
            Словарь с данными ответа
        """
        pass

    def _get_auth_header(self) -> dict[str, str]:
        """
        Возвращает заголовок с токеном авторизации.

        Returns:
            Словарь с заголовком Authorization

        Raises:
            AuthError: Если токен не установлен
        """
        if not self.access_token:
            raise AuthError("Токен авторизации не установлен")

        return {"Authorization": f"{self.token_type} {self.access_token}"}

    def _is_token_expired(self) -> bool:
        """
        Проверяет, истек ли токен доступа.

        Returns:
            True, если токен истек или истечет в ближайшее время, иначе False
        """
        if not self.token_expires_at:
            return True

        now = get_timestamp(naive_utcnow())
        threshold = self.config.api.token_refresh_threshold

        # Токен истек или истечет в течение threshold секунд
        return now + threshold >= self.token_expires_at

    def _update_token_info(
        self,
        access_token: str,
        expires_in: int,
        token_type: str = "Bearer",
        refresh_token: Optional[str] = None,
    ) -> None:
        """
        Обновляет информацию о токене авторизации.

        Args:
            access_token: Новый токен доступа
            expires_in: Время жизни токена в секундах
            token_type: Тип токена
            refresh_token: Новый токен обновления (если есть)
        """
        self.access_token = access_token
        self.token_type = token_type
        self.token_expires_at = get_timestamp(naive_utcnow()) - 60 + expires_in

        if refresh_token:
            self.refresh_token = refresh_token

        logger.debug(
            f"Обновлена информация о токене. "
            f"Истекает через {timedelta(seconds=expires_in)}"
        )

    def _build_url(self, endpoint: str) -> str:
        """
        Строит полный URL для запроса.

        Args:
            endpoint: Эндпоинт API

        Returns:
            Полный URL для запроса
        """
        base_url = self.config.api.base_url.rstrip("/")
        endpoint = endpoint.lstrip("/")
        return f"{base_url}/{endpoint}"

    def _handle_response(
        self,
        status_code: int,
        content: Union[str, bytes],
        headers: dict[str, str]
    ) -> dict[str, Any]:
        """
        Обрабатывает ответ от API.

        Args:
            status_code: Код статуса ответа
            content: Тело ответа
            headers: Заголовки ответа

        Returns:
            Словарь с данными ответа

        Raises:
            AvitoApiError: При ошибке обработки ответа
        """
        # Логируем информацию о лимитах запросов
        limit, remaining = extract_rate_limits(headers)
        if limit is not None and remaining is not None:
            logger.debug(f"Лимит запросов: {remaining}/{limit}")

        # Пустой ответ
        if not content:
            if 200 <= status_code < 300:
                return {}
            handle_response_error(status_code)

        # Пробуем распарсить JSON
        try:
            if isinstance(content, bytes):
                content = content.decode('utf-8')

            response_data = json.loads(content)

            # Проверяем наличие ошибки в ответе
            if 200 <= status_code < 300:
                return response_data

            handle_response_error(status_code, response_data)

        except json.JSONDecodeError:
            logger.error(f"Ошибка декодирования JSON: {content}")
            if 200 <= status_code < 300:
                return {"content": content}
            handle_response_error(status_code)

        # Этот код не должен выполниться, но добавлен для типизации
        return {}

    def parse_response_model(self, model_class: Type[T], data: dict[str, Any]) -> T:
        """
        Парсит данные ответа в модель Pydantic.

        Args:
            model_class: Класс модели для парсинга
            data: Данные для парсинга

        Returns:
            Экземпляр модели с данными
        """
        return parse_model(model_class, data)

    @abstractmethod
    def get_token(self) -> dict[str, Any]:
        """
        Получает токен доступа через client_credentials.

        Returns:
            Информация о токене доступа
        """
        pass

    @abstractmethod
    async def get_token_async(self) -> dict[str, Any]:
        """
        Асинхронно получает токен доступа через client_credentials.

        Returns:
            Информация о токене доступа
        """
        pass

    @abstractmethod
    def get_current_token(self) -> AccessTokenResponse:
        """
        Получает текущий токен доступа через client_credentials.

        Returns:
            Информация о токене доступа
        """
        pass

    @abstractmethod
    async def get_current_token_async(self) -> AccessTokenResponse:
        """
        Асинхронно получает текущий токен доступа через client_credentials.

        Returns:
            Информация о токене доступа
        """
        pass

    @abstractmethod
    def refresh_access_token(self) -> dict[str, Any]:
        """
        Обновляет токен доступа с использованием refresh_token.

        Returns:
            Информация о новом токене доступа

        Raises:
            AuthError: Если refresh_token не установлен
        """
        pass

    @abstractmethod
    async def refresh_access_token_async(self) -> dict[str, Any]:
        """
        Асинхронно обновляет токен доступа с использованием refresh_token.

        Returns:
            Информация о новом токене доступа

        Raises:
            AuthError: Если refresh_token не установлен
        """
        pass

    def _ensure_auth(self) -> None:
        """
        Проверяет наличие действительного токена и обновляет его при необходимости.

        Raises:
            AuthError: Если не удалось получить или обновить токен
        """
        if not self.access_token or self._is_token_expired():
            if self.refresh_token and self.config.api.auto_refresh_token:
                logger.debug("Токен истек или отсутствует, обновляем с помощью refresh_token")
                try:
                    self.refresh_access_token()
                    return
                except AvitoApiError as e:
                    logger.warning(f"Не удалось обновить токен: {str(e)}")

            logger.debug("Получаем новый токен доступа")
            self.get_token()

    async def _ensure_auth_async(self) -> None:
        """
        Асинхронно проверяет наличие действительного токена и обновляет его при необходимости.

        Raises:
            AuthError: Если не удалось получить или обновить токен
        """
        if not self.access_token or self._is_token_expired():
            if self.refresh_token and self.config.api.auto_refresh_token:
                logger.debug("Токен истек или отсутствует, обновляем с помощью refresh_token")
                try:
                    await self.refresh_access_token_async()
                    return
                except AvitoApiError as e:
                    logger.warning(f"Не удалось обновить токен: {str(e)}")

            logger.debug("Получаем новый токен доступа")
            await self.get_token_async()
