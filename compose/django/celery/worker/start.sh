#!/bin/sh

set -o errexit
set -o nounset

python manage.py celery_worker