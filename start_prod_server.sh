#!/bin/bash

# Start Gunicorn server
exec gunicorn server.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 2 \
    --timeout 300 \
    --worker-class gthread \
    --threads 4 \
    --log-level info \
    --access-logfile - \
    --error-logfile -
