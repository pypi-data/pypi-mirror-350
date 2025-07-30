import sys
from typing import Literal

from loguru import logger
from pydantic import BaseModel, constr, ConfigDict, field_validator


class LoggingConfig(BaseModel):
    model_config = ConfigDict(strict=True, extra='forbid')
    log_file_name: constr(min_length=1)
    level: Literal[
        'DEBUG', 'INFO', 'TRACE', 'WARNING', 'ERROR'] = "DEBUG"
    console: bool = False

    @field_validator('log_file_name', mode='before')
    def validate_log_file_name(cls, v):
        if not v:
            raise ValueError('log_file_name cannot be None or empty')
        return v


def new_logger(log_file, level, console) -> logger:
    """
    Creates and returns a new Loguru logger with the specified settings.
    """
    # Create a logging configuration instance with the provided parameters
    config = LoggingConfig(log_file_name=log_file, level=level, console=console)
    # Configure and return a local logger using the given configuration
    return _configure_local_logger(config)


def _configure_local_logger(config: LoggingConfig):
    """
    Configures a local Loguru logger with the provided configuration.
    Returns a logger instance configured according to the provided settings.
    """
    local_logger = logger.bind()
    local_logger.remove()
    _setup_logging(local_logger, config)
    return local_logger


def _setup_logging(local_logger, config: LoggingConfig):
    """
    Sets up the Loguru logger according to the specified configuration.
    """
    if config.console:
        _add_console_output(local_logger, config.level)
    _add_file_output(local_logger, config.log_file_name, config.level)


def _add_console_output(local_logger, level: str):
    """
    Adds console output to the Loguru logger.
    """
    local_logger.add(
        sys.stdout,
        format="{time} {level} {message}",
        level=level,
        enqueue=True,
        backtrace=True,
        diagnose=True,
    )


def _add_file_output(local_logger, log_file_name: str, level: str):
    """
    Adds file output to the Loguru logger.
    """
    local_logger.add(
        log_file_name,
        rotation="100MB",
        format="{time} {level} {message}",
        level=level,
        enqueue=True,
        backtrace=True,
        diagnose=True,
        serialize=True,
    )


if __name__ == '__main__':
    try:
        custom_logger = new_logger(log_file="log/app.log", level="DEBUG", console=True)
        custom_logger.info("Logging is configured successfully.")
    except ValueError as e:
        print(f"Configuration error: {e}")
