# Авторизация

API Авито предоставляет два способа авторизации, которые поддерживаются в нашей библиотеке:

1. **Client Credentials** - для работы от своего имени
2. **OAuth 2.0 с authorization_code** - для работы от имени пользователя

## Client Credentials

Этот тип авторизации используется для доступа к API от своего имени. Для него требуются только Client ID и Client Secret.

### Получение Client ID и Client Secret

1. Зарегистрируйтесь в [личном кабинете Авито](https://www.avito.ru/professionals/api)
2. Получите Client ID и Client Secret

### Пример использования

```python
from avito_api.auth import SyncAuthClient

auth_client = SyncAuthClient(
    client_id="your_client_id",
    client_secret="your_client_secret"
)

# Получение токена доступа
token_info = auth_client.get_token()

print(f"Токен: {token_info.access_token}")
print(f"Истекает через {token_info.expires_in} секунд")
print(f"Тип токена: {token_info.token_type}")
```

Токен доступа действителен в течение 24 часов. Библиотека автоматически обновит токен при выполнении запросов, если он истек.

### Ручное управление токенами

```python
from avito_api.client import SyncApiClient

client = SyncApiClient(
    client_id="your_client_id",
    client_secret="your_client_secret"
)

# Получаем токен
token_info = client.get_token()

# Сохраняем токен для последующего использования
access_token = token_info["access_token"]
token_expires_at = token_info["expires_in"]

# Позже можно создать клиент с сохраненным токеном
client = SyncApiClient(
    client_id="your_client_id",
    client_secret="your_client_secret",
    access_token=access_token,
    token_expires_at=token_expires_at
)
```

## OAuth 2.0 с authorization_code

Этот тип авторизации используется для доступа к API от имени пользователя Авито. Он требует регистрации приложения на [https://developers.avito.ru/applications](https://developers.avito.ru/applications).

### Шаги для работы с OAuth 2.0

1. **Регистрация приложения**:
   - Зарегистрируйте приложение на [https://developers.avito.ru/applications](https://developers.avito.ru/applications)
   - Укажите Redirect URI для получения кода авторизации
   - Выберите необходимые скоупы (права доступа)

2. **Получение кода авторизации**:
   - Сформируйте URL для авторизации пользователя
   - Пользователь авторизуется и подтверждает доступ
   - Авито перенаправляет пользователя на ваш Redirect URI с кодом авторизации

3. **Обмен кода на токен доступа**:
   - Обменяйте код авторизации на токен доступа и refresh-токен
   - Используйте токен доступа для запросов к API
   - Обновляйте токен доступа с помощью refresh-токена при истечении срока действия

### Пример использования OAuth 2.0

```python
from avito_api.auth import SyncAuthClient, Scope

# Создаем клиент авторизации
auth_client = SyncAuthClient(
    client_id="your_client_id",
    client_secret="your_client_secret"
)

# Шаг 1: Формируем URL для авторизации пользователя
auth_url = auth_client.get_authorization_url(
    client_id="your_client_id",
    scopes=[
        Scope.MESSENGER_READ,
        Scope.MESSENGER_WRITE,
        Scope.USER_READ
    ],
    state="random_state_string",  # Защита от CSRF-атак
    redirect_uri="https://your-app.com/callback"
)

print(f"Перенаправьте пользователя на URL: {auth_url}")

# Шаг 2: Получаем код авторизации после редиректа
# (код получен после того, как пользователь подтвердил доступ и был перенаправлен на ваш redirect_uri)
code = "authorization_code_from_callback"

# Шаг 3: Обмениваем код на токен доступа
token_response = auth_client.get_token_by_authorization_code(code)

access_token = token_response.access_token
refresh_token = token_response.refresh_token
expires_in = token_response.expires_in

print(f"Получен токен доступа: {access_token}")
print(f"Получен refresh-токен: {refresh_token}")
print(f"Токен истекает через {expires_in} секунд")
```

### Обновление токена доступа

```python
from avito_api.auth import SyncAuthClient

auth_client = SyncAuthClient(
    client_id="your_client_id",
    client_secret="your_client_secret",
    refresh_token="your_refresh_token"
)

# Обновляем токен доступа
token_response = auth_client.refresh_access_token()

new_access_token = token_response.access_token
new_refresh_token = token_response.refresh_token  # Также обновляется refresh-токен
expires_in = token_response.expires_in

print(f"Новый токен доступа: {new_access_token}")
print(f"Новый refresh-токен: {new_refresh_token}")
print(f"Токен истекает через {expires_in} секунд")
```

### Автоматическое обновление токенов

Библиотека поддерживает автоматическое обновление токенов при истечении срока действия. Для этого достаточно создать клиент с refresh-токеном:

```python
from avito_api.messenger import SyncMessengerClient
from avito_api.config import ClientConfig, ApiConfig

# Настройка автоматического обновления токенов
config = ClientConfig(
    api=ApiConfig(
        auto_refresh_token=True,
        token_refresh_threshold=300  # Обновлять токен, если до истечения осталось менее 300 секунд
    )
)

# Создаем клиент с refresh-токеном
client = SyncMessengerClient(
    client_id="your_client_id",
    client_secret="your_client_secret",
    access_token="your_access_token",
    refresh_token="your_refresh_token",
    token_expires_at=1678901234,  # Unix timestamp окончания действия токена
    config=config
)

# При выполнении запросов токен будет автоматически обновлен, если истекает
```

## Доступные скоупы OAuth 2.0

Библиотека предоставляет enum `Scope` со всеми доступными скоупами:

```python
from avito_api.auth import Scope

# Примеры доступных скоупов
print(Scope.MESSENGER_READ)    # messenger:read
print(Scope.MESSENGER_WRITE)   # messenger:write
print(Scope.USER_READ)         # user:read
print(Scope.USER_BALANCE_READ) # user_balance:read
# и другие
```

Полный список доступных скоупов:

| Скоуп | Описание |
|-------|----------|
| `MESSENGER_READ` | Чтение сообщений в мессенджере Авито |
| `MESSENGER_WRITE` | Модифицирование сообщений в мессенджере Авито |
| `USER_BALANCE_READ` | Получение баланса пользователя |
| `JOB_WRITE` | Изменение объявлений вертикали Работа |
| `JOB_CV` | Получение информации резюме |
| `JOB_VACANCY` | Работа с вакансиями |
| `JOB_APPLICATIONS` | Получение информации об откликах на вакансии |
| `USER_OPERATIONS_READ` | Получение истории операций пользователя |
| `USER_READ` | Получение информации о пользователе |
| `AUTOLOAD_REPORTS` | Получение отчетов Автозагрузки |
| `ITEMS_INFO` | Получение информации об объявлениях |
| `ITEMS_APPLY_VAS` | Применение дополнительных услуг |
| `SHORT_TERM_RENT_READ` | Получение информации об объявлениях краткосрочной аренды |
| `SHORT_TERM_RENT_WRITE` | Изменение объявлений краткосрочной аренды |
| `STATS_READ` | Получение статистики объявлений |

## Асинхронная авторизация

Для асинхронной работы с авторизацией используйте класс `AsyncAuthClient`:

```python
import asyncio
from avito_api.auth import AsyncAuthClient

async def main():
    auth_client = AsyncAuthClient(
        client_id="your_client_id",
        client_secret="your_client_secret"
    )

    # Получение токена доступа
    token_info = await auth_client.get_token_async()

    print(f"Токен: {token_info.access_token}")

    # Использование OAuth 2.0
    code = "authorization_code_from_callback"
    token_response = await auth_client.get_token_by_authorization_code(code)

    print(f"OAuth токен: {token_response.access_token}")
    print(f"OAuth refresh-токен: {token_response.refresh_token}")

# Запуск асинхронной функции
asyncio.run(main())
```
