"""
Тесты для модуля авторизации.
"""
import pytest
from unittest.mock import patch, MagicMock

from avito_api.auth import (
    SyncAuthClient, AsyncAuthClient, Scope, GrantType,
    GetTokenRequest, GetTokenOAuthRequest, RefreshTokenRequest,
    TokenResponse, OAuth2TokenResponse
)
from avito_api.exceptions import AuthError


class TestSyncAuthClient:
    """Тесты для синхронного клиента авторизации."""

    def test_get_authorization_url(self):
        """Проверка формирования URL для OAuth2 авторизации."""
        auth_client = SyncAuthClient(
            client_id="test_client_id",
            client_secret="test_client_secret"
        )

        # Проверка базового URL с одним скоупом
        url = auth_client.get_authorization_url(
            client_id="test_client_id",
            scopes=[Scope.MESSENGER_READ]
        )

        assert url == "https://avito.ru/oauth?response_type=code&client_id=test_client_id&scope=messenger:read"

        # Проверка URL с несколькими скоупами
        url = auth_client.get_authorization_url(
            client_id="test_client_id",
            scopes=[Scope.MESSENGER_READ, Scope.MESSENGER_WRITE, "custom:scope"]
        )

        assert url == "https://avito.ru/oauth?response_type=code&client_id=test_client_id&scope=messenger:read,messenger:write,custom:scope"

        # Проверка URL с дополнительными параметрами
        url = auth_client.get_authorization_url(
            client_id="test_client_id",
            scopes=[Scope.MESSENGER_READ],
            state="test_state",
            redirect_uri="https://example.com/callback"
        )

        assert "state=test_state" in url
        assert "redirect_uri=https://example.com/callback" in url

    def test_get_token_by_authorization_code(self):
        """Проверка получения токена через код авторизации."""
        auth_client = SyncAuthClient(
            client_id="test_client_id",
            client_secret="test_client_secret"
        )

        # Подменяем метод запроса
        auth_client._request_sync = MagicMock(return_value={
            "access_token": "new_access_token",
            "refresh_token": "new_refresh_token",
            "expires_in": 3600,
            "token_type": "Bearer",
            "scope": "messenger:read messenger:write"
        })

        # Получаем токен
        token_response = auth_client.get_token_by_authorization_code("test_code")

        # Проверяем результат
        assert isinstance(token_response, OAuth2TokenResponse)
        assert token_response.access_token == "new_access_token"
        assert token_response.refresh_token == "new_refresh_token"
        assert token_response.expires_in == 3600
        assert token_response.token_type == "Bearer"
        assert token_response.scope == "messenger:read messenger:write"

        # Проверяем обновление токенов в клиенте
        assert auth_client.access_token == "new_access_token"
        assert auth_client.refresh_token == "new_refresh_token"
        assert auth_client.token_type == "Bearer"

        # Проверяем вызов метода запроса
        auth_client._request_sync.assert_called_once_with(
            method="POST",
            url="/token",
            data={
                "grant_type": "authorization_code",
                "client_id": "test_client_id",
                "client_secret": "test_client_secret",
                "code": "test_code",
            },
            auth_required=False,
            form_encoded=True,
        )

    def test_get_token_by_authorization_code_error(self):
        """Проверка обработки ошибок при получении токена через код авторизации."""
        auth_client = SyncAuthClient(
            client_id="test_client_id",
            client_secret="test_client_secret"
        )

        # Подменяем метод запроса с имитацией ошибки
        auth_client._request_sync = MagicMock(side_effect=AuthError("Invalid code"))

        # Проверяем вызов исключения
        with pytest.raises(AuthError) as e:
            auth_client.get_token_by_authorization_code("invalid_code")

        assert "Invalid code" in str(e.value)


class TestAsyncAuthClient:
    """Тесты для асинхронного клиента авторизации."""

    @pytest.mark.asyncio
    async def test_get_token_by_authorization_code(self):
        """Проверка асинхронного получения токена через код авторизации."""
        auth_client = AsyncAuthClient(
            client_id="test_client_id",
            client_secret="test_client_secret"
        )

        # Подменяем метод запроса
        auth_client._request_async = MagicMock(return_value={
            "access_token": "new_access_token",
            "refresh_token": "new_refresh_token",
            "expires_in": 3600,
            "token_type": "Bearer",
            "scope": "messenger:read messenger:write"
        })

        # Получаем токен
        token_response = await auth_client.get_token_by_authorization_code("test_code")

        # Проверяем результат
        assert isinstance(token_response, OAuth2TokenResponse)
        assert token_response.access_token == "new_access_token"
        assert token_response.refresh_token == "new_refresh_token"
        assert token_response.expires_in == 3600
        assert token_response.token_type == "Bearer"
        assert token_response.scope == "messenger:read messenger:write"

        # Проверяем обновление токенов в клиенте
        assert auth_client.access_token == "new_access_token"
        assert auth_client.refresh_token == "new_refresh_token"
        assert auth_client.token_type == "Bearer"

        # Проверяем вызов метода запроса
        auth_client._request_async.assert_called_once_with(
            method="POST",
            url="/token",
            data={
                "grant_type": "authorization_code",
                "client_id": "test_client_id",
                "client_secret": "test_client_secret",
                "code": "test_code",
            },
            auth_required=False,
            form_encoded=True,
        )

    @pytest.mark.asyncio
    async def test_get_token_by_authorization_code_error(self):
        """Проверка обработки ошибок при асинхронном получении токена через код авторизации."""
        auth_client = AsyncAuthClient(
            client_id="test_client_id",
            client_secret="test_client_secret"
        )

        # Подменяем метод запроса с имитацией ошибки
        error = AuthError("Invalid code")
        auth_client._request_async = MagicMock(side_effect=error)

        # Проверяем вызов исключения
        with pytest.raises(AuthError) as e:
            await auth_client.get_token_by_authorization_code("invalid_code")

        assert "Invalid code" in str(e.value)


class TestModels:
    """Тесты для моделей данных модуля авторизации."""

    def test_token_response(self):
        """Проверка модели TokenResponse."""
        data = {
            "access_token": "test_access_token",
            "expires_in": 3600,
            "token_type": "Bearer"
        }

        token = TokenResponse(**data)

        assert token.access_token == "test_access_token"
        assert token.expires_in == 3600
        assert token.token_type == "Bearer"

    def test_oauth2_token_response(self):
        """Проверка модели OAuth2TokenResponse."""
        data = {
            "access_token": "test_access_token",
            "refresh_token": "test_refresh_token",
            "expires_in": 3600,
            "token_type": "Bearer",
            "scope": "messenger:read messenger:write"
        }

        token = OAuth2TokenResponse(**data)

        assert token.access_token == "test_access_token"
        assert token.refresh_token == "test_refresh_token"
        assert token.expires_in == 3600
        assert token.token_type == "Bearer"
        assert token.scope == "messenger:read messenger:write"

    def test_get_token_request(self):
        """Проверка модели GetTokenRequest."""
        data = {
            "client_id": "test_client_id",
            "client_secret": "test_client_secret"
        }

        request = GetTokenRequest(**data)

        assert request.client_id == "test_client_id"
        assert request.client_secret == "test_client_secret"
        assert request.grant_type == GrantType.CLIENT_CREDENTIALS

    def test_get_token_oauth_request(self):
        """Проверка модели GetTokenOAuthRequest."""
        data = {
            "client_id": "test_client_id",
            "client_secret": "test_client_secret",
            "code": "test_code"
        }

        request = GetTokenOAuthRequest(**data)

        assert request.client_id == "test_client_id"
        assert request.client_secret == "test_client_secret"
        assert request.code == "test_code"
        assert request.grant_type == GrantType.AUTHORIZATION_CODE

    def test_refresh_token_request(self):
        """Проверка модели RefreshTokenRequest."""
        data = {
            "client_id": "test_client_id",
            "client_secret": "test_client_secret",
            "refresh_token": "test_refresh_token"
        }

        request = RefreshTokenRequest(**data)

        assert request.client_id == "test_client_id"
        assert request.client_secret == "test_client_secret"
        assert request.refresh_token == "test_refresh_token"
        assert request.grant_type == GrantType.REFRESH_TOKEN
