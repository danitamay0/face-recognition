#!/bin/sh

# My site
echo "cd server"
cd mysite/

echo Ejecuta las migraciones
python manage.py migrate --noinput

echo Recolecta archivos estáticos
python manage.py collectstatic --noinput

echo "running server"

exec gunicorn mysite.wsgi:application --bind 0.0.0.0:8000