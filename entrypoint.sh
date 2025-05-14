#!/bin/sh
# entrypoint.sh

# Exit immediately if a command exits with a non-zero status.
set -e

# # Run Django collectstatic
# echo "Collecting static files..."
# python manage.py collectstatic --noinput # Assuming USE_S3=False is handled in settings.py

# Then exec the container's main process (what's specified as CMD)
echo "Starting Gunicorn..."
exec "$@"
