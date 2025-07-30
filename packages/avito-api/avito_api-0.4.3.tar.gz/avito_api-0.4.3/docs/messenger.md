# Работа с мессенджером Авито

API мессенджера Авито позволяет получать список чатов пользователя, читать и отправлять сообщения, работать с изображениями и настраивать webhook-уведомления.

## Создание клиента мессенджера

### Синхронный клиент

```python
from avito_api.messenger import SyncMessengerClient

messenger = SyncMessengerClient(
    client_id="your_client_id",
    client_secret="your_client_secret"
)

# Получаем токен доступа
messenger.get_token()
```

### Асинхронный клиент

```python
import asyncio
from avito_api.messenger import AsyncMessengerClient

async def main():
    messenger = AsyncMessengerClient(
        client_id="your_client_id",
        client_secret="your_client_secret"
    )

    # Получаем токен доступа
    await messenger.get_token_async()

    # ...дальнейшая работа с мессенджером...

asyncio.run(main())
```

## Работа с чатами

### Получение списка чатов

```python
user_id = 12345678  # ID пользователя Авито

# Получаем список чатов
chats = messenger.get_chats(
    user_id=user_id,
    limit=10,            # Не более 100
    offset=0,            # Для пагинации
    unread_only=False,   # Только непрочитанные
    chat_types=["u2i"],  # u2i - чаты по объявлениям, u2u - между пользователями
    item_ids=[1234567, 7654321]  # Фильтр по ID объявлений
)

print(f"Получено {len(chats.chats)} чатов")

# Получение конкретного чата по ID
chat_id = "abcdef1234567890"
chat = messenger.get_chat(user_id=user_id, chat_id=chat_id)
```

### Отметка чата как прочитанного

```python
result = messenger.mark_chat_as_read(user_id=user_id, chat_id=chat_id)
print(f"Чат отмечен как прочитанный: {result.ok}")
```

## Работа с сообщениями

### Получение сообщений из чата

```python
messages = messenger.get_messages(
    user_id=user_id,
    chat_id=chat_id,
    limit=20,    # Не более 100
    offset=0     # Для пагинации
)

print(f"Получено {len(messages.__root__)} сообщений")

# Для каждого сообщения можно получить информацию
for message in messages.__root__:
    print(f"ID: {message.id}")
    print(f"Автор: {message.author_id}")
    print(f"Создано: {message.created}")
    print(f"Тип: {message.type}")

    # Содержимое зависит от типа сообщения
    if message.type == "text":
        print(f"Текст: {message.content.text}")
    elif message.type == "image":
        print(f"Изображение: {message.content.image.sizes}")
```

### Отправка текстового сообщения

```python
message = messenger.send_message(
    user_id=user_id,
    chat_id=chat_id,
    text="Привет! Это тестовое сообщение от API."
)

print(f"Сообщение успешно отправлено, ID: {message.id}")
```

### Работа с изображениями

#### Загрузка изображения

```python
# Загрузка из файла на диске
image_upload = messenger.upload_image(
    user_id=user_id,
    image_file="path/to/image.jpg"
)

# Или загрузка из байтов
with open("path/to/image.jpg", "rb") as f:
    image_bytes = f.read()

image_upload = messenger.upload_image(
    user_id=user_id,
    image_file=image_bytes
)

# Получаем ID загруженного изображения
image_id = list(image_upload.keys())[0]
print(f"Изображение загружено, ID: {image_id}")
```

#### Отправка сообщения с изображением

```python
message = messenger.send_image_message(
    user_id=user_id,
    chat_id=chat_id,
    image_id=image_id
)

print(f"Сообщение с изображением отправлено, ID: {message.id}")
```

### Удаление сообщения

```python
messenger.delete_message(
    user_id=user_id,
    chat_id=chat_id,
    message_id=message.id
)

print("Сообщение удалено")
```

## Работа с голосовыми сообщениями

### Получение ссылок на голосовые сообщения

```python
voice_ids = ["voice1", "voice2"]  # ID голосовых сообщений из content.voice.voice_id

voice_files = messenger.get_voice_files(
    user_id=user_id,
    voice_ids=voice_ids
)

# Получаем ссылки на голосовые сообщения
for voice_id, url in voice_files.voices_urls.items():
    print(f"Голосовое сообщение {voice_id}: {url}")
```

## Работа с webhook-уведомлениями

Webhook-уведомления позволяют получать информацию о новых сообщениях в реальном времени.

### Подписка на webhook-уведомления

```python
result = messenger.subscribe_webhook(url="https://your-webhook-url.com/avito-webhook")
print(f"Подписка на webhook успешна: {result.ok}")
```

### Получение списка подписок

```python
subscriptions = messenger.get_webhook_subscriptions()
print(f"Всего подписок: {len(subscriptions.subscriptions)}")

for subscription in subscriptions.subscriptions:
    print(f"URL: {subscription.url}, версия: {subscription.version}")
```

### Отписка от webhook-уведомлений

```python
result = messenger.unsubscribe_webhook(url="https://your-webhook-url.com/avito-webhook")
print(f"Отписка от webhook успешна: {result.ok}")
```

### Формат уведомлений webhook

Когда приходит новое сообщение, Авито отправляет POST-запрос на ваш webhook URL с данными в формате JSON. Эти данные соответствуют модели `WebhookMessage`:

```json
{
  "author_id": 123456,
  "chat_id": "abcdef1234567890",
  "chat_type": "u2i",
  "content": {
    "text": "Привет! Это тестовое сообщение."
  },
  "created": 1678901234,
  "id": "msg123456789",
  "item_id": 987654321,
  "type": "text",
  "user_id": 345678
}
```

В библиотеке это соответствует модели:

```python
from avito_api.messenger import WebhookMessage

# В вашем webhook-обработчике:
def webhook_handler(request_data):
    # Парсим данные в модель
    message = WebhookMessage(**request_data)

    print(f"Получено сообщение от {message.author_id} в чате {message.chat_id}")

    if message.type == "text":
        print(f"Текст: {message.content.text}")
    # и т.д.
```

## Черный список пользователей

### Добавление пользователей в черный список

```python
from avito_api.messenger import BlacklistUser, BlacklistUserContext, BlacklistReasonId

# Создаем список пользователей для блокировки
blacklist_users = [
    BlacklistUser(
        user_id=12345,
        context=BlacklistUserContext(
            item_id=67890,
            reason_id=BlacklistReasonId.SPAM  # 1 - спам, 2 - мошенничество, 3 - оскорбления, 4 - другая причина
        )
    ),
    BlacklistUser(
        user_id=23456,
        context=BlacklistUserContext(
            item_id=78901,
            reason_id=BlacklistReasonId.FRAUD
        )
    )
]

# Добавляем пользователей в черный список
result = messenger.add_to_blacklist(
    user_id=user_id,
    blacklist_users=blacklist_users
)

print("Пользователи добавлены в черный список")
```

## Работа с типами данных

Библиотека предоставляет несколько Enum-классов для удобства работы с типизированными данными:

```python
from avito_api.messenger import ChatType, MessageType, MessageDirection, BlacklistReasonId

# Типы чатов
print(ChatType.USER_TO_ITEM)  # u2i - чаты по объявлениям
print(ChatType.USER_TO_USER)  # u2u - чаты между пользователями

# Типы сообщений
print(MessageType.TEXT)    # text
print(MessageType.IMAGE)   # image
print(MessageType.LINK)    # link
print(MessageType.ITEM)    # item
print(MessageType.VOICE)   # voice
# и другие

# Направления сообщений
print(MessageDirection.IN)   # in - входящие
print(MessageDirection.OUT)  # out - исходящие

# Причины добавления в черный список
print(BlacklistReasonId.SPAM)    # 1
print(BlacklistReasonId.FRAUD)   # 2
print(BlacklistReasonId.INSULT)  # 3
print(BlacklistReasonId.OTHER)   # 4
```

## Асинхронное использование

Все методы, описанные выше, имеют асинхронные аналоги в классе `AsyncMessengerClient`:

```python
import asyncio
from avito_api.messenger import AsyncMessengerClient

async def main():
    messenger = AsyncMessengerClient(
        client_id="your_client_id",
        client_secret="your_client_secret"
    )

    # Получаем токен доступа
    await messenger.get_token_async()

    user_id = 12345678

    # Получаем список чатов
    chats = await messenger.get_chats(user_id=user_id, limit=10)

    if not chats.chats:
        print("Нет доступных чатов")
        return

    chat_id = chats.chats[0].id

    # Отправляем сообщение
    message = await messenger.send_message(
        user_id=user_id,
        chat_id=chat_id,
        text="Привет! Это асинхронное сообщение."
    )

    print(f"Сообщение отправлено, ID: {message.id}")

    # Параллельное выполнение запросов
    chat_tasks = [
        messenger.get_chat(user_id=user_id, chat_id=chat.id)
        for chat in chats.chats[:3]  # Берем первые 3 чата
    ]

    chat_results = await asyncio.gather(*chat_tasks)

    for i, chat in enumerate(chat_results):
        print(f"Чат {i+1}: {chat.id}")

# Запускаем асинхронную функцию
asyncio.run(main())
```

## Обработка ошибок

При работе с API могут возникать различные ошибки. Библиотека перехватывает эти ошибки и генерирует соответствующие исключения:

```python
from avito_api.exceptions import (
    AvitoApiError, AuthError, ForbiddenError,
    NotFoundError, ValidationError, RateLimitError
)

try:
    chats = messenger.get_chats(user_id=user_id)
except AuthError as e:
    print(f"Ошибка авторизации: {str(e)}")
except ForbiddenError as e:
    print(f"Доступ запрещен: {str(e)}")
except NotFoundError as e:
    print(f"Ресурс не найден: {str(e)}")
except ValidationError as e:
    print(f"Ошибка валидации данных: {str(e)}")
    if e.errors:
        print(f"Детали: {e.errors}")
except RateLimitError as e:
    print(f"Превышен лимит запросов: {str(e)}")
except AvitoApiError as e:
    print(f"Другая ошибка API: {str(e)}")
```

## Расширенная настройка

Для более тонкой настройки работы с API можно использовать конфигурацию:

```python
from avito_api.config import ClientConfig, ApiConfig, LogConfig
from avito_api.messenger import SyncMessengerClient

# Создаем конфигурацию
config = ClientConfig(
    api=ApiConfig(
        base_url="https://api.avito.ru",
        timeout=30.0,
        max_retries=3,
        retry_delay=1.0,
        auto_refresh_token=True,
        token_refresh_threshold=300
    ),
    logging=LogConfig(
        level="DEBUG",
        sink="avito_api.log",
        rotation="20 MB",
        retention="1 week",
        enqueue=True,
        diagnose=True
    )
)

# Создаем клиент с настроенной конфигурацией
messenger = SyncMessengerClient(
    client_id="your_client_id",
    client_secret="your_client_secret",
    config=config
)
```
