"""
Асинхронная реализация клиента API Авито на базе httpx.
"""
from typing import Any, Optional

import httpx
from httpx import HTTPError

from .base import BaseApiClient, AccessTokenResponse
from ..config import logger
from ..exceptions import AuthError, NetworkError
from ..utils import format_form_data


class AsyncApiClient(BaseApiClient):
    """
    Асинхронная реализация клиента API Авито на базе библиотеки httpx.
    """

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

        Raises:
            NetworkError: При ошибке соединения
            AuthError: При ошибке авторизации
        """
        if auth_required and not url.endswith("/token"):
            await self._ensure_auth_async()

        full_url = self._build_url(url)
        request_headers = {"User-Agent": self.config.api.user_agent}

        if headers:
            request_headers.update(headers)

        if auth_required and self.access_token:
            request_headers.update(self._get_auth_header())

        if form_encoded and data:
            request_headers["Content-Type"] = "application/x-www-form-urlencoded"
            processed_data = format_form_data(data)
        else:
            processed_data = data

        logger.debug(
            f"Выполнение асинхронного {method} запроса к {full_url}"
            f"{' с авторизацией' if auth_required else ''}"
        )

        try:
            async with httpx.AsyncClient(timeout=self.config.api.timeout) as client:
                response = await client.request(
                    method=method,
                    url=full_url,
                    params=params,
                    data=processed_data,
                    json=json_data,
                    headers=request_headers,
                    files=files,
                )

                # Проверяем, не истек ли токен
                if response.status_code == 401 and auth_required and self.config.api.auto_refresh_token:
                    logger.debug("Получен 401, пробуем обновить токен и повторить запрос")

                    if self.refresh_token:
                        await self.refresh_access_token_async()
                    else:
                        await self.get_token_async()

                    # Обновляем заголовок авторизации
                    request_headers.update(self._get_auth_header())

                    # Повторяем запрос с новым токеном
                    response = await client.request(
                        method=method,
                        url=full_url,
                        params=params,
                        data=processed_data,
                        json=json_data,
                        headers=request_headers,
                        files=files,
                    )

                return self._handle_response(
                    status_code=response.status_code,
                    content=response.content,
                    headers=dict(response.headers)
                )

        except HTTPError as e:
            logger.error(f"Ошибка асинхронного запроса: {str(e)}")
            raise NetworkError(f"Ошибка при выполнении асинхронного запроса: {str(e)}", original_exception=e)

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
        Заглушка для синхронного метода в асинхронном клиенте.

        Raises:
            NotImplementedError: Всегда
        """
        raise NotImplementedError(
            "Синхронные методы не реализованы в асинхронном клиенте. "
            "Используйте SyncApiClient для синхронных запросов."
        )

    def get_token(self) -> dict[str, Any]:
        """
        Заглушка для синхронного метода в асинхронном клиенте.

        Raises:
            NotImplementedError: Всегда
        """
        raise NotImplementedError(
            "Синхронные методы не реализованы в асинхронном клиенте. "
            "Используйте SyncApiClient для синхронных запросов."
        )

    async def get_token_async(self) -> dict[str, Any]:
        """
        Асинхронно получает токен доступа через client_credentials.

        Returns:
            Информация о токене доступа

        Raises:
            AuthError: Если не удалось получить токен
        """
        logger.debug("Асинхронный запрос токена доступа через client_credentials")

        data = {
            "grant_type": "client_credentials",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
        }

        try:
            response = await self._request_async(
                method="POST",
                url="/token",
                data=data,
                auth_required=False,
                form_encoded=True,
            )

            access_token = response.get("access_token")
            expires_in = response.get("expires_in", 86400)
            token_type = response.get("token_type", "Bearer")

            if not access_token:
                raise AuthError("Не удалось получить токен доступа: отсутствует access_token в ответе")

            self._update_token_info(
                access_token=access_token,
                expires_in=expires_in,
                token_type=token_type,
            )

            return response

        except Exception as e:
            logger.error(f"Ошибка при асинхронном получении токена: {str(e)}")
            if isinstance(e, AuthError):
                raise
            raise AuthError(f"Не удалось получить токен доступа: {str(e)}")

    def get_current_token(self) -> AccessTokenResponse:
        """
        Заглушка для синхронного метода в асинхронном клиенте.

        Raises:
            NotImplementedError: Всегда
        """
        raise NotImplementedError(
            "Синхронные методы не реализованы в асинхронном клиенте. "
            "Используйте SyncApiClient для синхронных запросов."
        )

    async def get_current_token_async(self) -> AccessTokenResponse:
        """
        Возвращает текущий токен авторизации.

        Returns:
            Объект с данными токена

        Raises:
            AuthError: Если токен не установлен
        """
        # Если нет токена доступа или он устарел, получаем новый
        if not self.access_token or self._is_token_expired():
            token = await self.get_token_async()

        if not self.access_token:
            raise AuthError("Токен авторизации не установлен")

        return AccessTokenResponse(access_token=self.access_token, expires_at=self.token_expires_at,
                                   token_type=self.token_type)

    def refresh_access_token(self) -> dict[str, Any]:
        """
        Заглушка для синхронного метода в асинхронном клиенте.

        Raises:
            NotImplementedError: Всегда
        """
        raise NotImplementedError(
            "Синхронные методы не реализованы в асинхронном клиенте. "
            "Используйте SyncApiClient для синхронных запросов."
        )

    async def refresh_access_token_async(self) -> dict[str, Any]:
        """
        Асинхронно обновляет токен доступа с использованием refresh_token.

        Returns:
            Информация о новом токене доступа

        Raises:
            AuthError: Если refresh_token не установлен или не удалось обновить токен
        """
        if not self.refresh_token:
            raise AuthError("Невозможно обновить токен: refresh_token не установлен")

        logger.debug("Асинхронное обновление токена доступа с использованием refresh_token")

        data = {
            "grant_type": "refresh_token",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "refresh_token": self.refresh_token,
        }

        try:
            response = await self._request_async(
                method="POST",
                url="/token",
                data=data,
                auth_required=False,
                form_encoded=True,
            )

            access_token = response.get("access_token")
            expires_in = response.get("expires_in", 86400)
            refresh_token = response.get("refresh_token")
            token_type = response.get("token_type", "Bearer")

            if not access_token:
                raise AuthError("Не удалось обновить токен доступа: отсутствует access_token в ответе")

            self._update_token_info(
                access_token=access_token,
                expires_in=expires_in,
                token_type=token_type,
                refresh_token=refresh_token,
            )

            return response

        except Exception as e:
            logger.error(f"Ошибка при асинхронном обновлении токена: {str(e)}")
            if isinstance(e, AuthError):
                raise
            raise AuthError(f"Не удалось обновить токен доступа: {str(e)}")
