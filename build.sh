#!/usr/bin/env bash
pip install -r requirements.txt
echo $PWD
python manage.py collectstatic --no-input
python manage.py migrate