##### Build Image #####

FROM python:3.7-alpine as builder

LABEL maintainer Jeff_SH_Wang@wistron.com

RUN apk update && apk add --no-cache \
    gcc~=9.2 \
    musl-dev~=1.1 \
    linux-headers~=4.19 \
    openldap-dev~=2.4 \
    postgresql-dev~=12.2

COPY ./requirements/production.txt /requirements/production.txt

RUN pip wheel --wheel-dir=/tmp/wheels -r /requirements/production.txt

#-----------------------------------------------------------------------------

##### Production Imgae #####

FROM python:3.7-alpine

COPY --from=builder /tmp/wheels /tmp/wheels

COPY --from=builder /requirements/production.txt /requirements/production.txt

RUN pip install --no-index --find-links=/tmp/wheels -r /requirements/production.txt

ENV APP_HOME=/app

RUN mkdir -p $APP_HOME && mkdir -p /shared && mkdir -p /log

RUN addgroup -S app && adduser -S app -G app

COPY uwsgi.ini /etc/uwsgi/uwsgi.ini

COPY . $APP_HOME

WORKDIR $APP_HOME

RUN chown -R app:app $APP_HOME

# if sentry was used, it can be disclaimed
RUN chown -R app:app /log

RUN chown -R app:app /shared

USER app

ENTRYPOINT ["docker-entrypoint.sh"]

EXPOSE 55555

CMD ["/usr/local/bin/uwsgi", "--ini", "/etc/uwsgi/uwsgi.ini"]