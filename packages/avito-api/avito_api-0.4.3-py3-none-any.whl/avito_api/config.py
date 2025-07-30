"""
Модуль конфигурации для библиотеки avito_api.
"""
import sys
from typing import Optional, Union, Any

from pydantic import BaseModel, Field

# Пытаемся импортировать loguru, но не создаем ошибку,
# если она не установлена - просто показываем сообщение
try:
    from loguru import logger
except ImportError:
    import logging


    # Создаем заглушку для logger, чтобы код работал без loguru
    class Logger:
        def __init__(self):
            self.logger = logging.getLogger("avito_api")
            handler = logging.StreamHandler(sys.stdout)
            handler.setFormatter(logging.Formatter(
                "%(asctime)s.%(msecs)03d | %(levelname)-8s | %(name)s:%(funcName)s:%(lineno)d - %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S"
            ))
            self.logger.addHandler(handler)
            self.logger.setLevel(logging.INFO)

        def configure(self, **kwargs):
            # Игнорируем параметры, которые используются в loguru
            # Просто используем level, если он предоставлен
            if 'level' in kwargs:
                level_name = kwargs.get('level')
                if level_name == 'DEBUG':
                    self.logger.setLevel(logging.DEBUG)
                elif level_name == 'INFO':
                    self.logger.setLevel(logging.INFO)
                elif level_name == 'WARNING':
                    self.logger.setLevel(logging.WARNING)
                elif level_name == 'ERROR':
                    self.logger.setLevel(logging.ERROR)
                elif level_name == 'CRITICAL':
                    self.logger.setLevel(logging.CRITICAL)
            return self

        def bind(self, **kwargs):
            return self

        def debug(self, message, *args, **kwargs):
            self.logger.debug(message)

        def info(self, message, *args, **kwargs):
            self.logger.info(message)

        def warning(self, message, *args, **kwargs):
            self.logger.warning(message)

        def error(self, message, *args, **kwargs):
            self.logger.error(message)

        def exception(self, message, *args, **kwargs):
            self.logger.exception(message)


    logger = Logger()


class LogConfig(BaseModel):
    """Конфигурация логирования."""

    level: str = Field("INFO", description="Уровень логирования")
    format: str = Field(
        "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        description="Формат логов"
    )
    sink: Optional[str] = Field(None, description="Путь к файлу или stdout/stderr")
    rotation: Optional[Union[str, int]] = Field(None, description="Настройки ротации логов (например, '10 MB')")
    retention: Optional[Union[str, int]] = Field(None, description="Настройки хранения логов (например, '1 week')")
    enqueue: bool = Field(False, description="Использовать ли очередь для логирования")
    diagnose: bool = Field(True, description="Включить диагностику исключений")
    serialize: bool = Field(False, description="Сериализовать логи в JSON формат")

    def get_loguru_add_kwargs(self) -> dict[str, Any]:
        """Генерирует параметры для logger.add()"""
        resolved_sink = self.sink or sys.stderr

        kwargs = {
            "sink": resolved_sink,
            "level": self.level,
            "format": self.format,
            "enqueue": self.enqueue,
            "diagnose": self.diagnose,
            "serialize": self.serialize,
        }

        # rotation и retention только если sink — путь к файлу
        if isinstance(resolved_sink, str):
            if self.rotation:
                kwargs["rotation"] = self.rotation
            if self.retention:
                kwargs["retention"] = self.retention

        return kwargs


class ApiConfig(BaseModel):
    """Конфигурация API."""

    base_url: str = Field("https://api.avito.ru", description="Базовый URL API")
    timeout: float = Field(30.0, description="Таймаут запросов в секундах")
    max_retries: int = Field(3, description="Максимальное количество повторных попыток")
    retry_delay: float = Field(1.0, description="Задержка между повторными попытками в секундах")
    user_agent: str = Field("AvitoApiClient/1.0", description="User-Agent для запросов")

    # Настройки авторизации
    auto_refresh_token: bool = Field(True, description="Автоматически обновлять токен при истечении")
    token_refresh_threshold: int = Field(
        300,
        description="Порог в секундах для обновления токена до истечения"
    )


class ClientConfig(BaseModel):
    """Конфигурация клиента API Авито."""

    api: ApiConfig = Field(default_factory=ApiConfig, description="Настройки API")
    logging: LogConfig = Field(default_factory=LogConfig, description="Настройки логирования")

    def setup_logging(self) -> None:
        """Настраивает логирование в соответствии с конфигурацией."""
        try:
            if hasattr(logger, 'remove'):
                logger.remove()
                logger.add(**self.logging.get_loguru_add_kwargs())
            else:
                # Это наша заглушка без loguru
                # Устанавливаем только уровень логирования
                if hasattr(logger, 'logger'):
                    level = getattr(logging, self.logging.level, logging.INFO)
                    logger.logger.setLevel(level)
        except Exception as e:
            print(f"Ошибка при настройке логирования: {str(e)}")

        # Пробуем использовать логгер для отладочного сообщения
        try:
            logger.debug("Логирование настроено")
        except Exception:
            pass


# Настройки по умолчанию
DEFAULT_CONFIG = ClientConfig()
