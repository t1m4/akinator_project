#!/bin/bash
set -e

python manage.py migrate
python manage.py create_custom_superuser