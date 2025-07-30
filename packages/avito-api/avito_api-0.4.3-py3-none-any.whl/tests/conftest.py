"""
Общие фикстуры и конфигурация для тестов.
"""
import os
import json
import pytest
from unittest.mock import patch, MagicMock

from avito_api.config import ClientConfig
from avito_api.auth import SyncAuthClient, AsyncAuthClient
from avito_api.messenger import SyncMessengerClient, AsyncMessengerClient

# Тестовые данные
TEST_CLIENT_ID = "test_client_id"
TEST_CLIENT_SECRET = "test_client_secret"
TEST_ACCESS_TOKEN = "test_access_token"
TEST_REFRESH_TOKEN = "test_refresh_token"
TEST_USER_ID = 12345
TEST_CHAT_ID = "test_chat_id"
TEST_MESSAGE_ID = "test_message_id"


@pytest.fixture
def client_config():
    """Фикстура для тестовой конфигурации клиента."""
    return ClientConfig()


@pytest.fixture
def mock_response():
    """Фикстура для создания мок-ответа."""

    def _create_mock_response(status_code=200, json_data=None, content=None, headers=None):
        mock_resp = MagicMock()
        mock_resp.status_code = status_code

        if json_data is not None:
            mock_resp.json = MagicMock(return_value=json_data)

            # Для requests content - это bytes, для httpx - это str
            if content is None:
                content = json.dumps(json_data).encode('utf-8')

        mock_resp.content = content or b''
        mock_resp.headers = headers or {}

        return mock_resp

    return _create_mock_response


@pytest.fixture
def mock_token_response(mock_response):
    """Фикстура для мок-ответа с токеном."""
    return mock_response(
        json_data={
            "access_token": TEST_ACCESS_TOKEN,
            "refresh_token": TEST_REFRESH_TOKEN,
            "expires_in": 86400,
            "token_type": "Bearer"
        }
    )


@pytest.fixture
def mock_chats_response(mock_response):
    """Фикстура для мок-ответа со списком чатов."""
    return mock_response(
        json_data={
            "chats": [
                {
                    "id": TEST_CHAT_ID,
                    "created": 1600000000,
                    "updated": 1600000100,
                    "users": [
                        {
                            "id": TEST_USER_ID,
                            "name": "Test User"
                        },
                        {
                            "id": 67890,
                            "name": "Another User"
                        }
                    ],
                    "last_message": {
                        "id": TEST_MESSAGE_ID,
                        "author_id": 67890,
                        "content": {
                            "text": "Test message"
                        },
                        "created": 1600000100,
                        "direction": "in",
                        "type": "text"
                    }
                }
            ]
        }
    )


@pytest.fixture
def mock_messages_response(mock_response):
    """Фикстура для мок-ответа со списком сообщений."""
    return mock_response(
        json_data=[
            {
                "id": TEST_MESSAGE_ID,
                "author_id": 67890,
                "content": {
                    "text": "Test message"
                },
                "created": 1600000100,
                "direction": "in",
                "is_read": True,
                "type": "text"
            },
            {
                "id": "another_message_id",
                "author_id": TEST_USER_ID,
                "content": {
                    "text": "Reply message"
                },
                "created": 1600000200,
                "direction": "out",
                "is_read": False,
                "type": "text"
            }
        ]
    )


@pytest.fixture
def mock_send_message_response(mock_response):
    """Фикстура для мок-ответа при отправке сообщения."""
    return mock_response(
        json_data={
            "id": "new_message_id",
            "content": {
                "text": "New test message"
            },
            "created": 1600000300,
            "direction": "out",
            "type": "text",
            "author_id": TEST_USER_ID
        }
    )


@pytest.fixture
def mock_success_response(mock_response):
    """Фикстура для мок-ответа с успешным результатом."""
    return mock_response(
        json_data={
            "ok": True
        }
    )


@pytest.fixture
def sync_auth_client():
    """Фикстура для синхронного клиента авторизации."""
    with patch('avito_api.auth.client.SyncAuthClient._request_sync') as mock_request:
        client = SyncAuthClient(
            client_id=TEST_CLIENT_ID,
            client_secret=TEST_CLIENT_SECRET
        )

        # Патчим метод получения токена
        def mock_get_token():
            return {
                "access_token": TEST_ACCESS_TOKEN,
                "expires_in": 86400,
                "token_type": "Bearer"
            }

        client.get_token = MagicMock(side_effect=mock_get_token)

        yield client


@pytest.fixture
def async_auth_client():
    """Фикстура для асинхронного клиента авторизации."""
    with patch('avito_api.auth.client.AsyncAuthClient._request_async') as mock_request:
        client = AsyncAuthClient(
            client_id=TEST_CLIENT_ID,
            client_secret=TEST_CLIENT_SECRET
        )

        # Патчим метод получения токена
        async def mock_get_token_async():
            return {
                "access_token": TEST_ACCESS_TOKEN,
                "expires_in": 86400,
                "token_type": "Bearer"
            }

        client.get_token_async = MagicMock(side_effect=mock_get_token_async)

        yield client


@pytest.fixture
def sync_messenger_client():
    """Фикстура для синхронного клиента мессенджера."""
    with patch('avito_api.messenger.client.SyncMessengerClient._request_sync') as mock_request:
        client = SyncMessengerClient(
            client_id=TEST_CLIENT_ID,
            client_secret=TEST_CLIENT_SECRET,
            access_token=TEST_ACCESS_TOKEN
        )
        yield client


@pytest.fixture
def async_messenger_client():
    """Фикстура для асинхронного клиента мессенджера."""
    with patch('avito_api.messenger.client.AsyncMessengerClient._request_async') as mock_request:
        client = AsyncMessengerClient(
            client_id=TEST_CLIENT_ID,
            client_secret=TEST_CLIENT_SECRET,
            access_token=TEST_ACCESS_TOKEN
        )
        yield client
