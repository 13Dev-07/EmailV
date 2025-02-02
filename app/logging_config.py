"""Logging configuration for the Email Validator Service."""

import logging.config
import os
from typing import Dict

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

LOGGING_CONFIG: Dict = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "json": {
            "class": "pythonjsonlogger.jsonlogger.JsonFormatter",
            "format": "%(asctime)s %(name)s %(levelname)s %(message)s"
        },
        "standard": {
            "format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "standard",
            "level": LOG_LEVEL,
            "stream": "ext://sys.stdout"
        },
        "json_file": {
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "json",
            "filename": "logs/email_validator.json",
            "maxBytes": 10485760,  # 10MB
            "backupCount": 5,
            "level": LOG_LEVEL
        }
    },
    "loggers": {
        "email_validator": {
            "level": LOG_LEVEL,
            "handlers": ["console", "json_file"],
            "propagate": False
        },
        "smtp_validator": {
            "level": LOG_LEVEL,
            "handlers": ["console", "json_file"],
            "propagate": False
        },
        "dns_resolver": {
            "level": LOG_LEVEL,
            "handlers": ["console", "json_file"],
            "propagate": False
        }
    },
    "root": {
        "level": LOG_LEVEL,
        "handlers": ["console"]
    }
}