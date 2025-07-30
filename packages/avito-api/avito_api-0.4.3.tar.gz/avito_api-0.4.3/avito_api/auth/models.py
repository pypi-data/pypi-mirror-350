"""
Модели данных для модуля авторизации API Авито.
"""
from enum import Enum
from typing import Optional, Any

from pydantic import BaseModel, Field


class GrantType(str, Enum):
    """Типы авторизации OAuth."""

    CLIENT_CREDENTIALS = "client_credentials"
    AUTHORIZATION_CODE = "authorization_code"
    REFRESH_TOKEN = "refresh_token"


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


class TokenResponse(BaseModel):
    """Базовый ответ с информацией о токене."""

    access_token: str = Field(..., description="Ключ для временной авторизации в системе")
    expires_in: int = Field(..., description="Время жизни ключа в секундах")
    token_type: str = Field(..., description="Тип ключа авторизации")


class OAuth2TokenResponse(TokenResponse):
    """Ответ с информацией о токене OAuth2 (с refresh_token)."""

    refresh_token: Optional[str] = Field(None, description="Ключ для обновления токена доступа")
    scope: Optional[str] = Field(None, description="Полученный скоуп")


class ErrorResponse(BaseModel):
    """Модель ошибки API."""

    error: dict[str, Any] = Field(..., description="Информация об ошибке")


# Модели для авторизационных скоупов
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
