#!/bin/bash
set -e

alembic upgrade head

python -m app.server.main
