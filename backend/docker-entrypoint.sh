#!/bin/sh
set -e

# Run migrations
alembic upgrade head

# Execute the main command
exec "$@"
