"""
这是一个可异步的 log 创建工具：
1. 可以创建多个 logger，每个 logger 可以有不同的 log level 和 log file
2. 可以创建多个 listener 和 queue，每个 listener 和 queue 可以有不同的 log file
3. 可以创建多个 handler，每个 handler 可以有不同的 log file
4. 可以创建多个 formatter，每个 formatter 可以有不同的 log file
使用方法参考底部测试代码
"""

import logging
import sys
import time
from logging.handlers import QueueHandler, QueueListener, RotatingFileHandler
from pathlib import Path
from queue import Queue
from typing import Any, Dict, Literal, Sequence

import colorlog
from pydantic import BaseModel
from pythonjsonlogger import jsonlogger

_LogLevel = Literal[
    "debug",
    "info",
    "warning",
    "error",
]

LOG_KEYS = [
    "asctime",
    "levelname",
    "name",
    "filename",
    "lineno",
    "process",
    "message",
]

LOG_FORMAT = (
    "%(blue)s%(asctime)sZ%(reset)s | "
    "%(log_color)s%(levelname)s%(reset)s | "
    "%(cyan)s%(name)s:%(filename)s:%(lineno)s%(reset)s | "
    "%(blue)s%(process)d:%(thread)d%(reset)s >> "
    "%(log_color)s%(message)s%(reset)s"
)

DEFAULT_LEVEL: _LogLevel = "info"


class LogSettings(BaseModel):
    name: str | None = None
    level: _LogLevel = DEFAULT_LEVEL
    save_file_or_dir: Path | None = None
    stream_handler: bool = True  # stream print
    rich_handler: bool = False  # rich stream print
    json_logger: bool = False  # save log file as .jsonl


class CustomJsonFormatter(jsonlogger.JsonFormatter):
    def add_fields(
        self,
        log_record: Dict[str, Any],
        record: logging.LogRecord,
        message_dict: Dict[str, Any],
    ) -> None:
        super().add_fields(log_record, record, message_dict)
        unwanted_keys = set(log_record.keys()) - set(LOG_KEYS)
        for k in unwanted_keys:
            del log_record[k]


def _get_stream_handler() -> logging.StreamHandler:
    formatter = colorlog.ColoredFormatter(LOG_FORMAT)
    stream_handler = logging.StreamHandler(sys.stderr)
    stream_handler.setFormatter(formatter)
    return stream_handler


def _get_rich_handler():
    from rich.logging import RichHandler

    return RichHandler(
        rich_tracebacks=True,
        show_time=True,
        omit_repeated_times=True,
        show_level=True,
        show_path=True,
        enable_link_path=True,
    )


def _get_rotating_file_handler(log_settings: LogSettings) -> RotatingFileHandler | None:
    if log_settings.save_file_or_dir is not None:
        log_file = _create_log_file(
            log_settings.save_file_or_dir,
            log_settings.name,
        )
        file_handler = RotatingFileHandler(
            filename=str(log_file),
            maxBytes=1048576,
            backupCount=8,
        )
        if log_settings.json_logger is True:
            file_handler.setFormatter(CustomJsonFormatter(LOG_FORMAT, json_ensure_ascii=False))
        else:
            file_handler.setFormatter(colorlog.ColoredFormatter(LOG_FORMAT))
        return file_handler
    return None


def _configure_logger(log_settings: LogSettings, async_queue: bool) -> QueueListener | None:
    logger = _init_logger(log_settings.name, log_settings.level)

    if async_queue is True:
        # Create a queue for logging
        log_queue = Queue(-1)
        logger.addHandler(QueueHandler(log_queue))

    # Create handlers
    handlers = []
    if log_settings.stream_handler is True:
        handlers.append(_get_stream_handler())
    if log_settings.rich_handler is True:
        handlers.append(_get_rich_handler())
    file_handler = _get_rotating_file_handler(log_settings)
    if file_handler is not None:
        handlers.append(file_handler)

    if async_queue is True:
        queue_listener = QueueListener(log_queue, *handlers)
        queue_listener.start()
        return queue_listener
    else:
        for handler in handlers:
            logger.addHandler(handler)
        return None


def _init_logger(
    name: str | None = None,
    level: _LogLevel = DEFAULT_LEVEL,
) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level.upper()))
    logger.handlers.clear()
    logger.propagate = False
    return logger


def _create_log_file(log_path: Path, name: str | None = None) -> Path:
    """
    if log_path not exist:
        folder named log_path will be created,
        then '{name}.log' will be the file name.
    if log_path exists:
        if is a file, use the file as log file,
        if is a folder, use the '{name}.log' as file name.
    """
    if not log_path.exists():
        log_path.mkdir(exist_ok=True, parents=True)

    if log_path.is_dir():
        if name is None:
            name = ""
        log_path = log_path.joinpath(f"{name}.log")

    return log_path


def setup_loggers(
    log_settings_list: Sequence[LogSettings | None], async_queue: bool = False
) -> dict[str, QueueListener] | None:
    setup_basic_log_config()
    if async_queue is True:
        queue_listeners: dict = {}
        for log_settings in log_settings_list:
            if log_settings is None:
                log_settings = LogSettings()
            if log_settings.name is None:
                queue_listeners['root'] = _configure_logger(log_settings, async_queue)
            else:
                queue_listeners[log_settings.name] = _configure_logger(log_settings, async_queue)
        return queue_listeners
    else:
        for log_settings in log_settings_list:
            if log_settings is None:
                log_settings = LogSettings()
            _configure_logger(log_settings, async_queue)
        return None


def setup_logger(log_settings: LogSettings | None = None, async_queue: bool = False):
    setup_basic_log_config()
    if log_settings is None:
        log_settings = LogSettings()
    return _configure_logger(log_settings, async_queue)


def setup_basic_log_config() -> None:
    logging.basicConfig(datefmt="%Y-%m-%d %H:%M:%S")
    logging.Formatter.converter = time.gmtime


if __name__ == "__main__":
    """
    This is a test for the async log.
    """

    def init_log(async_queue: bool = True):
        logger_names = [None, 'asyncLogTest']

        log_settings_list = [
            LogSettings(
                name=name,
                save_file_or_dir=Path('./data/logs'),
                stream_handler=False,
                rich_handler=False,
                json_logger=True,
                level='debug',
            )
            for name in logger_names
        ]

        log_listeners = setup_loggers(log_settings_list, async_queue=async_queue)

        app_log = logging.getLogger('asyncLogTest')
        return app_log, log_listeners

    def log_messages():
        for i in range(100):
            logger.info(f"Logging message {i}")
            logger.info("***" * 10)
            logger.info("***" * 10)
            logger.info("***" * 10)
            logger.info("***" * 10)
            logger.info("***" * 10)
            logger.info("***" * 10)
            logger.info("***" * 10)
            logger.info("***" * 10)
            logger.info("***" * 10)
            logger.info("***" * 10)
            # Simulate a time-consuming task
            time.sleep(0.01)

    def main():
        start_time = time.time()
        log_messages()
        end_time = time.time()
        print(f"Logging completed in {end_time - start_time:.2f} seconds")

    setup_basic_log_config()
    logger, log_listeners = init_log(async_queue=True)  # change to True or False to test
    main()
    if log_listeners is not None:
        for listener in log_listeners.values():
            listener.stop()
