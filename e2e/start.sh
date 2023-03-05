#!/bin/bash

set -o errexit
set -o nounset

gunicorn e2e.e2e_django_helper:application -b :8001