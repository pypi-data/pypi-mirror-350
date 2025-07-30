# Avito API Client

Библиотека для работы с API Авито. Поддерживает синхронные и асинхронные запросы, автоматическое обновление токенов и настраиваемое логирование.

## Установка

```bash
pip install avito-api
```

## Быстрый старт

```python
from avito_api.messenger import SyncMessengerClient

# Создаем клиент
client = SyncMessengerClient(
    client_id="your_client_id",
    client_secret="your_client_secret",
)

# Получаем токен
client.get_token()

# Работаем с API
# ...
```

## Документация

Подробная документация: [docs/index.md](docs/index.md)

## Лицензия

MIT
