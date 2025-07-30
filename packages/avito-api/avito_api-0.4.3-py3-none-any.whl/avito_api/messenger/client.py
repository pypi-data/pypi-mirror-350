"""
Клиент для работы с API мессенджера Авито.
"""
import os
from typing import Optional, Union, Any, BinaryIO

from ..client import SyncApiClient, AsyncApiClient
from ..config import logger
from ..exceptions import ValidationError
from .models import (
    ChatType, MessageType, Messages, Message, Chat, Chats,
    SendMessageRequest, SendImageMessageRequest, WebhookSubscribeRequest,
    AddBlacklistRequest, BlacklistUser, SuccessResponse,
    WebhookSubscriptions, VoiceFiles
)


class BaseMessengerClient:
    """
    Базовый класс для работы с API мессенджера Авито.
    """

    def _validate_message_text(self, text: str) -> None:
        """
        Проверяет валидность текста сообщения.

        Args:
            text: Текст сообщения

        Raises:
            ValidationError: Если текст сообщения не валиден
        """
        if not text or not isinstance(text, str):
            raise ValidationError("Текст сообщения не может быть пустым")

        if len(text) > 4000:  # Предполагаемое ограничение на длину сообщения
            raise ValidationError(
                f"Текст сообщения слишком длинный ({len(text)} символов). "
                f"Максимальная длина - 4000 символов"
            )


class SyncMessengerClient(BaseMessengerClient, SyncApiClient):
    """
    Синхронный клиент для работы с API мессенджера Авито.
    """

    def get_chats(
        self,
        user_id: int,
        item_ids: Optional[list[int]] = None,
        unread_only: bool = False,
        chat_types: Optional[list[Union[ChatType, str]]] = None,
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
        logger.debug(f"Запрос списка чатов для пользователя {user_id}")

        # Преобразуем chat_types в строки, если они переданы как Enum
        if chat_types:
            chat_types_str = [ct.value if isinstance(ct, ChatType) else ct for ct in chat_types]
        else:
            chat_types_str = None

        params = {
            "unread_only": unread_only,
            "limit": limit,
            "offset": offset,
        }

        if item_ids:
            params["item_ids"] = ",".join(str(item_id) for item_id in item_ids)

        if chat_types_str:
            params["chat_types"] = ",".join(chat_types_str)

        response = self._request_sync(
            method="GET",
            url=f"/messenger/v2/accounts/{user_id}/chats",
            params=params,
        )

        return Chats(**response)

    def get_chat(self, user_id: int, chat_id: str) -> Chat:
        """
        Получает информацию о конкретном чате.

        Args:
            user_id: Идентификатор пользователя
            chat_id: Идентификатор чата

        Returns:
            Информация о чате
        """
        logger.debug(f"Запрос информации о чате {chat_id} для пользователя {user_id}")

        response = self._request_sync(
            method="GET",
            url=f"/messenger/v2/accounts/{user_id}/chats/{chat_id}",
        )

        return Chat(**response)

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
        logger.debug(f"Запрос сообщений чата {chat_id} для пользователя {user_id}")

        params = {
            "limit": limit,
            "offset": offset,
        }

        response = self._request_sync(
            method="GET",
            url=f"/messenger/v3/accounts/{user_id}/chats/{chat_id}/messages/",
            params=params,
        )
        return Messages(**response)

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
        logger.debug(f"Отправка сообщения в чат {chat_id} от пользователя {user_id}")

        # Проверяем валидность текста сообщения
        self._validate_message_text(text)

        request = SendMessageRequest(
            type=MessageType.TEXT,
            message={"text": text},
        )

        response = self._request_sync(
            method="POST",
            url=f"/messenger/v1/accounts/{user_id}/chats/{chat_id}/messages",
            json_data=request.dict(),
        )

        return Message(**response)

    def upload_image(
        self,
        user_id: int,
        image_file: Union[str, bytes, BinaryIO],
    ) -> dict[str, dict[str, str]]:
        """
        Загружает изображение для последующей отправки в сообщении.

        Args:
            user_id: Идентификатор пользователя
            image_file: Путь к файлу, содержимое файла в байтах или открытый файловый объект

        Returns:
            Информация о загруженном изображении
        """
        logger.debug(f"Загрузка изображения для пользователя {user_id}")

        files = {}

        # Если передана строка, считаем её путём к файлу
        if isinstance(image_file, str):
            if not os.path.isfile(image_file):
                raise ValidationError(f"Файл не найден: {image_file}")

            file_name = os.path.basename(image_file)
            files = {"uploadfile[]": (file_name, open(image_file, "rb"))}

        # Если переданы байты, используем их
        elif isinstance(image_file, bytes):
            files = {"uploadfile[]": ("image.jpg", image_file)}

        # Если передан файловый объект, используем его
        elif hasattr(image_file, "read"):
            file_name = getattr(image_file, "name", "image.jpg")
            files = {"uploadfile[]": (os.path.basename(file_name), image_file)}

        else:
            raise ValidationError(
                "Неверный тип файла. Ожидается путь к файлу, байты или файловый объект"
            )

        response = self._request_sync(
            method="POST",
            url=f"/messenger/v1/accounts/{user_id}/uploadImages",
            files=files,
            multipart=True,
        )

        return response

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
        logger.debug(f"Отправка сообщения с изображением в чат {chat_id} от пользователя {user_id}")

        request = SendImageMessageRequest(image_id=image_id)

        response = self._request_sync(
            method="POST",
            url=f"/messenger/v1/accounts/{user_id}/chats/{chat_id}/messages/image",
            json_data=request.dict(),
        )

        return Message(**response)

    def mark_chat_as_read(self, user_id: int, chat_id: str) -> SuccessResponse:
        """
        Отмечает чат как прочитанный.

        Args:
            user_id: Идентификатор пользователя
            chat_id: Идентификатор чата

        Returns:
            Подтверждение успешного выполнения операции
        """
        logger.debug(f"Отметка чата {chat_id} как прочитанного для пользователя {user_id}")

        response = self._request_sync(
            method="POST",
            url=f"/messenger/v1/accounts/{user_id}/chats/{chat_id}/read",
        )

        if not response:
            return SuccessResponse(ok=True)
        else:
            return SuccessResponse(**response)

    def delete_message(self, user_id: int, chat_id: str, message_id: str) -> dict[str, Any]:
        """
        Удаляет сообщение из чата.

        Args:
            user_id: Идентификатор пользователя
            chat_id: Идентификатор чата
            message_id: Идентификатор сообщения

        Returns:
            Подтверждение успешного выполнения операции
        """
        logger.debug(f"Удаление сообщения {message_id} из чата {chat_id} пользователя {user_id}")

        response = self._request_sync(
            method="POST",
            url=f"/messenger/v1/accounts/{user_id}/chats/{chat_id}/messages/{message_id}",
        )

        return response

    def get_voice_files(self, user_id: int, voice_ids: list[str]) -> VoiceFiles:
        """
        Получает ссылки на файлы голосовых сообщений.

        Args:
            user_id: Идентификатор пользователя
            voice_ids: Список идентификаторов голосовых сообщений

        Returns:
            Ссылки на файлы голосовых сообщений
        """
        logger.debug(f"Запрос файлов голосовых сообщений для пользователя {user_id}")

        params = {"voice_ids": ",".join(voice_ids)}

        response = self._request_sync(
            method="GET",
            url=f"/messenger/v1/accounts/{user_id}/getVoiceFiles",
            params=params,
        )

        return VoiceFiles(**response)

    def subscribe_webhook(self, url: str) -> SuccessResponse:
        """
        Подписывается на webhook-уведомления.

        Args:
            url: URL для получения уведомлений

        Returns:
            Подтверждение успешной подписки
        """
        logger.debug(f"Подписка на webhook-уведомления: {url}")

        request = WebhookSubscribeRequest(url=url)

        response = self._request_sync(
            method="POST",
            url="/messenger/v3/webhook",
            json_data=request.dict(),
        )

        return SuccessResponse(**response)

    def unsubscribe_webhook(self, url: str) -> SuccessResponse:
        """
        Отписывается от webhook-уведомлений.

        Args:
            url: URL, на который больше не нужно отправлять уведомления

        Returns:
            Подтверждение успешной отписки
        """
        logger.debug(f"Отписка от webhook-уведомлений: {url}")

        request = WebhookSubscribeRequest(url=url)

        response = self._request_sync(
            method="POST",
            url="/messenger/v1/webhook/unsubscribe",
            json_data=request.dict(),
        )

        return SuccessResponse(**response)

    def get_webhook_subscriptions(self) -> WebhookSubscriptions:
        """
        Получает список подписок на webhook-уведомления.

        Returns:
            Список подписок на webhook-уведомления
        """
        logger.debug("Запрос списка подписок на webhook-уведомления")

        response = self._request_sync(
            method="POST",
            url="/messenger/v1/subscriptions",
        )

        return WebhookSubscriptions(**response)

    def add_to_blacklist(self, user_id: int, blacklist_users: list[BlacklistUser]) -> dict[str, Any]:
        """
        Добавляет пользователей в черный список.

        Args:
            user_id: Идентификатор пользователя
            blacklist_users: Список пользователей для добавления в черный список

        Returns:
            Подтверждение успешного выполнения операции
        """
        logger.debug(f"Добавление пользователей в черный список для пользователя {user_id}")

        request = AddBlacklistRequest(users=blacklist_users)

        response = self._request_sync(
            method="POST",
            url=f"/messenger/v2/accounts/{user_id}/blacklist",
            json_data=request.dict(),
        )

        return response


class AsyncMessengerClient(BaseMessengerClient, AsyncApiClient):
    """
    Асинхронный клиент для работы с API мессенджера Авито.
    """

    async def get_chats(
        self,
        user_id: int,
        item_ids: Optional[list[int]] = None,
        unread_only: bool = False,
        chat_types: Optional[list[Union[ChatType, str]]] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> Chats:
        """
        Асинхронно получает список чатов пользователя.

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
        logger.debug(f"Асинхронный запрос списка чатов для пользователя {user_id}")

        # Преобразуем chat_types в строки, если они переданы как Enum
        if chat_types:
            chat_types_str = [ct.value if isinstance(ct, ChatType) else ct for ct in chat_types]
        else:
            chat_types_str = None

        params = {
            "unread_only": unread_only,
            "limit": limit,
            "offset": offset,
        }

        if item_ids:
            params["item_ids"] = ",".join(str(item_id) for item_id in item_ids)

        if chat_types_str:
            params["chat_types"] = ",".join(chat_types_str)

        response = await self._request_async(
            method="GET",
            url=f"/messenger/v2/accounts/{user_id}/chats",
            params=params,
        )

        return Chats(**response)

    async def get_chat(self, user_id: int, chat_id: str) -> Chat:
        """
        Асинхронно получает информацию о конкретном чате.

        Args:
            user_id: Идентификатор пользователя
            chat_id: Идентификатор чата

        Returns:
            Информация о чате
        """
        logger.debug(f"Асинхронный запрос информации о чате {chat_id} для пользователя {user_id}")

        response = await self._request_async(
            method="GET",
            url=f"/messenger/v2/accounts/{user_id}/chats/{chat_id}",
        )

        return Chat(**response)

    async def get_messages(
        self,
        user_id: int,
        chat_id: str,
        limit: int = 100,
        offset: int = 0,
    ) -> Messages:
        """
        Асинхронно получает список сообщений в чате.

        Args:
            user_id: Идентификатор пользователя
            chat_id: Идентификатор чата
            limit: Максимальное количество сообщений
            offset: Смещение в выборке

        Returns:
            Список сообщений в чате
        """
        logger.debug(f"Асинхронный запрос сообщений чата {chat_id} для пользователя {user_id}")

        params = {
            "limit": limit,
            "offset": offset,
        }

        response = await self._request_async(
            method="GET",
            url=f"/messenger/v3/accounts/{user_id}/chats/{chat_id}/messages/",
            params=params,
        )

        return Messages(**response)

    async def send_message(
        self,
        user_id: int,
        chat_id: str,
        text: str,
    ) -> Message:
        """
        Асинхронно отправляет текстовое сообщение в чат.

        Args:
            user_id: Идентификатор пользователя
            chat_id: Идентификатор чата
            text: Текст сообщения

        Returns:
            Информация об отправленном сообщении
        """
        logger.debug(f"Асинхронная отправка сообщения в чат {chat_id} от пользователя {user_id}")

        # Проверяем валидность текста сообщения
        self._validate_message_text(text)

        request = SendMessageRequest(
            type=MessageType.TEXT,
            message={"text": text},
        )

        response = await self._request_async(
            method="POST",
            url=f"/messenger/v1/accounts/{user_id}/chats/{chat_id}/messages",
            json_data=request.dict(),
        )

        return Message(**response)

    async def upload_image(
        self,
        user_id: int,
        image_file: Union[str, bytes, BinaryIO],
    ) -> dict[str, dict[str, str]]:
        """
        Асинхронно загружает изображение для последующей отправки в сообщении.

        Args:
            user_id: Идентификатор пользователя
            image_file: Путь к файлу, содержимое файла в байтах или открытый файловый объект

        Returns:
            Информация о загруженном изображении
        """
        logger.debug(f"Асинхронная загрузка изображения для пользователя {user_id}")

        files = {}

        # Если передана строка, считаем её путём к файлу
        if isinstance(image_file, str):
            if not os.path.isfile(image_file):
                raise ValidationError(f"Файл не найден: {image_file}")

            file_name = os.path.basename(image_file)
            with open(image_file, "rb") as f:
                image_content = f.read()
            files = {"uploadfile[]": (file_name, image_content)}

        # Если переданы байты, используем их
        elif isinstance(image_file, bytes):
            files = {"uploadfile[]": ("image.jpg", image_file)}

        # Если передан файловый объект, используем его
        elif hasattr(image_file, "read"):
            file_name = getattr(image_file, "name", "image.jpg")
            image_content = image_file.read()
            files = {"uploadfile[]": (os.path.basename(file_name), image_content)}

        else:
            raise ValidationError(
                "Неверный тип файла. Ожидается путь к файлу, байты или файловый объект"
            )

        response = await self._request_async(
            method="POST",
            url=f"/messenger/v1/accounts/{user_id}/uploadImages",
            files=files,
            multipart=True,
        )

        return response

    async def send_image_message(
        self,
        user_id: int,
        chat_id: str,
        image_id: str,
    ) -> Message:
        """
        Асинхронно отправляет сообщение с изображением в чат.

        Args:
            user_id: Идентификатор пользователя
            chat_id: Идентификатор чата
            image_id: Идентификатор загруженного изображения

        Returns:
            Информация об отправленном сообщении
        """
        logger.debug(f"Асинхронная отправка сообщения с изображением в чат {chat_id} от пользователя {user_id}")

        request = SendImageMessageRequest(image_id=image_id)

        response = await self._request_async(
            method="POST",
            url=f"/messenger/v1/accounts/{user_id}/chats/{chat_id}/messages/image",
            json_data=request.dict(),
        )

        return Message(**response)

    async def mark_chat_as_read(self, user_id: int, chat_id: str) -> SuccessResponse:
        """
        Асинхронно отмечает чат как прочитанный.

        Args:
            user_id: Идентификатор пользователя
            chat_id: Идентификатор чата

        Returns:
            Подтверждение успешного выполнения операции
        """
        logger.debug(f"Асинхронная отметка чата {chat_id} как прочитанного для пользователя {user_id}")

        response = await self._request_async(
            method="POST",
            url=f"/messenger/v1/accounts/{user_id}/chats/{chat_id}/read",
        )

        if not response:
            return SuccessResponse(ok=True)
        else:
            return SuccessResponse(**response)

    async def delete_message(self, user_id: int, chat_id: str, message_id: str) -> dict[str, Any]:
        """
        Асинхронно удаляет сообщение из чата.

        Args:
            user_id: Идентификатор пользователя
            chat_id: Идентификатор чата
            message_id: Идентификатор сообщения

        Returns:
            Подтверждение успешного выполнения операции
        """
        logger.debug(f"Асинхронное удаление сообщения {message_id} из чата {chat_id} пользователя {user_id}")

        response = await self._request_async(
            method="POST",
            url=f"/messenger/v1/accounts/{user_id}/chats/{chat_id}/messages/{message_id}",
        )

        return response

    async def get_voice_files(self, user_id: int, voice_ids: list[str]) -> VoiceFiles:
        """
        Асинхронно получает ссылки на файлы голосовых сообщений.

        Args:
            user_id: Идентификатор пользователя
            voice_ids: Список идентификаторов голосовых сообщений

        Returns:
            Ссылки на файлы голосовых сообщений
        """
        logger.debug(f"Асинхронный запрос файлов голосовых сообщений для пользователя {user_id}")

        params = {"voice_ids": ",".join(voice_ids)}

        response = await self._request_async(
            method="GET",
            url=f"/messenger/v1/accounts/{user_id}/getVoiceFiles",
            params=params,
        )

        return VoiceFiles(**response)

    async def subscribe_webhook(self, url: str) -> SuccessResponse:
        """
        Асинхронно подписывается на webhook-уведомления.

        Args:
            url: URL для получения уведомлений

        Returns:
            Подтверждение успешной подписки
        """
        logger.debug(f"Асинхронная подписка на webhook-уведомления: {url}")

        request = WebhookSubscribeRequest(url=url)

        response = await self._request_async(
            method="POST",
            url="/messenger/v3/webhook",
            json_data=request.dict(),
        )

        return SuccessResponse(**response)

    async def unsubscribe_webhook(self, url: str) -> SuccessResponse:
        """
        Асинхронно отписывается от webhook-уведомлений.

        Args:
            url: URL, на который больше не нужно отправлять уведомления

        Returns:
            Подтверждение успешной отписки
        """
        logger.debug(f"Асинхронная отписка от webhook-уведомлений: {url}")

        request = WebhookSubscribeRequest(url=url)

        response = await self._request_async(
            method="POST",
            url="/messenger/v1/webhook/unsubscribe",
            json_data=request.dict(),
        )

        return SuccessResponse(**response)

    async def get_webhook_subscriptions(self) -> WebhookSubscriptions:
        """
        Асинхронно получает список подписок на webhook-уведомления.

        Returns:
            Список подписок на webhook-уведомления
        """
        logger.debug("Асинхронный запрос списка подписок на webhook-уведомления")

        response = await self._request_async(
            method="POST",
            url="/messenger/v1/subscriptions",
        )

        return WebhookSubscriptions(**response)

    async def add_to_blacklist(self, user_id: int, blacklist_users: list[BlacklistUser]) -> dict[str, Any]:
        """
        Асинхронно добавляет пользователей в черный список.

        Args:
            user_id: Идентификатор пользователя
            blacklist_users: Список пользователей для добавления в черный список

        Returns:
            Подтверждение успешного выполнения операции
        """
        logger.debug(f"Асинхронное добавление пользователей в черный список для пользователя {user_id}")

        request = AddBlacklistRequest(users=blacklist_users)

        response = await self._request_async(
            method="POST",
            url=f"/messenger/v2/accounts/{user_id}/blacklist",
            json_data=request.dict(),
        )

        return response
