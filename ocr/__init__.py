import logging
import sys
from enum import StrEnum
from typing import Any

from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict


class LogLevel(StrEnum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class LoggingSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="LOGGER_",
        env_file=".env",
        env_file_encoding="utf-8",
    )
    log_level: LogLevel = LogLevel.INFO

    def model_post_init(self, context: Any, /) -> None:
        logging.basicConfig(
            level=self.log_level.value,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            handlers=[logging.StreamHandler(sys.stdout)],
        )


LoggingSettings()
