#!/bin/sh
source .venv/bin/activate
pip install -r ./mysite/requirements.txt 
python  ./mysite/manage.py migrate
python mysite/manage.py runserver $PORT
