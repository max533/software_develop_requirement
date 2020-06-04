FROM nginx:1.17.0
LABEL maintainer jeff_sh_wang@wistron.com

RUN mkdir -p /log

COPY ./compose/production/nginx/nginx.conf /etc/nginx/nginx.conf
COPY ./compose/production/nginx/my_nginx.conf.template /etc/nginx/conf.d/my_nginx.conf.template
COPY ./compose/production/nginx/uwsgi_params /etc/nginx/uwsgi_params
COPY --chown=nginx ./compose/production/nginx/start /start

RUN sed -i 's/\r$//g' /start \
  && chmod +x /start \
  && chown nginx /start