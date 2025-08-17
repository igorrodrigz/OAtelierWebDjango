#!/usr/bin/env bash
# Render build script

set -o errexit  # Exit on error

# Install dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --noinput

# Run database migrations
python manage.py migrate