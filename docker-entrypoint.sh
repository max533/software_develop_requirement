#!/bin/sh

if [ "$1" == "/usr/local/bin/uwsgi" -a "$2" == "--ini" -a "$3" == "/app/uwsgi.ini" ]; then
    ### 1. Collect django static files with production setting
    python manage.py collectstatic --noinput --settings=config.settings.production
    ### 2. Copy staticfiles to the shared volume directory
    cp -r /app/staticfiles /shared
    ### 3. execute uwsgi
    exec "$@"
fi

exec "$@"

