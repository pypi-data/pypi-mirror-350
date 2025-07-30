# Справочник API: Модуль авторизации

Модуль `avito_api.auth` предоставляет классы и модели для работы с авторизацией API Авито.

## Клиенты авторизации

### AuthClient

```python
from avito_api.auth import AuthClient
```

Базовый класс для работы с API авторизации Авито. Предоставляет общие методы для формирования URL авторизации.

#### Методы

```python
def get_authorization_url(
    self,
    client_id: str,
    scopes: List[Union[Scope, str]],
    state: Optional[str] = None,
    redirect_uri: Optional[str] = None,
) -> str:
    """
    Формирует URL для OAuth2 авторизации.

    Args:
        client_id: Идентификатор клиента
        scopes: Список запрашиваемых разрешений
        state: Произвольная строка для защиты от CSRF-атак
        redirect_uri: URL для перенаправления после авторизации

    Returns:
        URL для авторизации
    """
```

### SyncAuthClient

```python
from avito_api.auth import SyncAuthClient
```

Синхронный клиент для работы с API авторизации Авито.

#### Пример использования

```python
auth_client = SyncAuthClient(
    client_id="your_client_id",
    client_secret="your_client_secret"
)

# Получение токена доступа через client_credentials
token_info = auth_client.get_token()

# Получение токена доступа через код авторизации
code = "authorization_code"
token_response = auth_client.get_token_by_authorization_code(code)

# Обновление токена доступа
auth_client = SyncAuthClient(
    client_id="your_client_id",
    client_secret="your_client_secret",
    refresh_token="your_refresh_token"
)
token_response = auth_client.refresh_access_token()
```

#### Методы

```python
def get_token_by_authorization_code(self, code: str) -> OAuth2TokenResponse:
    """
    Получает токен доступа через код авторизации (authorization_code).

    Args:
        code: Код авторизации, полученный после подтверждения прав пользователем

    Returns:
        Информация о полученном токене доступа

    Raises:
        AuthError: Если не удалось получить токен
    """
```

### AsyncAuthClient

```python
from avito_api.auth import AsyncAuthClient
```

Асинхронный клиент для работы с API авторизации Авито.

#### Пример использования

```python
import asyncio

async def main():
    auth_client = AsyncAuthClient(
        client_id="your_client_id",
        client_secret="your_client_secret"
    )

    # Получение токена доступа через client_credentials
    token_info = await auth_client.get_token_async()

    # Получение токена доступа через код авторизации
    code = "authorization_code"
    token_response = await auth_client.get_token_by_authorization_code(code)

    # Обновление токена доступа
    auth_client = AsyncAuthClient(
        client_id="your_client_id",
        client_secret="your_client_secret",
        refresh_token="your_refresh_token"
    )
    token_response = await auth_client.refresh_access_token_async()

asyncio.run(main())
```

#### Методы

```python
async def get_token_by_authorization_code(self, code: str) -> OAuth2TokenResponse:
    """
    Асинхронно получает токен доступа через код авторизации (authorization_code).

    Args:
        code: Код авторизации, полученный после подтверждения прав пользователем

    Returns:
        Информация о полученном токене доступа

    Raises:
        AuthError: Если не удалось получить токен
    """
```

## Модели данных

### GrantType

```python
from avito_api.auth import GrantType
```

Enum-класс для типов авторизации OAuth.

```python
class GrantType(str, Enum):
    """Типы авторизации OAuth."""

    CLIENT_CREDENTIALS = "client_credentials"
    AUTHORIZATION_CODE = "authorization_code"
    REFRESH_TOKEN = "refresh_token"
```

### Scope

```python
from avito_api.auth import Scope
```

Enum-класс для доступных скоупов OAuth2 authorization_code.

```python
class Scope(str, Enum):
    """Доступные скоупы для OAuth2 authorization_code."""

    MESSENGER_READ = "messenger:read"
    MESSENGER_WRITE = "messenger:write"
    USER_BALANCE_READ = "user_balance:read"
    JOB_WRITE = "job:write"
    JOB_CV = "job:cv"
    JOB_VACANCY = "job:vacancy"
    JOB_APPLICATIONS = "job:applications"
    USER_OPERATIONS_READ = "user_operations:read"
    USER_READ = "user:read"
    AUTOLOAD_REPORTS = "autoload:reports"
    ITEMS_INFO = "items:info"
    ITEMS_APPLY_VAS = "items:apply_vas"
    SHORT_TERM_RENT_READ = "short_term_rent:read"
    SHORT_TERM_RENT_WRITE = "short_term_rent:write"
    STATS_READ = "stats:read"
```

### Модели запросов

```python
from avito_api.auth import GetTokenRequest, GetTokenOAuthRequest, RefreshTokenRequest
```

Модели для запросов на получение и обновление токенов.

```python
class GetTokenRequest(BaseModel):
    """Запрос на получение токена через client_credentials."""

    grant_type: str = Field(default=GrantType.CLIENT_CREDENTIALS, description="Тип OAuth flow")
    client_id: str = Field(..., description="Идентификатор клиента")
    client_secret: str = Field(..., description="Секрет клиента")

class GetTokenOAuthRequest(BaseModel):
    """Запрос на получение токена через authorization_code."""

    grant_type: str = Field(default=GrantType.AUTHORIZATION_CODE, description="Тип OAuth flow")
    client_id: str = Field(..., description="Идентификатор клиента")
    client_secret: str = Field(..., description="Секрет клиента")
    code: str = Field(..., description="Код авторизации")

class RefreshTokenRequest(BaseModel):
    """Запрос на обновление токена через refresh_token."""

    grant_type: str = Field(default=GrantType.REFRESH_TOKEN, description="Тип OAuth flow")
    client_id: str = Field(..., description="Идентификатор клиента")
    client_secret: str = Field(..., description="Секрет клиента")
    refresh_token: str = Field(..., description="Токен обновления")
```

### Модели ответов

```python
from avito_api.auth import TokenResponse, OAuth2TokenResponse
```

Модели для ответов с информацией о токене.

```python
class TokenResponse(BaseModel):
    """Базовый ответ с информацией о токене."""

    access_token: str = Field(..., description="Ключ для временной авторизации в системе")
    expires_in: int = Field(..., description="Время жизни ключа в секундах")
    token_type: str = Field(..., description="Тип ключа авторизации")

class OAuth2TokenResponse(TokenResponse):
    """Ответ с информацией о токене OAuth2 (с refresh_token)."""

    refresh_token: Optional[str] = Field(None, description="Ключ для обновления токена доступа")
    scope: Optional[str] = Field(None, description="Полученный скоуп")
```

## Примеры использования

### Получение токена через client_credentials

```python
from avito_api.auth import SyncAuthClient

auth_client = SyncAuthClient(
    client_id="your_client_id",
    client_secret="your_client_secret"
)

token_info = auth_client.get_token()

print(f"Токен: {token_info.access_token}")
print(f"Истекает через: {token_info.expires_in} секунд")
print(f"Тип токена: {token_info.token_type}")
```

### Получение токена через OAuth2 authorization_code

```python
from avito_api.auth import SyncAuthClient, Scope

auth_client = SyncAuthClient(
    client_id="your_client_id",
    client_secret="your_client_secret"
)

# Формируем URL для авторизации
auth_url = auth_client.get_authorization_url(
    client_id="your_client_id",
    scopes=[Scope.MESSENGER_READ, Scope.MESSENGER_WRITE],
    state="random_state",  # Для защиты от CSRF
    redirect_uri="https://your-app.com/callback"
)

print(f"URL для авторизации: {auth_url}")

# После редиректа с кодом авторизации
code = "authorization_code_from_callback"

# Обмениваем код на токен
token_response = auth_client.get_token_by_authorization_code(code)

print(f"Access token: {token_response.access_token}")
print(f"Refresh token: {token_response.refresh_token}")
print(f"Scope: {token_response.scope}")
```

### Обновление токена доступа

```python
from avito_api.auth import SyncAuthClient

auth_client = SyncAuthClient(
    client_id="your_client_id",
    client_secret="your_client_secret",
    refresh_token="your_refresh_token"
)

token_response = auth_client.refresh_access_token()

print(f"Новый access token: {token_response.access_token}")
print(f"Новый refresh token: {token_response.refresh_token}")
```

### Асинхронное получение токена

```python
import asyncio
from avito_api.auth import AsyncAuthClient

async def main():
    auth_client = AsyncAuthClient(
        client_id="your_client_id",
        client_secret="your_client_secret"
    )

    token_info = await auth_client.get_token_async()

    print(f"Токен: {token_info.access_token}")

asyncio.run(main())
```

## Ошибки авторизации

При работе с авторизацией могут возникать следующие исключения:

```python
from avito_api.exceptions import AuthError, TokenExpiredError

try:
    token_info = auth_client.get_token()
except AuthError as e:
    print(f"Ошибка авторизации: {str(e)}")
except TokenExpiredError as e:
    print(f"Истек срок действия токена: {str(e)}")
```

## Интеграция с другими модулями

Клиенты авторизации можно использовать вместе с другими клиентами библиотеки:

```python
from avito_api.auth import SyncAuthClient
from avito_api.messenger import SyncMessengerClient

# Получаем токен через OAuth
auth_client = SyncAuthClient(
    client_id="your_client_id",
    client_secret="your_client_secret"
)

code = "authorization_code_from_callback"
token_response = auth_client.get_token_by_authorization_code(code)

# Создаем клиент мессенджера с полученными токенами
messenger_client = SyncMessengerClient(
    client_id="your_client_id",
    client_secret="your_client_secret",
    access_token=token_response.access_token,
    refresh_token=token_response.refresh_token,
    token_expires_at=token_response.expires_in  # Библиотека автоматически преобразует в timestamp
)

# Теперь можно работать с мессенджером от имени пользователя
# ...
```
