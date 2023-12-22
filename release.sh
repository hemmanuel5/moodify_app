#!/bin/bash

echo "Running release script..."

# Example: Apply database migrations (replace with your actual migration command)
python moodify_app.py migrate

# Example: Install project dependencies
pip install -r requirements.txt

# Example: Collect static files
python moodify_app.py collectstatic --noinput

# Add any other release tasks you need here