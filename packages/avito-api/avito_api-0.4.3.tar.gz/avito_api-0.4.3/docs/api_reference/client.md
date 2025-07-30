# Справочник API: Базовые клиенты

Модуль `avito_api.client` содержит базовые классы для работы с API Авито.

## Базовые классы

### BaseApiClient

```python
from avito_api.client import BaseApiClient
```

Абстрактный базовый класс для всех клиентов API. Определяет общий интерфейс и функциональность для синхронных и асинхронных клиентов.

#### Конструктор

```python
def __init__(
    self,
    client_id: str,
    client_secret: str,
    access_token: Optional[str] = None,
    refresh_token: Optional[str] = None,
    token_expires_at: Optional[float] = None,
    config: Optional[ClientConfig] = None,
):
    """
    Инициализирует клиент API Авито.

    Args:
        client_id: Идентификатор клиента
        client_secret: Секрет клиента
        access_token: Опциональный токен доступа (если уже есть)
        refresh_token: Опциональный токен обновления (если уже есть)
        token_expires_at: Опциональное время истечения токена (если уже есть)
        config: Опциональная конфигурация клиента
    """
```

#### Основные методы

Класс `BaseApiClient` определяет следующие абстрактные методы, которые должны быть реализованы в дочерних классах:

```python
@abstractmethod
async def _request_async(
    self,
    method: str,
    url: str,
    params: Optional[Dict[str, Any]] = None,
    data: Optional[Dict[str, Any]] = None,
    json_data: Optional[Dict[str, Any]] = None,
    headers: Optional[Dict[str, str]] = None,
    auth_required: bool = True,
    form_encoded: bool = False,
    multipart: bool = False,
    files: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Выполняет асинхронный HTTP-запрос к API.
    """
    pass

@abstractmethod
def _request_sync(
    self,
    method: str,
    url: str,
    params: Optional[Dict[str, Any]] = None,
    data: Optional[Dict[str, Any]] = None,
    json_data: Optional[Dict[str, Any]] = None,
    headers: Optional[Dict[str, str]] = None,
    auth_required: bool = True,
    form_encoded: bool = False,
    multipart: bool = False,
    files: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Выполняет синхронный HTTP-запрос к API.
    """
    pass

@abstractmethod
def get_token(self) -> Dict[str, Any]:
    """
    Получает токен доступа через client_credentials.
    """
    pass

@abstractmethod
async def get_token_async(self) -> Dict[str, Any]:
    """
    Асинхронно получает токен доступа через client_credentials.
    """
    pass

@abstractmethod
def refresh_access_token(self) -> Dict[str, Any]:
    """
    Обновляет токен доступа с использованием refresh_token.
    """
    pass

@abstractmethod
async def refresh_access_token_async(self) -> Dict[str, Any]:
    """
    Асинхронно обновляет токен доступа с использованием refresh_token.
    """
    pass
```

#### Вспомогательные методы

Класс также предоставляет несколько вспомогательных методов:

```python
def _get_auth_header(self) -> Dict[str, str]:
    """
    Возвращает заголовок с токеном авторизации.

    Returns:
        Словарь с заголовком Authorization

    Raises:
        AuthError: Если токен не установлен
    """

def _is_token_expired(self) -> bool:
    """
    Проверяет, истек ли токен доступа.

    Returns:
        True, если токен истек или истечет в ближайшее время, иначе False
    """

def _update_token_info(
    self,
    access_token: str,
    expires_in: int,
    token_type: str = "Bearer",
    refresh_token: Optional[str] = None,
) -> None:
    """
    Обновляет информацию о токене авторизации.

    Args:
        access_token: Новый токен доступа
        expires_in: Время жизни токена в секундах
        token_type: Тип токена
        refresh_token: Новый токен обновления (если есть)
    """

def _build_url(self, endpoint: str) -> str:
    """
    Строит полный URL для запроса.

    Args:
        endpoint: Эндпоинт API

    Returns:
        Полный URL для запроса
    """

def _handle_response(
    self,
    status_code: int,
    content: Union[str, bytes],
    headers: Dict[str, str]
) -> Dict[str, Any]:
    """
    Обрабатывает ответ от API.

    Args:
        status_code: Код статуса ответа
        content: Тело ответа
        headers: Заголовки ответа

    Returns:
        Словарь с данными ответа

    Raises:
        AvitoApiError: При ошибке обработки ответа
    """

def parse_response_model(self, model_class: Type[T], data: Dict[str, Any]) -> T:
    """
    Парсит данные ответа в модель Pydantic.

    Args:
        model_class: Класс модели для парсинга
        data: Данные для парсинга

    Returns:
        Экземпляр модели с данными
    """
```

### SyncApiClient

```python
from avito_api.client import SyncApiClient
```

Синхронная реализация клиента API Авито на базе библиотеки requests.

#### Пример использования

```python
client = SyncApiClient(
    client_id="your_client_id",
    client_secret="your_client_secret"
)

# Получаем токен
client.get_token()

# Выполняем запрос
response = client._request_sync(
    method="GET",
    url="/some/endpoint",
    params={"param1": "value1"},
    auth_required=True
)
```

### AsyncApiClient

```python
from avito_api.client import AsyncApiClient
```

Асинхронная реализация клиента API Авито на базе библиотеки httpx.

#### Пример использования

```python
import asyncio

async def main():
    client = AsyncApiClient(
        client_id="your_client_id",
        client_secret="your_client_secret"
    )

    # Получаем токен
    await client.get_token_async()

    # Выполняем запрос
    response = await client._request_async(
        method="GET",
        url="/some/endpoint",
        params={"param1": "value1"},
        auth_required=True
    )

    print(response)

asyncio.run(main())
```

## Классы конфигурации

### ClientConfig

```python
from avito_api.config import ClientConfig
```

Класс для настройки клиента API Авито.

#### Конструктор

```python
def __init__(
    self,
    api: ApiConfig = Field(default_factory=ApiConfig),
    logging: LogConfig = Field(default_factory=LogConfig)
):
    """
    Создает конфигурацию клиента.

    Args:
        api: Настройки API
        logging: Настройки логирования
    """
```

### ApiConfig

```python
from avito_api.config import ApiConfig
```

Класс для настройки параметров API.

#### Конструктор

```python
def __init__(
    self,
    base_url: str = "https://api.avito.ru",
    timeout: float = 30.0,
    max_retries: int = 3,
    retry_delay: float = 1.0,
    user_agent: str = "AvitoApiClient/1.0",
    auto_refresh_token: bool = True,
    token_refresh_threshold: int = 300
):
    """
    Создает конфигурацию API.

    Args:
        base_url: Базовый URL API
        timeout: Таймаут запросов в секундах
        max_retries: Максимальное количество повторных попыток
        retry_delay: Задержка между повторными попытками в секундах
        user_agent: User-Agent для запросов
        auto_refresh_token: Автоматически обновлять токен при истечении
        token_refresh_threshold: Порог в секундах для обновления токена до истечения
    """
```

### LogConfig

```python
from avito_api.config import LogConfig
```

Класс для настройки логирования.

#### Конструктор

```python
def __init__(
    self,
    level: str = "INFO",
    format: str = "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
    sink: Optional[str] = None,
    rotation: Optional[Union[str, int]] = None,
    retention: Optional[Union[str, int]] = None,
    enqueue: bool = False,
    diagnose: bool = True,
    serialize: bool = False
):
    """
    Создает конфигурацию логирования.

    Args:
        level: Уровень логирования
        format: Формат логов
        sink: Путь к файлу или stdout/stderr
        rotation: Настройки ротации логов (например, '10 MB')
        retention: Настройки хранения логов (например, '1 week')
        enqueue: Использовать ли очередь для логирования
        diagnose: Включить диагностику исключений
        serialize: Сериализовать логи в JSON формат
    """
```

## Глобальные настройки логирования

Библиотека использует loguru для логирования. Вы можете настроить логирование в любой момент:

```python
from avito_api.config import logger

# Настройка логирования
logger.remove()  # Удаляем встроенный обработчик
logger.add("avito_api.log", level="DEBUG", rotation="10 MB")

# Или можно использовать ClientConfig
from avito_api.config import ClientConfig, LogConfig

config = ClientConfig(
    logging=LogConfig(
        level="DEBUG",
        sink="avito_api.log",
        rotation="10 MB"
    )
)

config.setup_logging()  # Применяем настройки
```

## Обработка ошибок

При работе с API могут возникать различные исключения:

```python
from avito_api.exceptions import (
    AvitoApiError,  # Базовое исключение
    AuthError,      # Ошибка авторизации
    TokenExpiredError,  # Истек срок действия токена
    ForbiddenError,     # Доступ запрещен
    NotFoundError,      # Ресурс не найден
    ValidationError,    # Ошибка валидации данных
    RateLimitError,     # Превышен лимит запросов
    ServerError,        # Ошибка сервера
    NetworkError,       # Ошибка сети
    ConfigError         # Ошибка конфигурации
)
```

Все исключения наследуются от `AvitoApiError`, что позволяет легко перехватывать все ошибки библиотеки:

```python
try:
    client.get_token()
except AvitoApiError as e:
    print(f"Произошла ошибка: {str(e)}")
```
