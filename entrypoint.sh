#!/bin/sh

echo "running collecstatic"
poetry run python manage.py collectstatic --noinput
echo "running migrate"
poetry run python manage.py migrate

echo "running server"
poetry run python manage.py runserver 0.0.0.0:8000
