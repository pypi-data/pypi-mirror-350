# Справочник API: Модуль мессенджера

Модуль `avito_api.messenger` предоставляет классы и модели для работы с API мессенджера Авито.

## Клиенты мессенджера

### BaseMessengerClient

```python
from avito_api.messenger import BaseMessengerClient
```

Базовый класс для работы с API мессенджера Авито. Предоставляет общие методы для валидации сообщений.

### SyncMessengerClient

```python
from avito_api.messenger import SyncMessengerClient
```

Синхронный клиент для работы с API мессенджера Авито.

#### Пример использования

```python
messenger_client = SyncMessengerClient(
    client_id="your_client_id",
    client_secret="your_client_secret"
)

# Получаем токен доступа
messenger_client.get_token()

# Работаем с мессенджером
user_id = 12345678
chats = messenger_client.get_chats(user_id=user_id, limit=10)
```

#### Основные методы

```python
def get_chats(
    self,
    user_id: int,
    item_ids: Optional[List[int]] = None,
    unread_only: bool = False,
    chat_types: Optional[List[Union[ChatType, str]]] = None,
    limit: int = 100,
    offset: int = 0,
) -> Chats:
    """
    Получает список чатов пользователя.

    Args:
        user_id: Идентификатор пользователя
        item_ids: Идентификаторы объявлений для фильтрации
        unread_only: Только непрочитанные чаты
        chat_types: Типы чатов для фильтрации
        limit: Максимальное количество чатов
        offset: Смещение в выборке

    Returns:
        Список чатов пользователя
    """

def get_chat(self, user_id: int, chat_id: str) -> Chat:
    """
    Получает информацию о конкретном чате.

    Args:
        user_id: Идентификатор пользователя
        chat_id: Идентификатор чата

    Returns:
        Информация о чате
    """

def get_messages(
    self,
    user_id: int,
    chat_id: str,
    limit: int = 100,
    offset: int = 0,
) -> Messages:
    """
    Получает список сообщений в чате.

    Args:
        user_id: Идентификатор пользователя
        chat_id: Идентификатор чата
        limit: Максимальное количество сообщений
        offset: Смещение в выборке

    Returns:
        Список сообщений в чате
    """

def send_message(
    self,
    user_id: int,
    chat_id: str,
    text: str,
) -> Message:
    """
    Отправляет текстовое сообщение в чат.

    Args:
        user_id: Идентификатор пользователя
        chat_id: Идентификатор чата
        text: Текст сообщения

    Returns:
        Информация об отправленном сообщении
    """

def upload_image(
    self,
    user_id: int,
    image_file: Union[str, bytes, BinaryIO],
) -> Dict[str, Dict[str, str]]:
    """
    Загружает изображение для последующей отправки в сообщении.

    Args:
        user_id: Идентификатор пользователя
        image_file: Путь к файлу, содержимое файла в байтах или открытый файловый объект

    Returns:
        Информация о загруженном изображении
    """

def send_image_message(
    self,
    user_id: int,
    chat_id: str,
    image_id: str,
) -> Message:
    """
    Отправляет сообщение с изображением в чат.

    Args:
        user_id: Идентификатор пользователя
        chat_id: Идентификатор чата
        image_id: Идентификатор загруженного изображения

    Returns:
        Информация об отправленном сообщении
    """

def mark_chat_as_read(self, user_id: int, chat_id: str) -> SuccessResponse:
    """
    Отмечает чат как прочитанный.

    Args:
        user_id: Идентификатор пользователя
        chat_id: Идентификатор чата

    Returns:
        Подтверждение успешного выполнения операции
    """

def delete_message(self, user_id: int, chat_id: str, message_id: str) -> Dict[str, Any]:
    """
    Удаляет сообщение из чата.

    Args:
        user_id: Идентификатор пользователя
        chat_id: Идентификатор чата
        message_id: Идентификатор сообщения

    Returns:
        Подтверждение успешного выполнения операции
    """

def get_voice_files(self, user_id: int, voice_ids: List[str]) -> VoiceFiles:
    """
    Получает ссылки на файлы голосовых сообщений.

    Args:
        user_id: Идентификатор пользователя
        voice_ids: Список идентификаторов голосовых сообщений

    Returns:
        Ссылки на файлы голосовых сообщений
    """

def subscribe_webhook(self, url: str) -> SuccessResponse:
    """
    Подписывается на webhook-уведомления.

    Args:
        url: URL для получения уведомлений

    Returns:
        Подтверждение успешной подписки
    """

def unsubscribe_webhook(self, url: str) -> SuccessResponse:
    """
    Отписывается от webhook-уведомлений.

    Args:
        url: URL, на который больше не нужно отправлять уведомления

    Returns:
        Подтверждение успешной отписки
    """

def get_webhook_subscriptions(self) -> WebhookSubscriptions:
    """
    Получает список подписок на webhook-уведомления.

    Returns:
        Список подписок на webhook-уведомления
    """

def add_to_blacklist(self, user_id: int, blacklist_users: List[BlacklistUser]) -> Dict[str, Any]:
    """
    Добавляет пользователей в черный список.

    Args:
        user_id: Идентификатор пользователя
        blacklist_users: Список пользователей для добавления в черный список

    Returns:
        Подтверждение успешного выполнения операции
    """
```

### AsyncMessengerClient

```python
from avito_api.messenger import AsyncMessengerClient
```

Асинхронный клиент для работы с API мессенджера Авито.

#### Пример использования

```python
import asyncio

async def main():
    messenger_client = AsyncMessengerClient(
        client_id="your_client_id",
        client_secret="your_client_secret"
    )

    # Получаем токен доступа
    await messenger_client.get_token_async()

    # Работаем с мессенджером
    user_id = 12345678
    chats = await messenger_client.get_chats(user_id=user_id, limit=10)

    print(f"Получено {len(chats.chats)} чатов")

asyncio.run(main())
```

Класс `AsyncMessengerClient` предоставляет те же методы, что и `SyncMessengerClient`, но в асинхронной форме. Все методы начинаются с `async def` и должны вызываться с `await`.

## Enum-типы данных

### ChatType

```python
from avito_api.messenger import ChatType
```

Enum-класс для типов чатов.

```python
class ChatType(str, Enum):
    """Типы чатов."""

    USER_TO_ITEM = "u2i"  # Чаты по объявлениям
    USER_TO_USER = "u2u"  # Чаты между пользователями
```

### MessageType

```python
from avito_api.messenger import MessageType
```

Enum-класс для типов сообщений.

```python
class MessageType(str, Enum):
    """Типы сообщений."""

    TEXT = "text"
    IMAGE = "image"
    LINK = "link"
    ITEM = "item"
    LOCATION = "location"
    CALL = "call"
    DELETED = "deleted"
    VOICE = "voice"
    SYSTEM = "system"
    APP_CALL = "appCall"
    FILE = "file"
    VIDEO = "video"
```

### MessageDirection

```python
from avito_api.messenger import MessageDirection
```

Enum-класс для направлений сообщений.

```python
class MessageDirection(str, Enum):
    """Направления сообщений."""

    IN = "in"   # Входящие
    OUT = "out"  # Исходящие
```

### BlacklistReasonId

```python
from avito_api.messenger import BlacklistReasonId
```

Enum-класс для причин добавления пользователей в черный список.

```python
class BlacklistReasonId(int, Enum):
    """Причины добавления пользователя в черный список."""

    SPAM = 1
    FRAUD = 2
    INSULT = 3
    OTHER = 4
```

## Модели данных

### Модели запросов

```python
from avito_api.messenger import (
    SendMessageRequest, SendImageMessageRequest, WebhookSubscribeRequest,
    BlacklistUserContext, BlacklistUser, AddBlacklistRequest
)
```

Модели для отправки запросов к API мессенджера.

### Модели содержимого сообщений

```python
from avito_api.messenger import (
    CallContent, ImageContent, ItemContent, LinkPreview, LinkContent,
    LocationContent, VoiceContent, MessageContent
)
```

Модели для различных типов содержимого сообщений.

### Модели сообщений и чатов

```python
from avito_api.messenger import (
    MessageQuote, Message, Messages, UserAvatar, UserProfile, User,
    ItemContext, ChatContext, LastMessage, Chat, Chats
)
```

Модели для сообщений и чатов.

### Модели для webhooks

```python
from avito_api.messenger import (
    WebhookMessage, WebhookSubscription, WebhookSubscriptions
)
```

Модели для работы с webhook-уведомлениями.

### Прочие модели

```python
from avito_api.messenger import (
    VoiceFiles, SuccessResponse
)
```

Дополнительные модели для работы с API мессенджера.

## Примеры использования

### Работа с чатами

```python
from avito_api.messenger import SyncMessengerClient, ChatType

messenger_client = SyncMessengerClient(
    client_id="your_client_id",
    client_secret="your_client_secret"
)

# Получаем токен
messenger_client.get_token()

user_id = 12345678

# Получаем чаты по объявлениям
chats = messenger_client.get_chats(
    user_id=user_id,
    chat_types=[ChatType.USER_TO_ITEM],
    limit=5
)

# Получаем чаты между пользователями
user_chats = messenger_client.get_chats(
    user_id=user_id,
    chat_types=[ChatType.USER_TO_USER],
    limit=5
)

# Получаем все непрочитанные чаты
unread_chats = messenger_client.get_chats(
    user_id=user_id,
    unread_only=True
)

# Получаем чаты по конкретным объявлениям
item_chats = messenger_client.get_chats(
    user_id=user_id,
    item_ids=[1234567, 7654321]
)
```

### Отправка сообщений

```python
from avito_api.messenger import SyncMessengerClient

messenger_client = SyncMessengerClient(
    client_id="your_client_id",
    client_secret="your_client_secret"
)

# Получаем токен
messenger_client.get_token()

user_id = 12345678
chat_id = "abcdef1234567890"

# Отправляем текстовое сообщение
message = messenger_client.send_message(
    user_id=user_id,
    chat_id=chat_id,
    text="Привет! Это тестовое сообщение от API."
)

print(f"Сообщение отправлено, ID: {message.id}")

# Загружаем изображение
with open("image.jpg", "rb") as f:
    image_data = f.read()

image_upload = messenger_client.upload_image(
    user_id=user_id,
    image_file=image_data
)

image_id = list(image_upload.keys())[0]

# Отправляем сообщение с изображением
image_message = messenger_client.send_image_message(
    user_id=user_id,
    chat_id=chat_id,
    image_id=image_id
)

print(f"Сообщение с изображением отправлено, ID: {image_message.id}")
```

### Асинхронная работа с мессенджером

```python
import asyncio
from avito_api.messenger import AsyncMessengerClient

async def main():
    messenger_client = AsyncMessengerClient(
        client_id="your_client_id",
        client_secret="your_client_secret"
    )

    # Получаем токен
    await messenger_client.get_token_async()

    user_id = 12345678

    # Получаем чаты и сообщения параллельно
    chats = await messenger_client.get_chats(user_id=user_id, limit=5)

    if not chats.chats:
        print("Нет доступных чатов")
        return

    # Получаем сообщения из всех чатов параллельно
    chat_ids = [chat.id for chat in chats.chats]

    tasks = [
        messenger_client.get_messages(user_id=user_id, chat_id=chat_id, limit=10)
        for chat_id in chat_ids
    ]

    messages_results = await asyncio.gather(*tasks)

    # Обрабатываем результаты
    for i, messages in enumerate(messages_results):
        print(f"Чат {i+1}: получено {len(messages.__root__)} сообщений")

asyncio.run(main())
```

### Работа с webhook-уведомлениями

```python
from avito_api.messenger import SyncMessengerClient, WebhookMessage

messenger_client = SyncMessengerClient(
    client_id="your_client_id",
    client_secret="your_client_secret"
)

# Получаем токен
messenger_client.get_token()

# Подписываемся на webhook-уведомления
result = messenger_client.subscribe_webhook(url="https://your-site.com/webhook")
print(f"Подписка на webhook: {result.ok}")

# Получаем список подписок
subscriptions = messenger_client.get_webhook_subscriptions()
print(f"Всего подписок: {len(subscriptions.subscriptions)}")

for subscription in subscriptions.subscriptions:
    print(f"URL: {subscription.url}, версия: {subscription.version}")

# Пример обработки webhook-уведомления на вашем сервере
def webhook_handler(request_data):
    message = WebhookMessage(**request_data)

    print(f"Получено сообщение от {message.author_id} в чате {message.chat_id}")

    if message.type == "text":
        print(f"Текст: {message.content.text}")
    elif message.type == "image":
        print(f"Изображение")
```
