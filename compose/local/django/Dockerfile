##### Python Local Imgae #####

FROM python:3.7-slim-buster

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

COPY ./utility/instantclient-basic-linux.x64-12.2.0.1.0.zip /opt/instantclient-basic-linux.x64-12.2.0.1.0.zip

RUN apt-get update \
  # Dependencies for connet oralce database
  && apt-get install --no-install-recommends -y libaio1=0.3.112-3 build-essential=12.6 unzip=6.0-23+deb10u1 \
  # Unzip file
  && unzip -d /opt /opt/instantclient-basic-linux.x64-12.2.0.1.0.zip \
  # Make a oracle clinet library soft link file
  && ln -s /opt/instantclient_12_2/libclntsh.so.12.1 /opt/instantclient_12_2/libclntsh.so \
  # Remove unnecessary file
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*

# Install requirement python package
COPY ./requirements /requirements
RUN pip install -r /requirements/local.txt

# Make image entripoint shell script with different need
COPY ./compose/production/django/docker-entrypoint.sh /docker-entrypoint.sh
RUN sed -i 's/\r$//g' /docker-entrypoint.sh \
  && chmod +x /docker-entrypoint.sh

COPY ./compose/local/django/start /start
RUN sed -i 's/\r$//g' /start \
  && chmod +x /start

COPY ./compose/local/django/celery/worker/start /start-celeryworker
RUN sed -i 's/\r$//g' /start-celeryworker \
  && chmod +x /start-celeryworker

COPY ./compose/local/django/celery/beat/start /start-celerybeat
RUN sed -i 's/\r$//g' /start-celerybeat \
  && chmod +x /start-celerybeat

COPY ./compose/local/django/celery/flower/start /start-flower
RUN sed -i 's/\r$//g' /start-flower \
  && chmod +x /start-flower

WORKDIR /app

ENTRYPOINT ["/docker-entrypoint.sh"]
