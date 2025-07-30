"""
Тесты для модуля мессенджера.
"""
import os
import json
import pytest
from unittest.mock import patch, MagicMock, mock_open

from avito_api.messenger import (
    SyncMessengerClient, AsyncMessengerClient, ChatType, MessageType,
    MessageDirection, Chats, Chat, Messages, Message, SuccessResponse,
    BlacklistUser, BlacklistUserContext, BlacklistReasonId
)
from avito_api.exceptions import ValidationError


class TestSyncMessengerClient:
    """Тесты для синхронного клиента мессенджера."""

    def test_validate_message_text(self, sync_messenger_client):
        """Проверка валидации текста сообщения."""
        # Проверка валидного текста
        sync_messenger_client._validate_message_text("Test message")

        # Проверка пустого текста
        with pytest.raises(ValidationError):
            sync_messenger_client._validate_message_text("")

        # Проверка None вместо текста
        with pytest.raises(ValidationError):
            sync_messenger_client._validate_message_text(None)

        # Проверка слишком длинного текста
        with pytest.raises(ValidationError):
            sync_messenger_client._validate_message_text("a" * 5000)

    def test_get_chats(self, sync_messenger_client, mock_chats_response):
        """Проверка получения списка чатов."""
        # Подменяем метод запроса
        sync_messenger_client._request_sync = MagicMock(return_value={
            "chats": [
                {
                    "id": "test_chat_id",
                    "created": 1600000000,
                    "updated": 1600000100,
                    "users": [
                        {
                            "id": 12345,
                            "name": "Test User"
                        }
                    ],
                    "last_message": {
                        "id": "test_message_id",
                        "author_id": 12345,
                        "content": {
                            "text": "Test message"
                        },
                        "created": 1600000100,
                        "direction": "out",
                        "type": "text"
                    }
                }
            ]
        })

        # Получаем чаты
        chats = sync_messenger_client.get_chats(
            user_id=12345,
            limit=10,
            unread_only=True,
            chat_types=[ChatType.USER_TO_ITEM]
        )

        # Проверяем результат
        assert isinstance(chats, Chats)
        assert len(chats.chats) == 1
        assert chats.chats[0].id == "test_chat_id"
        assert chats.chats[0].created == 1600000000
        assert chats.chats[0].last_message.type == "text"
        assert chats.chats[0].last_message.content.text == "Test message"

        # Проверяем вызов метода запроса
        sync_messenger_client._request_sync.assert_called_once_with(
            method="GET",
            url="/messenger/v2/accounts/12345/chats",
            params={
                "unread_only": True,
                "limit": 10,
                "offset": 0,
                "chat_types": "u2i",
            }
        )

    def test_get_chat(self, sync_messenger_client):
        """Проверка получения информации о чате."""
        # Подменяем метод запроса
        sync_messenger_client._request_sync = MagicMock(return_value={
            "id": "test_chat_id",
            "created": 1600000000,
            "updated": 1600000100,
            "users": [
                {
                    "id": 12345,
                    "name": "Test User"
                }
            ],
            "last_message": {
                "id": "test_message_id",
                "author_id": 12345,
                "content": {
                    "text": "Test message"
                },
                "created": 1600000100,
                "direction": "out",
                "type": "text"
            }
        })

        # Получаем чат
        chat = sync_messenger_client.get_chat(
            user_id=12345,
            chat_id="test_chat_id"
        )

        # Проверяем результат
        assert isinstance(chat, Chat)
        assert chat.id == "test_chat_id"
        assert chat.created == 1600000000
        assert chat.last_message.type == "text"
        assert chat.last_message.content.text == "Test message"

        # Проверяем вызов метода запроса
        sync_messenger_client._request_sync.assert_called_once_with(
            method="GET",
            url="/messenger/v2/accounts/12345/chats/test_chat_id",
        )

    def test_get_messages(self, sync_messenger_client, mock_messages_response):
        """Проверка получения списка сообщений."""
        # Подменяем метод запроса
        sync_messenger_client._request_sync = MagicMock(return_value=[
            {
                "id": "test_message_id",
                "author_id": 12345,
                "content": {
                    "text": "Test message"
                },
                "created": 1600000100,
                "direction": "out",
                "is_read": True,
                "type": "text"
            }
        ])

        # Получаем сообщения
        messages = sync_messenger_client.get_messages(
            user_id=12345,
            chat_id="test_chat_id",
            limit=10,
            offset=5
        )

        # Проверяем результат
        assert isinstance(messages, Messages)
        assert len(messages.__root__) == 1
        assert messages.__root__[0].id == "test_message_id"
        assert messages.__root__[0].type == "text"
        assert messages.__root__[0].content.text == "Test message"

        # Проверяем вызов метода запроса
        sync_messenger_client._request_sync.assert_called_once_with(
            method="GET",
            url="/messenger/v3/accounts/12345/chats/test_chat_id/messages/",
            params={
                "limit": 10,
                "offset": 5,
            }
        )

    def test_send_message(self, sync_messenger_client, mock_send_message_response):
        """Проверка отправки текстового сообщения."""
        # Подменяем метод запроса
        sync_messenger_client._request_sync = MagicMock(return_value={
            "id": "new_message_id",
            "content": {
                "text": "Test message"
            },
            "created": 1600000300,
            "direction": "out",
            "type": "text",
            "author_id": 12345
        })

        # Отправляем сообщение
        message = sync_messenger_client.send_message(
            user_id=12345,
            chat_id="test_chat_id",
            text="Test message"
        )

        # Проверяем результат
        assert isinstance(message, Message)
        assert message.id == "new_message_id"
        assert message.type == "text"
        assert message.content.text == "Test message"

        # Проверяем вызов метода запроса
        async_messenger_client._request_async.assert_called_once_with(
            method="POST",
            url="/messenger/v1/accounts/12345/chats/test_chat_id/messages",
            json_data={
                "type": "text",
                "message": {
                    "text": "Test message"
                }
            }
        )

    @pytest.mark.asyncio
    async def test_upload_image_from_bytes(self, async_messenger_client):
        """Проверка асинхронной загрузки изображения из байтов."""
        # Подменяем метод запроса
        async_messenger_client._request_async = MagicMock(return_value={
            "test_image_id": {
                "140x105": "https://example.com/image_140_105.jpg",
                "32x32": "https://example.com/image_32_32.jpg"
            }
        })

        # Загружаем изображение
        result = await async_messenger_client.upload_image(
            user_id=12345,
            image_file=b"image_content"
        )

        # Проверяем результат
        assert result == {
            "test_image_id": {
                "140x105": "https://example.com/image_140_105.jpg",
                "32x32": "https://example.com/image_32_32.jpg"
            }
        }

        # Проверяем вызов метода запроса
        async_messenger_client._request_async.assert_called_once()

        # Проверяем, что запрос был выполнен с файлами
        call_args = async_messenger_client._request_async.call_args
        assert call_args[1]["method"] == "POST"
        assert call_args[1]["url"] == "/messenger/v1/accounts/12345/uploadImages"
        assert "files" in call_args[1]
        assert call_args[1]["files"]["uploadfile[]"][1] == b"image_content"

    @pytest.mark.asyncio
    async def test_upload_image_from_path(self, async_messenger_client):
        """Проверка асинхронной загрузки изображения из файла."""
        # Подменяем метод запроса
        async_messenger_client._request_async = MagicMock(return_value={
            "test_image_id": {
                "140x105": "https://example.com/image_140_105.jpg",
                "32x32": "https://example.com/image_32_32.jpg"
            }
        })

        # Подменяем open и os.path.isfile
        with patch("os.path.isfile", return_value=True), \
            patch("builtins.open", mock_open(read_data=b"image_content")):
            # Загружаем изображение
            result = await async_messenger_client.upload_image(
                user_id=12345,
                image_file="test_image.jpg"
            )

        # Проверяем результат
        assert result == {
            "test_image_id": {
                "140x105": "https://example.com/image_140_105.jpg",
                "32x32": "https://example.com/image_32_32.jpg"
            }
        }

        # Проверяем вызов метода запроса
        async_messenger_client._request_async.assert_called_once()

        # Проверяем, что запрос был выполнен с файлами
        call_args = async_messenger_client._request_async.call_args
        assert call_args[1]["method"] == "POST"
        assert call_args[1]["url"] == "/messenger/v1/accounts/12345/uploadImages"
        assert "files" in call_args[1]
        assert "multipart" in call_args[1] and call_args[1]["multipart"] is True

    @pytest.mark.asyncio
    async def test_get_messages(self, async_messenger_client):
        """Проверка асинхронного получения списка сообщений."""
        # Подменяем метод запроса
        async_messenger_client._request_async = MagicMock(return_value=[
            {
                "id": "test_message_id",
                "author_id": 12345,
                "content": {
                    "text": "Test message"
                },
                "created": 1600000100,
                "direction": "out",
                "is_read": True,
                "type": "text"
            }
        ])

        # Получаем сообщения
        messages = await async_messenger_client.get_messages(
            user_id=12345,
            chat_id="test_chat_id",
            limit=10,
            offset=5
        )

        # Проверяем результат
        assert isinstance(messages, Messages)
        assert len(messages.__root__) == 1
        assert messages.__root__[0].id == "test_message_id"
        assert messages.__root__[0].type == "text"
        assert messages.__root__[0].content.text == "Test message"

        # Проверяем вызов метода запроса
        async_messenger_client._request_async.assert_called_once_with(
            method="GET",
            url="/messenger/v3/accounts/12345/chats/test_chat_id/messages/",
            params={
                "limit": 10,
                "offset": 5,
            }
        )

    @pytest.mark.asyncio
    async def test_mark_chat_as_read(self, async_messenger_client):
        """Проверка асинхронной отметки чата как прочитанного."""
        # Подменяем метод запроса
        async_messenger_client._request_async = MagicMock(return_value={
            "ok": True
        })

        # Отмечаем чат как прочитанный
        result = await async_messenger_client.mark_chat_as_read(
            user_id=12345,
            chat_id="test_chat_id"
        )

        # Проверяем результат
        assert isinstance(result, SuccessResponse)
        assert result.ok is True

        # Проверяем вызов метода запроса
        async_messenger_client._request_async.assert_called_once_with(
            method="POST",
            url="/messenger/v1/accounts/12345/chats/test_chat_id/read",
        )

    @pytest.mark.asyncio
    async def test_subscribe_webhook(self, async_messenger_client):
        """Проверка асинхронной подписки на webhook-уведомления."""
        # Подменяем метод запроса
        async_messenger_client._request_async = MagicMock(return_value={
            "ok": True
        })

        # Подписываемся на webhook
        result = await async_messenger_client.subscribe_webhook(
            url="https://example.com/webhook"
        )

        # Проверяем результат
        assert isinstance(result, SuccessResponse)
        assert result.ok is True

        # Проверяем вызов метода запроса
        async_messenger_client._request_async.assert_called_once_with(
            method="POST",
            url="/messenger/v3/webhook",
            json_data={
                "url": "https://example.com/webhook"
            }
        )

    @pytest.mark.asyncio
    async def test_unsubscribe_webhook(self, async_messenger_client):
        """Проверка асинхронной отписки от webhook-уведомлений."""
        # Подменяем метод запроса
        async_messenger_client._request_async = MagicMock(return_value={
            "ok": True
        })

        # Отписываемся от webhook
        result = await async_messenger_client.unsubscribe_webhook(
            url="https://example.com/webhook"
        )

        # Проверяем результат
        assert isinstance(result, SuccessResponse)
        assert result.ok is True

        # Проверяем вызов метода запроса
        async_messenger_client._request_async.assert_called_once_with(
            method="POST",
            url="/messenger/v1/webhook/unsubscribe",
            json_data={
                "url": "https://example.com/webhook"
            }
        )


class TestMessengerModels:
    """Тесты для моделей данных модуля мессенджера."""

    def test_message_model(self):
        """Проверка модели сообщения."""
        # Тестовые данные
        data = {
            "id": "test_message_id",
            "author_id": 12345,
            "content": {
                "text": "Test message"
            },
            "created": 1600000000,
            "direction": "out",
            "type": "text",
            "is_read": True
        }

        # Создаем модель сообщения
        message = Message(**data)

        # Проверяем атрибуты
        assert message.id == "test_message_id"
        assert message.author_id == 12345
        assert message.content.text == "Test message"
        assert message.created == 1600000000
        assert message.direction == MessageDirection.OUT
        assert message.type == MessageType.TEXT
        assert message.is_read is True

    def test_chat_model(self):
        """Проверка модели чата."""
        # Тестовые данные
        data = {
            "id": "test_chat_id",
            "created": 1600000000,
            "updated": 1600000100,
            "users": [
                {
                    "id": 12345,
                    "name": "Test User"
                }
            ],
            "last_message": {
                "id": "test_message_id",
                "author_id": 12345,
                "content": {
                    "text": "Test message"
                },
                "created": 1600000100,
                "direction": "out",
                "type": "text"
            }
        }

        # Создаем модель чата
        chat = Chat(**data)

        # Проверяем атрибуты
        assert chat.id == "test_chat_id"
        assert chat.created == 1600000000
        assert chat.updated == 1600000100
        assert len(chat.users) == 1
        assert chat.users[0].id == 12345
        assert chat.users[0].name == "Test User"
        assert chat.last_message.id == "test_message_id"
        assert chat.last_message.author_id == 12345
        assert chat.last_message.content.text == "Test message"

    def test_blacklist_models(self):
        """Проверка моделей для черного списка."""
        # Создаем модель контекста
        context = BlacklistUserContext(
            item_id=54321,
            reason_id=BlacklistReasonId.SPAM
        )

        # Проверяем атрибуты
        assert context.item_id == 54321
        assert context.reason_id == BlacklistReasonId.SPAM

        # Создаем модель пользователя для черного списка
        user = BlacklistUser(
            user_id=67890,
            context=context
        )

        # Проверяем атрибуты
        assert user.user_id == 67890
        assert user.context == context
        assert message.content.text == "Test message"

        # Проверяем вызов метода запроса
        sync_messenger_client._request_sync.assert_called_once_with(
            method="POST",
            url="/messenger/v1/accounts/12345/chats/test_chat_id/messages",
            json_data={
                "type": "text",
                "message": {
                    "text": "Test message"
                }
            }
        )

    def test_upload_image_from_path(self, sync_messenger_client):
        """Проверка загрузки изображения из файла."""
        # Подменяем метод запроса
        sync_messenger_client._request_sync = MagicMock(return_value={
            "test_image_id": {
                "140x105": "https://example.com/image_140_105.jpg",
                "32x32": "https://example.com/image_32_32.jpg"
            }
        })

        # Подменяем open и os.path.isfile
        with patch("os.path.isfile", return_value=True), \
            patch("builtins.open", mock_open(read_data=b"image_content")):
            # Загружаем изображение
            result = sync_messenger_client.upload_image(
                user_id=12345,
                image_file="test_image.jpg"
            )

        # Проверяем результат
        assert result == {
            "test_image_id": {
                "140x105": "https://example.com/image_140_105.jpg",
                "32x32": "https://example.com/image_32_32.jpg"
            }
        }

        # Проверяем вызов метода запроса
        sync_messenger_client._request_sync.assert_called_once()

        # Проверяем, что запрос был выполнен с файлами
        call_args = sync_messenger_client._request_sync.call_args
        assert call_args[1]["method"] == "POST"
        assert call_args[1]["url"] == "/messenger/v1/accounts/12345/uploadImages"
        assert "files" in call_args[1]
        assert "multipart" in call_args[1] and call_args[1]["multipart"] is True

    def test_upload_image_from_bytes(self, sync_messenger_client):
        """Проверка загрузки изображения из байтов."""
        # Подменяем метод запроса
        sync_messenger_client._request_sync = MagicMock(return_value={
            "test_image_id": {
                "140x105": "https://example.com/image_140_105.jpg",
                "32x32": "https://example.com/image_32_32.jpg"
            }
        })

        # Загружаем изображение
        result = sync_messenger_client.upload_image(
            user_id=12345,
            image_file=b"image_content"
        )

        # Проверяем результат
        assert result == {
            "test_image_id": {
                "140x105": "https://example.com/image_140_105.jpg",
                "32x32": "https://example.com/image_32_32.jpg"
            }
        }

        # Проверяем вызов метода запроса
        sync_messenger_client._request_sync.assert_called_once()

        # Проверяем, что запрос был выполнен с файлами
        call_args = sync_messenger_client._request_sync.call_args
        assert call_args[1]["method"] == "POST"
        assert call_args[1]["url"] == "/messenger/v1/accounts/12345/uploadImages"
        assert "files" in call_args[1]
        assert call_args[1]["files"]["uploadfile[]"][1] == b"image_content"

    def test_send_image_message(self, sync_messenger_client):
        """Проверка отправки сообщения с изображением."""
        # Подменяем метод запроса
        sync_messenger_client._request_sync = MagicMock(return_value={
            "id": "new_message_id",
            "content": {
                "image": {
                    "sizes": {
                        "140x105": "https://example.com/image_140_105.jpg",
                        "32x32": "https://example.com/image_32_32.jpg"
                    }
                }
            },
            "created": 1600000300,
            "direction": "out",
            "type": "image",
            "author_id": 12345
        })

        # Отправляем сообщение с изображением
        message = sync_messenger_client.send_image_message(
            user_id=12345,
            chat_id="test_chat_id",
            image_id="test_image_id"
        )

        # Проверяем результат
        assert isinstance(message, Message)
        assert message.id == "new_message_id"
        assert message.type == "image"
        assert message.content.image.sizes["140x105"] == "https://example.com/image_140_105.jpg"

        # Проверяем вызов метода запроса
        sync_messenger_client._request_sync.assert_called_once_with(
            method="POST",
            url="/messenger/v1/accounts/12345/chats/test_chat_id/messages/image",
            json_data={
                "image_id": "test_image_id"
            }
        )

    def test_mark_chat_as_read(self, sync_messenger_client, mock_success_response):
        """Проверка отметки чата как прочитанного."""
        # Подменяем метод запроса
        sync_messenger_client._request_sync = MagicMock(return_value={
            "ok": True
        })

        # Отмечаем чат как прочитанный
        result = sync_messenger_client.mark_chat_as_read(
            user_id=12345,
            chat_id="test_chat_id"
        )

        # Проверяем результат
        assert isinstance(result, SuccessResponse)
        assert result.ok is True

        # Проверяем вызов метода запроса
        sync_messenger_client._request_sync.assert_called_once_with(
            method="POST",
            url="/messenger/v1/accounts/12345/chats/test_chat_id/read",
        )

    def test_delete_message(self, sync_messenger_client):
        """Проверка удаления сообщения."""
        # Подменяем метод запроса
        sync_messenger_client._request_sync = MagicMock(return_value={})

        # Удаляем сообщение
        result = sync_messenger_client.delete_message(
            user_id=12345,
            chat_id="test_chat_id",
            message_id="test_message_id"
        )

        # Проверяем результат
        assert result == {}

        # Проверяем вызов метода запроса
        sync_messenger_client._request_sync.assert_called_once_with(
            method="POST",
            url="/messenger/v1/accounts/12345/chats/test_chat_id/messages/test_message_id",
        )

    def test_add_to_blacklist(self, sync_messenger_client):
        """Проверка добавления пользователей в черный список."""
        # Подменяем метод запроса
        sync_messenger_client._request_sync = MagicMock(return_value={})

        # Создаем список пользователей для блокировки
        blacklist_users = [
            BlacklistUser(
                user_id=67890,
                context=BlacklistUserContext(
                    item_id=54321,
                    reason_id=BlacklistReasonId.SPAM
                )
            )
        ]

        # Добавляем пользователей в черный список
        result = sync_messenger_client.add_to_blacklist(
            user_id=12345,
            blacklist_users=blacklist_users
        )

        # Проверяем результат
        assert result == {}

        # Проверяем вызов метода запроса
        sync_messenger_client._request_sync.assert_called_once_with(
            method="POST",
            url="/messenger/v2/accounts/12345/blacklist",
            json_data={
                "users": [
                    {
                        "user_id": 67890,
                        "context": {
                            "item_id": 54321,
                            "reason_id": 1
                        }
                    }
                ]
            }
        )


class TestAsyncMessengerClient:
    """Тесты для асинхронного клиента мессенджера."""

    @pytest.mark.asyncio
    async def test_get_chats(self, async_messenger_client):
        """Проверка асинхронного получения списка чатов."""
        # Подменяем метод запроса
        async_messenger_client._request_async = MagicMock(return_value={
            "chats": [
                {
                    "id": "test_chat_id",
                    "created": 1600000000,
                    "updated": 1600000100,
                    "users": [
                        {
                            "id": 12345,
                            "name": "Test User"
                        }
                    ],
                    "last_message": {
                        "id": "test_message_id",
                        "author_id": 12345,
                        "content": {
                            "text": "Test message"
                        },
                        "created": 1600000100,
                        "direction": "out",
                        "type": "text"
                    }
                }
            ]
        })

        # Получаем чаты
        chats = await async_messenger_client.get_chats(
            user_id=12345,
            limit=10,
            unread_only=True,
            chat_types=[ChatType.USER_TO_ITEM]
        )

        # Проверяем результат
        assert isinstance(chats, Chats)
        assert len(chats.chats) == 1
        assert chats.chats[0].id == "test_chat_id"

        # Проверяем вызов метода запроса
        async_messenger_client._request_async.assert_called_once_with(
            method="GET",
            url="/messenger/v2/accounts/12345/chats",
            params={
                "unread_only": True,
                "limit": 10,
                "offset": 0,
                "chat_types": "u2i",
            }
        )

    @pytest.mark.asyncio
    async def test_send_message(self, async_messenger_client):
        """Проверка асинхронной отправки текстового сообщения."""
        # Подменяем метод запроса
        async_messenger_client._request_async = MagicMock(return_value={
            "id": "new_message_id",
            "content": {
                "text": "Test message"
            },
            "created": 1600000300,
            "direction": "out",
            "type": "text",
            "author_id": 12345
        })

        # Отправляем сообщение
        message = await async_messenger_client.send_message(
            user_id=12345,
            chat_id="test_chat_id",
            text="Test message"
        )

        # Проверяем результат
        assert isinstance(message, Message)
        assert message.id == "new_message_id"
        assert message.type == "text"
