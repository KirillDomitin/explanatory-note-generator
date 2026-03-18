import logging
import os

from pathlib import Path

from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parents[2]
ENV_FILE = BASE_DIR / ".env"
logging.info(ENV_FILE)

class Settings(BaseSettings):

    model_config = SettingsConfigDict(
        env_file=ENV_FILE,
        env_file_encoding="utf-8",
        extra="ignore",
    )

    url: str
    headers: dict[str, str]
    jwt_access_secret: str
    jwt_algorithm: str
    access_cookie_name: str

    redis_host: str
    redis_port: int
    redis_db: int

    auth_postgres_host: str
    auth_postgres_port: int
    auth_postgres_db: str
    auth_postgres_user: str
    auth_postgres_password: str

    template_path: str = os.path.join(os.path.dirname(os.path.dirname(__file__)), "docx_templates", "template_explanatory_note.docx")
    logging_config: dict = {
        'version': 1,
        'disable_existing_loggers': True,
        'formatters': {
            'standard': {
                'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
            },
            'custom_formatter': {
                'format': "%(asctime)s [%(processName)s: %(process)d] [%(threadName)s: %(thread)d] [%(levelname)s] %(name)s: %(message)s"

            },
        },
        'handlers': {
            'default': {
                'formatter': 'standard',
                'class': 'logging.StreamHandler',
                'stream': 'ext://sys.stdout',  # Default is stderr
            },
            'stream_handler': {
                'formatter': 'custom_formatter',
                'class': 'logging.StreamHandler',
                'stream': 'ext://sys.stdout',  # Default is stderr
            },
            'file_handler': {
                'formatter': 'custom_formatter',
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': 'app.log',
                'maxBytes': 1024 * 1024 * 1,  # = 1MB
                'backupCount': 3,
            },
        },
        'loggers': {
            'uvicorn': {
                'handlers': ['default', 'file_handler'],
                'level': 'TRACE',
                'propagate': False
            },
            'uvicorn.access': {
                'handlers': ['stream_handler', 'file_handler'],
                'level': 'TRACE',
                'propagate': False
            },
            'uvicorn.error': {
                'handlers': ['stream_handler', 'file_handler'],
                'level': 'TRACE',
                'propagate': False
            },
            'uvicorn.asgi': {
                'handlers': ['stream_handler', 'file_handler'],
                'level': 'TRACE',
                'propagate': False
            },

        },
    }
    responses: dict = {
        200: {
            "description": "Успешно сгенерированный .docx файл с пояснительной запиской",
            "content": {
                "application/vnd.openxmlformats-officedocument.wordprocessingml.document": {
                    "schema": {"type": "string", "format": "binary"}
                }
            }
        },
        400: {
            "description": "Ошибка в данных или API (например, неверный ИНН, отсутствие блока в ответе, ошибка парсинга)",
            "content": {
                "application/json": {
                    "example": {"detail": "Не удалось получить юридический адрес: отсутствует ключ 'ЭлУлДорСети'"}
                }
            }
        },
        500: {
            "description": "Внутренняя ошибка сервера",
            "content": {
                "application/json": {
                    "example": {"detail": "Внутренняя ошибка: unexpected exception"}
                }
            }
        }
    }

    @property
    def postgres_dsn(self) -> str:
        return (
            f"postgresql+asyncpg://{self.auth_postgres_user}:{self.auth_postgres_password}"
            f"@{self.auth_postgres_host}:{self.auth_postgres_port}/{self.auth_postgres_db}"
        )

    @property
    def redis_dsn(self) -> str:
        auth_part = f":{self.REDIS_PASSWORD}@" if self.REDIS_PASSWORD else ""
        return f"redis://{auth_part}{self.redis_host}:{self.redis_port}/{self.redis_db}"

@lru_cache
def get_settings() -> Settings:
    return Settings()