import datetime as dt
from dataclasses import is_dataclass

from app.core.cfg import cfg

__author__ = 'kclark'


def test_cfg_attributes():
    # assert test
    assert is_dataclass(cfg)
    assert isinstance(cfg.app_env, str)
    assert isinstance(cfg.app_start_time, dt.datetime)
