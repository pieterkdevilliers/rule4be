#!/bin/sh

# Exit immediately if a command exits with a non-zero status.
set -e

# Run Django collectstatic
# --noinput: Do not prompt the user for input of any kind.
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Then exec the container's main process (what's specified as CMD)
# "$@" is used to pass all arguments passed to the entrypoint script to the exec command
echo "Starting Gunicorn..."
exec "$@"