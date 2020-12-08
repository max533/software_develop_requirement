#!/usr/bin/env bash

set -o errexit
set -o pipefail
set -o nounset


### 1. Collect django static files
python /app/manage.py collectstatic --noinput

### 2. Copy staticfiles to the shared volume directory
cp -r /app/staticfiles /shared
