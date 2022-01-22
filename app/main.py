import datetime as dt
import logging

import requests

from app.core.cfg import cfg

__author__ = 'kclark'

logger = logging.getLogger(__name__)


def run_app():
    logger.info(f'{cfg.app_env}: App Script Start Time {cfg.app_start_time}')

    logger.info(_fetch_github_zen_msg())

    logger.info(f'{cfg.app_env}: App Script Finish Time {dt.datetime.utcnow()}')


def _fetch_github_zen_msg() -> str:
    try:
        resp = requests.get('https://api.github.com/zen')
        result = f'Zen message: {resp.text}'
    except requests.exceptions.HTTPError:
        result = 'Zen message not found (HTTP Error)'
    except requests.RequestException:
        result = 'Zen message not found (Request Error)'
    except Exception:
        result = 'Zen message not found (Unknown Error)'

    return result


if __name__ == '__main__':
    run_app()
