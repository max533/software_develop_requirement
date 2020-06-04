#!/usr/bin/env bash

set -o errexit
set -o pipefail
set -o nounset


### 1. Make default database url
if [ -z "${POSTGRES_USER}" ]; then
    base_postgres_image_default_user='postgres'
    export POSTGRES_USER="${base_postgres_image_default_user}"
fi
export DJANGO_DATABASE_DEFAULT_URL="postgres://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:${POSTGRES_PORT}/${POSTGRES_DB}"

### 2. Make hr database url
export DJANGO_DATABASE_HR_URL="oracle://${ORACLE_USER}:${ORACLE_PASSWORD}@${ORACLE_DSN}"

### 3. Setup oracle client library for cx_oracle package to use
export LD_LIBRARY_PATH=/opt/instantclient_12_2

### 4. Wait for internal database ready
postgres_ready() {
python << END
import sys
import psycopg2
try:
    psycopg2.connect(
        dbname="${POSTGRES_DB}",
        user="${POSTGRES_USER}",
        password="${POSTGRES_PASSWORD}",
        host="${POSTGRES_HOST}",
        port="${POSTGRES_PORT}",
    )
except psycopg2.OperationalError:
    sys.exit(-1)
sys.exit(0)
END
}
until postgres_ready; do
  >&2 echo 'Waiting for PostgreSQL to become available...'
  sleep 1
done
>&2 echo 'PostgreSQL is available'

### 5. Wait for external database ready
oracle_ready() {
python << END
import sys
import cx_Oracle
try:
    cx_Oracle.connect(
        dsn="${ORACLE_DSN}",
        user="${ORACLE_USER}",
        password="${ORACLE_PASSWORD}",
    )
except cx_Oracle.OperationalError:
    sys.exit(-1)
sys.exit(0)
END
}
until oracle_ready; do
  >&2 echo 'Waiting for Oracle to become available...'
  sleep 1
done
>&2 echo 'Oracle is available'

exec "$@"
