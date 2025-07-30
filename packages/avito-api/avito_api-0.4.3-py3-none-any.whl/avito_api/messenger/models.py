"""
Модели данных для модуля мессенджера API Авито.
"""
from enum import Enum
from typing import Any, Optional, Union

from pydantic import BaseModel, Field, HttpUrl, model_validator


class ChatType(str, Enum):
    """Типы чатов."""

    USER_TO_ITEM = "u2i"  # Чаты по объявлениям
    USER_TO_USER = "u2u"  # Чаты между пользователями


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


class MessageDirection(str, Enum):
    """Направления сообщений."""

    IN = "in"  # Входящие
    OUT = "out"  # Исходящие


class BlacklistReasonId(int, Enum):
    """Причины добавления пользователя в черный список."""

    SPAM = 1
    FRAUD = 2
    INSULT = 3
    OTHER = 4


# Модели запросов
class SendMessageRequest(BaseModel):
    """Запрос на отправку текстового сообщения."""

    type: MessageType = Field(MessageType.TEXT, description="Тип сообщения")
    message: dict[str, str] = Field(..., description="Данные сообщения")


class SendImageMessageRequest(BaseModel):
    """Запрос на отправку сообщения с изображением."""

    image_id: str = Field(..., description="Идентификатор загруженного изображения")


class WebhookSubscribeRequest(BaseModel):
    """Запрос на подписку на webhook."""

    url: str = Field(..., description="URL для получения уведомлений")


class BlacklistUserContext(BaseModel):
    """Контекст для блокировки пользователя."""

    item_id: Optional[int] = Field(None, description="ID объявления")
    reason_id: BlacklistReasonId = Field(..., description="Причина блокировки")


class BlacklistUser(BaseModel):
    """Информация о пользователе для добавления в черный список."""

    user_id: int = Field(..., description="ID пользователя для блокировки")
    context: BlacklistUserContext = Field(..., description="Контекст блокировки")


class AddBlacklistRequest(BaseModel):
    """Запрос на добавление пользователей в черный список."""

    users: list[BlacklistUser] = Field(..., description="Список пользователей для блокировки")


# Модели содержимого сообщений
class CallContent(BaseModel):
    """Содержимое сообщения типа call."""

    status: str = Field(..., description="Статус звонка")
    target_user_id: int = Field(..., description="ID целевого пользователя")


class ImageContent(BaseModel):
    """Содержимое сообщения типа image."""

    sizes: dict[str, str] = Field(..., description="Размеры и URL изображений")


class ImagesContent(BaseModel):
    """ Изображения с карточки объявления """
    count: int = Field(..., description="Число изображений")
    main: dict[str, HttpUrl] = Field(..., description="Изображение в формате 140х105. {'140х105': URL}")


class ItemContent(BaseModel):
    """Содержимое сообщения типа item."""

    image_url: HttpUrl = Field(..., description="URL изображения объявления")
    item_url: HttpUrl = Field(..., description="URL объявления")
    price_string: Optional[str] = Field(None, description="Цена в строковом формате")
    title: str = Field(..., description="Заголовок объявления")


class ItemContentWebhook(BaseModel):
    """Содержимое сообщения типа item в webhook."""

    id: int = Field(..., description="ID объявления")
    images: ImagesContent = Field(..., description="Изображения с карточки объявления")
    url: HttpUrl = Field(..., description="Ссылка на объявление")
    price_string: Optional[str] = Field(None, description="Цена в объявлении, с указанием валюты")
    title: str = Field(..., description="Заголовок объявления")
    status_id: Optional[int] = Field(None, description="Статус объявления, например 20 — объявление удалено")


class LinkPreview(BaseModel):
    """Предпросмотр ссылки."""

    description: Optional[str] = Field(None, description="Описание ссылки")
    domain: str = Field(..., description="Домен ссылки")
    images: Optional[dict[str, str]] = Field(None, description="Изображения предпросмотра")
    title: str = Field(..., description="Заголовок страницы")
    url: HttpUrl = Field(..., description="URL страницы")


class LinkContent(BaseModel):
    """Содержимое сообщения типа link."""

    preview: Optional[LinkPreview] = Field(None, description="Предпросмотр ссылки")
    text: str = Field(..., description="Текст ссылки")
    url: str = Field(..., description="URL ссылки")


class LocationContent(BaseModel):
    """Содержимое сообщения типа location."""

    kind: str = Field(..., description="Тип местоположения")
    lat: float = Field(..., description="Широта")
    lon: float = Field(..., description="Долгота")
    text: str = Field(..., description="Текстовое представление")
    title: str = Field(..., description="Заголовок местоположения")


class VoiceContent(BaseModel):
    """Содержимое сообщения типа voice."""

    voice_id: str = Field(..., description="ID голосового сообщения")


class MessageContent(BaseModel):
    """Содержимое сообщения разных типов."""

    text: Optional[str] = Field(None, description="Текст сообщения для типа text")
    call: Optional[CallContent] = Field(None, description="Данные звонка для типа call")
    image: Optional[ImageContent] = Field(None, description="Данные изображения для типа image")
    item: Optional[Union[ItemContent, ItemContentWebhook]] = Field(None, description="Данные объявления для типа item")
    link: Optional[LinkContent] = Field(None, description="Данные ссылки для типа link")
    location: Optional[LocationContent] = Field(None, description="Данные местоположения для типа location")
    voice: Optional[VoiceContent] = Field(None, description="Данные голосового сообщения для типа voice")
    flow_id: Optional[str] = Field(None, description="ID чат-бота для типа system")


# Модели ответов
class MessageQuote(BaseModel):
    """Цитируемое сообщение."""

    author_id: int = Field(..., description="ID автора сообщения")
    content: MessageContent = Field(..., description="Содержимое сообщения")
    created: int = Field(..., description="Время создания сообщения (Unix timestamp)")
    id: str = Field(..., description="ID сообщения")
    type: MessageType = Field(..., description="Тип сообщения")


class Message(BaseModel):
    """Модель сообщения."""

    author_id: int = Field(..., description="ID автора сообщения")
    content: MessageContent = Field(..., description="Содержимое сообщения")
    created: int = Field(..., description="Время создания сообщения (Unix timestamp)")
    direction: MessageDirection = Field(..., description="Направление сообщения")
    id: str = Field(..., description="ID сообщения")
    is_read: Optional[bool] = Field(None, description="Прочитано ли сообщение")
    quote: Optional[MessageQuote] = Field(None, description="Цитируемое сообщение")
    read: Optional[int] = Field(None, description="Время прочтения сообщения (Unix timestamp)")
    type: MessageType = Field(..., description="Тип сообщения")


class Messages(BaseModel):
    """Список сообщений."""

    messages: list[Message] = Field(..., description="Список сообщений")


class WebhookContent(BaseModel):
    """ Данные сообщения в webhook. """

    id: str = Field(..., description="ID сообщения")
    user_id: int = Field(..., description="ID получателя сообщения")
    author_id: int = Field(..., description="ID автора сообщения")
    chat_id: str = Field(..., description="ID чата")
    chat_type: ChatType = Field(..., description="Тип чата")
    content: MessageContent = Field(..., description="Содержимое сообщения")
    created: int = Field(..., description="Время создания сообщения (Unix timestamp)")
    item_id: Optional[int] = Field(None, description="ID объявления (для чатов u2i)")
    read: Optional[int] = Field(None, description="Время прочтения сообщения (Unix timestamp)")
    type: MessageType = Field(...,
                              description="Тип контекста, определяет значение и смысл других полей в объекте контекста")
    direction: Optional[MessageDirection] = Field(None, description="Направление сообщения")

    @model_validator(mode='before')
    def check_direction(cls, values):
        if values['user_id'] == values['author_id']:
            values['direction'] = MessageDirection.OUT
        else:
            values['direction'] = MessageDirection.IN
        return values


class WebhookPayload(BaseModel):
    """ Объект данных в сообщении webhook"""
    type: str = Field(..., description="Тип контекста, определяет значение и смысл других полей в объекте контекста")
    value: WebhookContent = Field(..., description="Данные сообщения")


class WebhookMessage(BaseModel):
    """ Сообщение, отправляемое через webhook. """
    id: str = Field(..., description="ID сообщения")
    version: Optional[str] = Field(None, description="Версия API")
    timestamp: int = Field(..., description="Время создания сообщения (Unix timestamp)")
    payload: WebhookPayload = Field(..., description="Данные сообщения")


class UserAvatar(BaseModel):
    """Аватар пользователя."""

    default: str = Field(..., description="URL аватара по умолчанию")
    images: dict[str, str] = Field(..., description="URL аватаров разных размеров")


class UserProfile(BaseModel):
    """Профиль пользователя."""

    avatar: UserAvatar = Field(..., description="Аватар пользователя")
    item_id: Optional[int] = Field(None, description="ID объявления пользователя")
    url: HttpUrl = Field(..., description="URL профиля пользователя")
    user_id: int = Field(..., description="ID пользователя")


class User(BaseModel):
    """Пользователь в чате."""

    id: int = Field(..., description="ID пользователя")
    name: str = Field(..., description="Имя пользователя")
    public_user_profile: Optional[UserProfile] = Field(None, description="Публичный профиль пользователя")


class ItemContext(BaseModel):
    """Контекст объявления в чате."""

    id: int = Field(..., description="ID объявления")
    images: dict[str, Any] = Field(..., description="Изображения объявления")
    price_string: str = Field(..., description="Цена в строковом формате")
    status_id: int = Field(..., description="Статус объявления")
    title: str = Field(..., description="Заголовок объявления")
    url: HttpUrl = Field(..., description="URL объявления")
    user_id: int = Field(..., description="ID автора объявления")


class ChatContext(BaseModel):
    """Контекст чата."""

    type: str = Field(..., description="Тип контекста")
    value: ItemContext = Field(..., description="Данные контекста")


class LastMessage(BaseModel):
    """Последнее сообщение в чате."""

    author_id: int = Field(..., description="ID автора сообщения")
    content: MessageContent = Field(..., description="Содержимое сообщения")
    created: int = Field(..., description="Время создания сообщения (Unix timestamp)")
    direction: MessageDirection = Field(..., description="Направление сообщения")
    id: str = Field(..., description="ID сообщения")
    type: MessageType = Field(..., description="Тип сообщения")


class Chat(BaseModel):
    """Модель чата."""

    context: Optional[ChatContext] = Field(None, description="Контекст чата")
    created: int = Field(..., description="Время создания чата (Unix timestamp)")
    id: str = Field(..., description="ID чата")
    last_message: LastMessage = Field(..., description="Последнее сообщение в чате")
    updated: int = Field(..., description="Время обновления чата (Unix timestamp)")
    users: list[User] = Field(..., description="Пользователи в чате")


class Chats(BaseModel):
    """Список чатов."""

    chats: list[Chat] = Field(..., description="Список чатов")


class VoiceFiles(BaseModel):
    """Информация о файлах голосовых сообщений."""

    voices_urls: dict[str, str] = Field(..., description="URL голосовых сообщений по ID")


class WebhookSubscription(BaseModel):
    """Информация о подписке на webhook."""

    url: str = Field(..., description="URL для уведомлений")
    version: str = Field(..., description="Версия API вебхука")


class WebhookSubscriptions(BaseModel):
    """Список подписок на webhook."""

    subscriptions: list[WebhookSubscription] = Field(..., description="Список подписок")


class SuccessResponse(BaseModel):
    """Успешный ответ с подтверждением."""

    ok: bool = Field(..., description="Подтверждение успешного выполнения")
