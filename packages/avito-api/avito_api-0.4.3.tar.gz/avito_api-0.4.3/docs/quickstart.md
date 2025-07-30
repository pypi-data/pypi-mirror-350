# Быстрый старт

В этом разделе вы узнаете, как начать использовать библиотеку Avito API Client для взаимодействия с API Авито.

## Подготовка к работе

Перед началом работы вам необходимы:

1. Client ID и Client Secret, полученные в [личном кабинете Авито](https://www.avito.ru/professionals/api)
2. Установленная библиотека `avito-api` (см. [Установка](installation.md))

## Синхронное использование

### 1. Создание клиента и получение токена

```python
import os
from avito_api.messenger import SyncMessengerClient

# Создаем клиент
client = SyncMessengerClient(
    client_id=os.environ.get("AVITO_CLIENT_ID", "your_client_id"),
    client_secret=os.environ.get("AVITO_CLIENT_SECRET", "your_client_secret")
)

# Получаем токен доступа
client.get_token()
```

### 2. Получение списка чатов

```python
# ID пользователя Авито
user_id = 12345678

# Получаем список чатов
chats = client.get_chats(
    user_id=user_id,
    limit=10,
    unread_only=True
)

print(f"Получено {len(chats.chats)} чатов")
```

### 3. Работа с сообщениями

```python
# Если есть чаты, работаем с первым
if chats.chats:
    chat = chats.chats[0]
    chat_id = chat.id

    # Получаем сообщения из чата
    messages = client.get_messages(
        user_id=user_id,
        chat_id=chat_id,
        limit=20
    )

    print(f"Получено {len(messages.__root__)} сообщений")

    # Отправляем новое сообщение
    response = client.send_message(
        user_id=user_id,
        chat_id=chat_id,
        text="Привет! Это тестовое сообщение от API."
    )

    print(f"Сообщение успешно отправлено, ID: {response.id}")

    # Отмечаем чат как прочитанный
    client.mark_chat_as_read(
        user_id=user_id,
        chat_id=chat_id
    )
```

### 4. Отправка изображений

```python
# Загружаем изображение
image_upload = client.upload_image(
    user_id=user_id,
    image_file="путь/к/изображению.jpg"
)

# Получаем ID загруженного изображения
image_id = list(image_upload.keys())[0]

# Отправляем сообщение с изображением
response = client.send_image_message(
    user_id=user_id,
    chat_id=chat_id,
    image_id=image_id
)

print(f"Сообщение с изображением отправлено, ID: {response.id}")
```

## Асинхронное использование

### 1. Создание асинхронного клиента

```python
import asyncio
import os
from avito_api.messenger import AsyncMessengerClient

async def main():
    # Создаем асинхронный клиент
    client = AsyncMessengerClient(
        client_id=os.environ.get("AVITO_CLIENT_ID", "your_client_id"),
        client_secret=os.environ.get("AVITO_CLIENT_SECRET", "your_client_secret")
    )

    # Получаем токен доступа
    await client.get_token_async()

    # Дальнейшие операции...

# Запускаем асинхронную функцию
asyncio.run(main())
```

### 2. Параллельное получение сообщений из нескольких чатов

```python
async def main():
    # ... (создание клиента и получение токена)

    # ID пользователя Авито
    user_id = 12345678

    # Получаем список чатов
    chats = await client.get_chats(user_id=user_id, limit=5)

    if not chats.chats:
        print("Нет доступных чатов")
        return

    # Получаем сообщения из всех чатов параллельно
    tasks = []
    for chat in chats.chats:
        task = client.get_messages(
            user_id=user_id,
            chat_id=chat.id,
            limit=10
        )
        tasks.append(task)

    # Ждем выполнения всех запросов
    all_messages = await asyncio.gather(*tasks)

    # Обрабатываем результаты
    for i, messages in enumerate(all_messages):
        print(f"Чат {i+1}: получено {len(messages.__root__)} сообщений")
```

## Настройка логирования

```python
from avito_api.config import ClientConfig, LogConfig
from avito_api.messenger import SyncMessengerClient

# Настраиваем конфигурацию
config = ClientConfig(
    logging=LogConfig(
        level="DEBUG",
        sink="avito_api.log",
        rotation="20 MB",
        retention="1 week"
    )
)

# Создаем клиент с настроенной конфигурацией
client = SyncMessengerClient(
    client_id="your_client_id",
    client_secret="your_client_secret",
    config=config
)
```

## Что дальше?

- Подробнее об авторизации и работе с токенами: [Авторизация](authentication.md)
- Подробнее о работе с мессенджером: [Мессенджер](messenger.md)
- Полный справочник API: [Справочник API](api_reference/client.md)
