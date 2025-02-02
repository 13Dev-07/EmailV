#!/bin/bash
# Run post-deployment tasks
echo "Running post-deployment tasks..."

# Clear cache if needed
echo "Clearing cache..."
python manage.py clear_cache

# Run any necessary data migrations
echo "Running data migrations..."
python manage.py migrate_data --noinput

exit 0