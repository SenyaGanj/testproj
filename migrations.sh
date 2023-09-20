#!/usr/bin/env bash

set -e
set -o pipefail

pipenv run python manage.py collectstatic --clear --no-input
./wait-for-it.sh psql:5432 -t 60
pipenv run python manage.py migrate
