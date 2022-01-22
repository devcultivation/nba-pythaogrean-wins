#!/bin/sh

set -e

. /opt/pysetup/.venv/bin/activate

exec python -m pytest -p no:cacheprovider tests/unit