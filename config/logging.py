import logging
import logging.config
import sys
from typing import Dict


def setup_logging(log_level: str = "INFO", structured: bool = True):
    """Configures application-wide logging."""

    formatter = "json" if structured else "detailed"

    logging_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "json": {
                "format": (
                    "%(asctime)s %(name)s %(levelname)s %(message)s %(pathname)s %(lineno)d "
                    "%(run_id)s %(task_id)s %(event_category)s %(error_code)s"
                ),
                "class": "pythonjsonlogger.jsonlogger.JsonFormatter",
            },
            "detailed": {
                "format": (
                    "%(asctime)s - %(name)s - %(levelname)s - %(message)s "
                    "[%(pathname)s:%(lineno)d] run_id=%(run_id)s task_id=%(task_id)s "
                    "category=%(event_category)s error=%(error_code)s"
                ),
                "datefmt": "%Y-%m-%d %H:%M:%S",
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
        "root": {"level": log_level, "handlers": ["console"]},
    }
    logging.config.dictConfig(logging_config)


def get_logger(name: str) -> logging.Logger:
    """Utility function to get a consistently named logger."""
    return logging.getLogger(name)


def log_event(
    logger: logging.Logger,
    level: int,
    event_category: str,
    message: str,
    run_id: str | None = None,
    task_id: str | None = None,
    error_code: str | None = None,
    **kwargs: Dict[str, str],
) -> None:
    """Emit a structured log with standardized fields.

    Args:
        logger: Logger instance to emit the event.
        level: Logging level (e.g., ``logging.INFO``).
        event_category: High level category describing the event.
        message: Log message.
        run_id: Optional identifier for the overall run.
        task_id: Optional identifier for the specific task.
        error_code: Optional error code describing the failure.
        **kwargs: Additional structured data to include in the log.
    """
    extra = {
        "run_id": run_id,
        "task_id": task_id,
        "event_category": event_category,
        "error_code": error_code,
    }
    extra.update(kwargs)
    logger.log(level, message, extra=extra)
