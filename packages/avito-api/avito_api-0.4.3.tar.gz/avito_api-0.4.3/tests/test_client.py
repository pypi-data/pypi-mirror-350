"""
Тесты для базовых клиентов API.
"""
import json
import time
import pytest
import requests
import httpx
from unittest.mock import patch, MagicMock, call

from avito_api.client import SyncApiClient, AsyncApiClient
from avito_api.exceptions import (
    AvitoApiError, AuthError, TokenExpiredError, NetworkError, ForbiddenError,
    NotFoundError, ValidationError, RateLimitError, ServerError
)


class TestSyncApiClient:
    """Тесты для синхронного клиента API."""

    def test_init(self):
        """Проверка инициализации клиента."""
        client = SyncApiClient(
            client_id="test_client_id",
            client_secret="test_client_secret"
        )

        assert client.client_id == "test_client_id"
        assert client.client_secret == "test_client_secret"
        assert client.access_token is None
        assert client.refresh_token is None
        assert client.token_expires_at is None
        assert client.token_type == "Bearer"

    def test_build_url(self):
        """Проверка формирования полного URL."""
        client = SyncApiClient(
            client_id="test_client_id",
            client_secret="test_client_secret"
        )

        # Проверка с базовым URL по умолчанию
        assert client._build_url("/test/endpoint") == "https://api.avito.ru/test/endpoint"

        # Проверка с кастомным базовым URL
        client.config.api.base_url = "https://custom-api.avito.ru"
        assert client._build_url("/test/endpoint") == "https://custom-api.avito.ru/test/endpoint"

        # Проверка обработки слешей
        assert client._build_url("test/endpoint") == "https://custom-api.avito.ru/test/endpoint"
        assert client._build_url("/test/endpoint/") == "https://custom-api.avito.ru/test/endpoint/"

    def test_get_auth_header(self):
        """Проверка формирования заголовков авторизации."""
        client = SyncApiClient(
            client_id="test_client_id",
            client_secret="test_client_secret",
            access_token="test_access_token"
        )

        # Проверка заголовка с токеном
        assert client._get_auth_header() == {"Authorization": "Bearer test_access_token"}

        # Проверка с другим типом токена
        client.token_type = "Custom"
        assert client._get_auth_header() == {"Authorization": "Custom test_access_token"}

        # Проверка ошибки без токена
        client.access_token = None
        with pytest.raises(AuthError):
            client._get_auth_header()

    def test_is_token_expired(self):
        """Проверка определения истечения токена."""
        client = SyncApiClient(
            client_id="test_client_id",
            client_secret="test_client_secret"
        )

        # Без установленного срока истечения
        assert client._is_token_expired() is True

        # Токен истекает в будущем
        client.token_expires_at = time.time() + 3600  # +1 час
        assert client._is_token_expired() is False

        # Токен истекает в ближайшем будущем (меньше порога)
        client.token_expires_at = time.time() + 60  # +1 минута
        client.config.api.token_refresh_threshold = 300  # 5 минут
        assert client._is_token_expired() is True

        # Токен уже истек
        client.token_expires_at = time.time() - 3600  # -1 час
        assert client._is_token_expired() is True

    def test_update_token_info(self):
        """Проверка обновления информации о токене."""
        client = SyncApiClient(
            client_id="test_client_id",
            client_secret="test_client_secret"
        )

        # Обновляем токен
        client._update_token_info(
            access_token="new_access_token",
            expires_in=3600,
            token_type="Custom",
            refresh_token="new_refresh_token"
        )

        assert client.access_token == "new_access_token"
        assert client.token_type == "Custom"
        assert client.refresh_token == "new_refresh_token"

        # Проверяем срок истечения (с погрешностью)
        now = time.time()
        assert abs(client.token_expires_at - (now + 3600)) < 1

    @patch('requests.request')
    def test_request_sync_success(self, mock_request):
        """Проверка успешного выполнения синхронного запроса."""
        # Создаем мок-ответ
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = json.dumps({"key": "value"}).encode("utf-8")
        mock_response.headers = {
            "X-RateLimit-Limit": "100",
            "X-RateLimit-Remaining": "99"
        }

        mock_request.return_value = mock_response

        client = SyncApiClient(
            client_id="test_client_id",
            client_secret="test_client_secret",
            access_token="test_access_token"
        )

        # Выполняем запрос
        result = client._request_sync(
            method="GET",
            url="/test/endpoint",
            params={"param": "value"},
            auth_required=True
        )

        # Проверяем результат
        assert result == {"key": "value"}

        # Проверяем, что запрос был выполнен с правильными параметрами
        mock_request.assert_called_once_with(
            method="GET",
            url="https://api.avito.ru/test/endpoint",
            params={"param": "value"},
            data=None,
            json=None,
            headers={
                "User-Agent": "AvitoApiClient/1.0",
                "Authorization": "Bearer test_access_token"
            },
            files=None,
            timeout=30.0
        )

    @patch('requests.request')
    def test_request_sync_error_handling(self, mock_request):
        """Проверка обработки ошибок при синхронном запросе."""
        # Создаем мок-ответ с ошибкой
        mock_response = MagicMock()
        mock_response.status_code = 401
        mock_response.content = json.dumps({
            "error": {
                "code": 401,
                "message": "Unauthorized"
            }
        }).encode("utf-8")
        mock_response.headers = {}

        mock_request.return_value = mock_response

        client = SyncApiClient(
            client_id="test_client_id",
            client_secret="test_client_secret",
            access_token="test_access_token"
        )

        # Проверяем вызов исключения
        with pytest.raises(AuthError) as e:
            client._request_sync(
                method="GET",
                url="/test/endpoint",
                auth_required=True
            )

        assert "Unauthorized" in str(e.value)

    @patch('requests.request')
    def test_request_sync_network_error(self, mock_request):
        """Проверка обработки сетевых ошибок при синхронном запросе."""
        # Имитируем сетевую ошибку
        mock_request.side_effect = requests.exceptions.ConnectionError("Connection error")

        client = SyncApiClient(
            client_id="test_client_id",
            client_secret="test_client_secret",
            access_token="test_access_token"
        )

        # Проверяем вызов исключения
        with pytest.raises(NetworkError) as e:
            client._request_sync(
                method="GET",
                url="/test/endpoint",
                auth_required=True
            )

        assert "Connection error" in str(e.value)

    @patch('requests.request')
    def test_request_sync_token_refresh(self, mock_request):
        """Проверка автоматического обновления токена при 401 ошибке."""
        # Создаем последовательность ответов: ошибка 401, затем успешный ответ
        unauthorized_response = MagicMock()
        unauthorized_response.status_code = 401
        unauthorized_response.content = json.dumps({
            "error": {
                "code": 401,
                "message": "Token expired"
            }
        }).encode("utf-8")
        unauthorized_response.headers = {}

        success_response = MagicMock()
        success_response.status_code = 200
        success_response.content = json.dumps({"key": "value"}).encode("utf-8")
        success_response.headers = {}

        mock_request.side_effect = [unauthorized_response, success_response]

        client = SyncApiClient(
            client_id="test_client_id",
            client_secret="test_client_secret",
            access_token="test_access_token",
            refresh_token="test_refresh_token"
        )

        # Подменяем методы обновления токена
        client.get_token = MagicMock()
        client.get_token.return_value = {
            "access_token": "new_access_token",
            "expires_in": 3600,
            "token_type": "Bearer"
        }

        # Выполняем запрос
        result = client._request_sync(
            method="GET",
            url="/test/endpoint",
            auth_required=True
        )

        # Проверяем результат
        assert result == {"key": "value"}

        # Проверяем, что токен был обновлен
        client.get_token.assert_called_once()

        # Проверяем, что было выполнено два запроса
        assert mock_request.call_count == 2

    def test_get_token(self, mock_token_response):
        """Проверка получения токена."""
        client = SyncApiClient(
            client_id="test_client_id",
            client_secret="test_client_secret"
        )

        # Подменяем метод запроса
        client._request_sync = MagicMock(return_value={
            "access_token": "new_access_token",
            "expires_in": 3600,
            "token_type": "Bearer"
        })

        # Получаем токен
        result = client.get_token()

        # Проверяем результат
        assert result == {
            "access_token": "new_access_token",
            "expires_in": 3600,
            "token_type": "Bearer"
        }

        # Проверяем обновление токена в клиенте
        assert client.access_token == "new_access_token"
        assert client.token_type == "Bearer"

        # Проверяем вызов метода запроса
        client._request_sync.assert_called_once_with(
            method="POST",
            url="/token",
            data={
                "grant_type": "client_credentials",
                "client_id": "test_client_id",
                "client_secret": "test_client_secret",
            },
            auth_required=False,
            form_encoded=True,
        )

    def test_refresh_access_token(self):
        """Проверка обновления токена доступа."""
        client = SyncApiClient(
            client_id="test_client_id",
            client_secret="test_client_secret",
            access_token="test_access_token",
            refresh_token="test_refresh_token"
        )

        # Подменяем метод запроса
        client._request_sync = MagicMock(return_value={
            "access_token": "new_access_token",
            "refresh_token": "new_refresh_token",
            "expires_in": 3600,
            "token_type": "Bearer"
        })

        # Обновляем токен
        result = client.refresh_access_token()

        # Проверяем результат
        assert result == {
            "access_token": "new_access_token",
            "refresh_token": "new_refresh_token",
            "expires_in": 3600,
            "token_type": "Bearer"
        }

        # Проверяем обновление токенов в клиенте
        assert client.access_token == "new_access_token"
        assert client.refresh_token == "new_refresh_token"
        assert client.token_type == "Bearer"

        # Проверяем вызов метода запроса
        client._request_sync.assert_called_once_with(
            method="POST",
            url="/token",
            data={
                "grant_type": "refresh_token",
                "client_id": "test_client_id",
                "client_secret": "test_client_secret",
                "refresh_token": "test_refresh_token",
            },
            auth_required=False,
            form_encoded=True,
        )


class TestAsyncApiClient:
    """Тесты для асинхронного клиента API."""

    def test_init(self):
        """Проверка инициализации клиента."""
        client = AsyncApiClient(
            client_id="test_client_id",
            client_secret="test_client_secret"
        )

        assert client.client_id == "test_client_id"
        assert client.client_secret == "test_client_secret"
        assert client.access_token is None
        assert client.refresh_token is None
        assert client.token_expires_at is None
        assert client.token_type == "Bearer"

    @pytest.mark.asyncio
    async def test_request_async_success(self):
        """Проверка успешного выполнения асинхронного запроса."""
        # Создаем мок-объект для AsyncClient и Response
        mock_client = MagicMock()
        mock_response = MagicMock()

        # Настраиваем мок-ответ
        mock_response.status_code = 200
        mock_response.content = json.dumps({"key": "value"}).encode("utf-8")
        mock_response.headers = {
            "X-RateLimit-Limit": "100",
            "X-RateLimit-Remaining": "99"
        }

        # Настраиваем мок-клиент
        mock_client.request.return_value.__aenter__.return_value = mock_response

        # Патчим httpx.AsyncClient
        with patch('httpx.AsyncClient', return_value=mock_client):
            client = AsyncApiClient(
                client_id="test_client_id",
                client_secret="test_client_secret",
                access_token="test_access_token"
            )

            # Выполняем запрос
            result = await client._request_async(
                method="GET",
                url="/test/endpoint",
                params={"param": "value"},
                auth_required=True
            )

            # Проверяем результат
            assert result == {"key": "value"}

            # Проверяем, что запрос был выполнен с правильными параметрами
            mock_client.request.assert_called_once_with(
                method="GET",
                url="https://api.avito.ru/test/endpoint",
                params={"param": "value"},
                data=None,
                json=None,
                headers={
                    "User-Agent": "AvitoApiClient/1.0",
                    "Authorization": "Bearer test_access_token"
                },
                files=None,
            )

    @pytest.mark.asyncio
    async def test_request_async_error_handling(self):
        """Проверка обработки ошибок при асинхронном запросе."""
        # Создаем мок-объект для AsyncClient и Response
        mock_client = MagicMock()
        mock_response = MagicMock()

        # Настраиваем мок-ответ с ошибкой
        mock_response.status_code = 404
        mock_response.content = json.dumps({
            "error": {
                "code": 404,
                "message": "Not Found"
            }
        }).encode("utf-8")
        mock_response.headers = {}

        # Настраиваем мок-клиент
        mock_client.request.return_value.__aenter__.return_value = mock_response

        # Патчим httpx.AsyncClient
        with patch('httpx.AsyncClient', return_value=mock_client):
            client = AsyncApiClient(
                client_id="test_client_id",
                client_secret="test_client_secret",
                access_token="test_access_token"
            )

            # Проверяем вызов исключения
            with pytest.raises(NotFoundError) as e:
                await client._request_async(
                    method="GET",
                    url="/test/endpoint",
                    auth_required=True
                )

            assert "Not Found" in str(e.value)

    @pytest.mark.asyncio
    async def test_request_async_network_error(self):
        """Проверка обработки сетевых ошибок при асинхронном запросе."""
        # Создаем мок-объект для AsyncClient
        mock_client = MagicMock()

        # Имитируем сетевую ошибку
        mock_client.request.return_value.__aenter__.side_effect = httpx.HTTPError("Connection error")

        # Патчим httpx.AsyncClient
        with patch('httpx.AsyncClient', return_value=mock_client):
            client = AsyncApiClient(
                client_id="test_client_id",
                client_secret="test_client_secret",
                access_token="test_access_token"
            )

            # Проверяем вызов исключения
            with pytest.raises(NetworkError) as e:
                await client._request_async(
                    method="GET",
                    url="/test/endpoint",
                    auth_required=True
                )

            assert "Connection error" in str(e.value)

    @pytest.mark.asyncio
    async def test_get_token_async(self):
        """Проверка асинхронного получения токена."""
        client = AsyncApiClient(
            client_id="test_client_id",
            client_secret="test_client_secret"
        )

        # Подменяем метод запроса
        client._request_async = MagicMock(return_value={
            "access_token": "new_access_token",
            "expires_in": 3600,
            "token_type": "Bearer"
        })

        # Получаем токен
        result = await client.get_token_async()

        # Проверяем результат
        assert result == {
            "access_token": "new_access_token",
            "expires_in": 3600,
            "token_type": "Bearer"
        }

        # Проверяем обновление токена в клиенте
        assert client.access_token == "new_access_token"
        assert client.token_type == "Bearer"

        # Проверяем вызов метода запроса
        client._request_async.assert_called_once_with(
            method="POST",
            url="/token",
            data={
                "grant_type": "client_credentials",
                "client_id": "test_client_id",
                "client_secret": "test_client_secret",
            },
            auth_required=False,
            form_encoded=True,
        )

    @pytest.mark.asyncio
    async def test_refresh_access_token_async(self):
        """Проверка асинхронного обновления токена доступа."""
        client = AsyncApiClient(
            client_id="test_client_id",
            client_secret="test_client_secret",
            access_token="test_access_token",
            refresh_token="test_refresh_token"
        )

        # Подменяем метод запроса
        client._request_async = MagicMock(return_value={
            "access_token": "new_access_token",
            "refresh_token": "new_refresh_token",
            "expires_in": 3600,
            "token_type": "Bearer"
        })

        # Обновляем токен
        result = await client.refresh_access_token_async()

        # Проверяем результат
        assert result == {
            "access_token": "new_access_token",
            "refresh_token": "new_refresh_token",
            "expires_in": 3600,
            "token_type": "Bearer"
        }

        # Проверяем обновление токенов в клиенте
        assert client.access_token == "new_access_token"
        assert client.refresh_token == "new_refresh_token"
        assert client.token_type == "Bearer"

        # Проверяем вызов метода запроса
        client._request_async.assert_called_once_with(
            method="POST",
            url="/token",
            data={
                "grant_type": "refresh_token",
                "client_id": "test_client_id",
                "client_secret": "test_client_secret",
                "refresh_token": "test_refresh_token",
            },
            auth_required=False,
            form_encoded=True,
        )
