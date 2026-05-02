#!/usr/bin/env bash
set -o errexit

python manage.py migrate
python manage.py prepare_demo_data
gunicorn komunikator_project.wsgi:application --bind 0.0.0.0:${PORT:-8000}
