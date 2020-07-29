##### Python Build Imgae #####

FROM python:3.7-slim-buster as builder

ENV PYTHONUNBUFFERED 1

COPY ./utility/instantclient-basic-linux.x64-12.2.0.1.0.zip /opt/instantclient-basic-linux.x64-12.2.0.1.0.zip

RUN echo "deb http://opensource.nchc.org.tw/debian/ buster main" > /etc/apt/sources.list \
  && echo "deb http://opensource.nchc.org.tw/debian/ buster-updates main" >> /etc/apt/sources.list \
  && echo "deb http://opensource.nchc.org.tw/debian/ buster-proposed-updates main" >> /etc/apt/sources.list

RUN apt-get update \
  # dependencies for building Python packages
  && apt-get install --no-install-recommends -y build-essential=12.6 unzip=6.0-23+deb10u1 \
  # Unzip file
  && unzip -d /opt /opt/instantclient-basic-linux.x64-12.2.0.1.0.zip \
  # cleaning up unused files
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*

COPY ./requirements /requirements

RUN pip wheel --wheel-dir=/tmp/wheels -r /requirements/production.txt

#-----------------------------------------------------------------------------

##### Python Production Imgae #####

FROM python:3.7-slim-buster

COPY --from=builder /tmp/wheels /tmp/wheels

COPY --from=builder /requirements /requirements

COPY --from=builder /opt/instantclient_12_2 /opt/instantclient_12_2

COPY ./compose/production/django/uwsgi.ini /etc/uwsgi/uwsgi.ini

RUN echo "deb http://opensource.nchc.org.tw/debian/ buster main" > /etc/apt/sources.list \
  && echo "deb http://opensource.nchc.org.tw/debian/ buster-updates main" >> /etc/apt/sources.list \
  && echo "deb http://opensource.nchc.org.tw/debian/ buster-proposed-updates main" >> /etc/apt/sources.list

RUN apt-get update \
  # Dependencies for connet oralce database
  && apt-get install --no-install-recommends -y libaio1=0.3.112-3 \
  # Make a oracle clinet library soft link file
  && ln -s /opt/instantclient_12_2/libclntsh.so.12.1 /opt/instantclient_12_2/libclntsh.so \
  # Remove unnecessary file
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*

# Install requirement python package with wheel formamt and remove python install package
RUN pip install --no-index --find-links=/tmp/wheels -r /requirements/production.txt \
    && rm -rf /requirements \
    && rm -rf /tmp/wheels

# To avoid execute with root permission, it create django user and group
RUN addgroup django \
    && adduser --gecos "" --ingroup django django

# Make image entripoint shell script with different need
COPY ./compose/production/django/docker-entrypoint.sh /docker-entrypoint.sh
RUN sed -i 's/\r$//g' /docker-entrypoint.sh \
  && chmod +x /docker-entrypoint.sh \
  && chown django /docker-entrypoint.sh

COPY ./compose/production/django/start /start
RUN sed -i 's/\r$//g' /start \
  && chmod +x /start \
  && chown django /start

COPY ./compose/production/django/celery/worker/start /start-celeryworker
RUN sed -i 's/\r$//g' /start-celeryworker \
  && chmod +x /start-celeryworker \
  && chown django /start-celeryworker

COPY ./compose/production/django/celery/beat/start /start-celerybeat
RUN sed -i 's/\r$//g' /start-celerybeat \
  && chmod +x /start-celerybeat \
  && chown django /start-celerybeat

COPY ./compose/production/django/celery/flower/start /start-flower
RUN sed -i 's/\r$//g' /start-flower \
  && chmod +x /start-flower

# Set source code to app home directoty
COPY --chown=django:django . /app

ENV APP_HOME=/app

# Make staticfile volume and log folder and change folder permission
RUN mkdir -p /shared \
  && mkdir -p /log \
  && chown -R django:django /shared \
  && chown -R django:django /log \
  && chown -R django:django /mnt \
  && rm -rf /app/utility/instantclient-basic-linux.x64-12.2.0.1.0.zip

USER django

WORKDIR ${APP_HOME}

ENTRYPOINT ["/docker-entrypoint.sh"]
