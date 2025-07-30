"""
Библиотека для работы с API Авито.

Поддерживает синхронные и асинхронные запросы к API,
автоматическое обновление токенов и логирование через loguru.

Примеры использования:

Синхронный клиент:
```python
import os
from avito_api import SyncApiClient
from avito_api.auth import SyncAuthClient
from avito_api.messenger import SyncMessengerClient

# Создаем клиент
client = SyncMessengerClient(
    client_id=os.environ.get("AVITO_CLIENT_ID"),
    client_secret=os.environ.get("AVITO_CLIENT_SECRET"),
)

# Получаем токен
client.get_current_token()

# Получаем список чатов
user_id = 123456
chats = client.get_chats(user_id=user_id, limit=10)

# Получаем сообщения из первого чата
if chats.chats:
    chat_id = chats.chats[0].id
    messages = client.get_messages(user_id=user_id, chat_id=chat_id, limit=20)

    # Отправляем сообщение
    response = client.send_message(
        user_id=user_id,
        chat_id=chat_id,
        text="Привет, это тестовое сообщение!",
    )
```

Асинхронный клиент:
```python
import os
import asyncio
from avito_api import AsyncApiClient
from avito_api.auth import AsyncAuthClient
from avito_api.messenger import AsyncMessengerClient

async def main():
    # Создаем асинхронный клиент
    client = AsyncMessengerClient(
        client_id=os.environ.get("AVITO_CLIENT_ID"),
        client_secret=os.environ.get("AVITO_CLIENT_SECRET"),
    )

    # Получаем токен
    await client.get_current_token_async()

    # Получаем список чатов
    user_id = 123456
    chats = await client.get_chats(user_id=user_id, limit=10)

    # Получаем сообщения из первого чата
    if chats.chats:
        chat_id = chats.chats[0].id
        messages = await client.get_messages(user_id=user_id, chat_id=chat_id, limit=20)

        # Отправляем сообщение
        response = await client.send_message(
            user_id=user_id,
            chat_id=chat_id,
            text="Привет, это тестовое сообщение!",
        )

# Запускаем асинхронную функцию
asyncio.run(main())
```
"""
__version__ = "0.4.3"

from .client import BaseApiClient, SyncApiClient, AsyncApiClient
from .config import ClientConfig, LogConfig, ApiConfig, logger
from .exceptions import (
    AvitoApiError, AuthError, TokenExpiredError, ForbiddenError,
    NotFoundError, ValidationError, RateLimitError, ServerError,
    NetworkError, ConfigError
)

__all__ = [
    "BaseApiClient", "SyncApiClient", "AsyncApiClient",
    "ClientConfig", "LogConfig", "ApiConfig", "logger",
    "AvitoApiError", "AuthError", "TokenExpiredError", "ForbiddenError",
    "NotFoundError", "ValidationError", "RateLimitError", "ServerError",
    "NetworkError", "ConfigError",
]
