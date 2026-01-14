#!/usr/bin/python
# -*- coding: utf-8 -*-
import os

URL = "https://egrul.itsoft.ru/{}.json"
HEADERS = {"Accept": "application/json"}
TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), "docx_templates", "template_explanatory_note.docx")

LOGGING_CONFIG = {
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

RESPONSES={
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