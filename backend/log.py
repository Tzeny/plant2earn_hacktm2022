import os
import logging
from logging.handlers import RotatingFileHandler


def create_logging_config(folder, additional_handlers=None, max_log_size_mb=1024, backup_count=5):
    log_path = f'/dataimages/log/{folder}/debug.log'
    try:
        os.makedirs(os.path.dirname(log_path))
    except FileExistsError:
        pass

    aio_logger = logging.getLogger('aiohttp')
    aio_logger.setLevel(logging.DEBUG)
    aio_logger.propagate = False

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)

    debug_handler = RotatingFileHandler(log_path, maxBytes=1024 * 1024 * max_log_size_mb, backupCount=backup_count)
    debug_handler.setLevel(logging.DEBUG)

    handlers = [
        debug_handler,
        stream_handler
    ]
    if additional_handlers is not None:
        handlers += additional_handlers

    formatter = logging.Formatter('%(asctime)s [%(threadName)s] [%(levelname)s] %(message)s')

    for handler in handlers:
        handler.setFormatter(formatter)
        aio_logger.addHandler(handler)

    return aio_logger
