import logging
import shutil
from logging.handlers import QueueHandler, QueueListener, RotatingFileHandler
import multiprocessing
from typing import Optional

from simple_logger.logger import DuplicateFilter, WrapperLogFormatter

LOGGER = logging.getLogger(__name__)


def setup_logging(log_level: int, log_file: str = "/tmp/pytest-tests.log") -> QueueListener:
    """
    Setup basic/root logging using QueueHandler/QueueListener
    to consolidate log messages into a single stream to be written to multiple outputs.

    Args:
        log_level (int): log level
        log_file (str): logging output file

    Returns:
        QueueListener: Process monitoring the log Queue

    Eg:
       root QueueHandler ┐                         ┌> StreamHandler
                         ├> Queue -> QueueListener ┤
      basic QueueHandler ┘                         └> FileHandler
    """
    basic_log_formatter = logging.Formatter(fmt="%(message)s")
    root_log_formatter = WrapperLogFormatter(
        fmt="%(asctime)s %(name)s %(log_color)s%(levelname)s%(reset)s %(message)s",
        log_colors={
            "DEBUG": "cyan",
            "INFO": "green",
            "WARNING": "yellow",
            "ERROR": "red",
            "CRITICAL": "red,bg_white",
        },
        secondary_log_colors={},
    )

    console_handler = logging.StreamHandler()
    log_file_handler = RotatingFileHandler(filename=log_file, maxBytes=100 * 1024 * 1024, backupCount=20)

    log_queue = multiprocessing.Queue(maxsize=-1)  # type: ignore[var-annotated]
    log_listener = QueueListener(
        log_queue,
        log_file_handler,
        console_handler,
    )

    basic_log_queue_handler = QueueHandler(queue=log_queue)
    basic_log_queue_handler.set_name(name="basic")
    basic_log_queue_handler.setFormatter(fmt=basic_log_formatter)

    basic_logger = logging.getLogger(name="basic")
    basic_logger.setLevel(level=log_level)
    basic_logger.addHandler(hdlr=basic_log_queue_handler)

    root_log_queue_handler = QueueHandler(queue=log_queue)
    root_log_queue_handler.set_name(name="root")
    root_log_queue_handler.setFormatter(fmt=root_log_formatter)

    root_logger = logging.getLogger()
    root_logger.setLevel(level=log_level)
    root_logger.addHandler(hdlr=root_log_queue_handler)
    root_logger.addFilter(filter=DuplicateFilter())

    root_logger.propagate = False
    basic_logger.propagate = False

    log_listener.start()
    return log_listener


def separator(symbol_: str, val: Optional[str] = None) -> str:
    terminal_width = shutil.get_terminal_size(fallback=(120, 40))[0]
    if not val:
        return f"{symbol_ * terminal_width}"

    sepa = int((terminal_width - len(val) - 2) // 2)
    return f"{symbol_ * sepa} {val} {symbol_ * sepa}"
