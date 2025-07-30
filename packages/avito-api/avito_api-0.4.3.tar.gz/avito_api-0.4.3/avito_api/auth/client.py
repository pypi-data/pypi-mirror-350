"""
Клиент для работы с API авторизации Авито.
"""
from typing import Optional, Union

from .models import GetTokenOAuthRequest, OAuth2TokenResponse, Scope
from ..client import SyncApiClient, AsyncApiClient
from ..config import logger
from ..exceptions import AuthError


class OAuth2Client:
    """
    Базовый класс для работы с API авторизации Авито.
    """

    def get_authorization_url(
        self,
        client_id: str,
        scopes: list[Union[Scope, str]],
        state: Optional[str] = None,
        redirect_uri: Optional[str] = None,
    ) -> str:
        """
        Формирует URL для OAuth2 авторизации.

        Args:
            client_id: Идентификатор клиента
            scopes: Список запрашиваемых разрешений
            state: Произвольная строка для защиты от CSRF-атак
            redirect_uri: URL для перенаправления после авторизации

        Returns:
            URL для авторизации
        """
        # Преобразуем scopes в строки если они переданы как Enum
        scope_strings = [s.value if isinstance(s, Scope) else s for s in scopes]
        scope_param = ",".join(scope_strings)

        url = f"https://avito.ru/oauth?response_type=code&client_id={client_id}&scope={scope_param}"

        if state:
            url += f"&state={state}"

        if redirect_uri:
            url += f"&redirect_uri={redirect_uri}"

        logger.debug(f"Сформирован URL для OAuth2 авторизации: {url}")
        return url


class SyncAuthClient(OAuth2Client, SyncApiClient):
    """
    Синхронный клиент для работы с API авторизации Авито.

    Предоставляет методы для получения и обновления токенов доступа.
    """

    def get_token_by_authorization_code(self, code: str) -> OAuth2TokenResponse:
        """
        Получает токен доступа через код авторизации (authorization_code).

        Args:
            code: Код авторизации, полученный после подтверждения прав пользователем

        Returns:
            Информация о полученном токене доступа

        Raises:
            AuthError: Если не удалось получить токен
        """
        logger.debug("Запрос токена доступа через authorization_code")

        request = GetTokenOAuthRequest(
            client_id=self.client_id,
            client_secret=self.client_secret,
            code=code,
        )

        response = self._request_sync(
            method="POST",
            url="/token",
            data=request.dict(),
            auth_required=False,
            form_encoded=True,
        )

        try:
            token_response = OAuth2TokenResponse(**response)

            # Обновляем информацию о токене
            self._update_token_info(
                access_token=token_response.access_token,
                expires_in=token_response.expires_in,
                token_type=token_response.token_type,
                refresh_token=token_response.refresh_token,
            )

            return token_response

        except Exception as e:
            logger.error(f"Ошибка при обработке ответа на запрос токена: {str(e)}")
            raise AuthError(f"Не удалось обработать ответ на запрос токена: {str(e)}")


class AsyncAuthClient(OAuth2Client, AsyncApiClient):
    """
    Асинхронный клиент для работы с API авторизации Авито.

    Предоставляет асинхронные методы для получения и обновления токенов доступа.
    """

    async def get_token_by_authorization_code(self, code: str) -> OAuth2TokenResponse:
        """
        Асинхронно получает токен доступа через код авторизации (authorization_code).

        Args:
            code: Код авторизации, полученный после подтверждения прав пользователем

        Returns:
            Информация о полученном токене доступа

        Raises:
            AuthError: Если не удалось получить токен
        """
        logger.debug("Асинхронный запрос токена доступа через authorization_code")

        request = GetTokenOAuthRequest(
            client_id=self.client_id,
            client_secret=self.client_secret,
            code=code,
        )

        response = await self._request_async(
            method="POST",
            url="/token",
            data=request.dict(),
            auth_required=False,
            form_encoded=True,
        )

        try:
            token_response = OAuth2TokenResponse(**response)

            # Обновляем информацию о токене
            self._update_token_info(
                access_token=token_response.access_token,
                expires_in=token_response.expires_in,
                token_type=token_response.token_type,
                refresh_token=token_response.refresh_token,
            )

            return token_response

        except Exception as e:
            logger.error(f"Ошибка при обработке ответа на асинхронный запрос токена: {str(e)}")
            raise AuthError(f"Не удалось обработать ответ на запрос токена: {str(e)}")
