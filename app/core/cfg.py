import datetime as dt
import logging
import os
from dataclasses import dataclass

__author__ = 'kclark'

@dataclass()
class Configuration:
    app_env: str
    app_start_time: dt.datetime
    log_level: int


def _initialize_logging():
    root = logging.getLogger()
    root.setLevel(cfg.log_level)

    handler = logging.StreamHandler()
    handler.setLevel(cfg.log_level)
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(filename)s %(funcName)s %(lineno)d %(message)s')
    handler.setFormatter(formatter)
    root.addHandler(handler)


# Create global singleton for configuration settings
cfg = Configuration(
    app_env=os.getenv('APP_ENV', 'dev'),
    app_start_time=dt.datetime.utcnow(),
    log_level=logging.getLevelName(os.getenv('LOG_LEVEL', 'INFO').upper())  # Ignores debug logs
)

_initialize_logging()
