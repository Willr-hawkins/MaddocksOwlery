#!/usr/bin/env bash
# exit on error
set -o errexit

# Upgrade pip
pip install --upgrade pip

# Install requirements
pip install -r requirements.txt

# Print static files directory contents
echo "Contents of static directory:"
ls -la static/

# Collect static files
python manage.py collectstatic --no-input -v 2

# Print staticfiles directory contents after collection
echo "Contents of staticfiles directory:"
ls -la staticfiles/

# Run migrations
python manage.py migrate