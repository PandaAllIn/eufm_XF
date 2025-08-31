import logging
import logging.config
import sys
from pythonjsonlogger import jsonlogger
from typing import Dict

def setup_logging(log_level: str = "INFO", structured: bool = True):
    """Configures application-wide logging."""
    
    formatter = "json" if structured else "detailed"
    
    logging_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "json": {
                "format": "%(asctime)s %(name)s %(levelname)s %(message)s %(pathname)s %(lineno)d",
                "class": "pythonjsonlogger.jsonlogger.JsonFormatter",
            },
            "detailed": {
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s [%(pathname)s:%(lineno)d]",
                "datefmt": "%Y-%m-%d %H:%M:%S"
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "stream": sys.stdout,
                "formatter": formatter,
                "level": log_level,
            },
        },
        "root": {
            "level": log_level,
            "handlers": ["console"]
        }
    }
    logging.config.dictConfig(logging_config)

def get_logger(name: str) -> logging.Logger:
    """Utility function to get a consistently named logger."""
    return logging.getLogger(name)
