FROM python:3.9.13-alpine3.16
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN set -ex \
    && apk add --no-cache --virtual .build-deps \
    git \
    gcc \
    musl-dev \
    linux-headers \
    libffi-dev \
    && apk add --no-cache \
    gettext \
    nodejs \
    npm \
    sudo

COPY ./requirements.txt /requirements.txt
RUN pip install --no-cache-dir -U pip setuptools \ 
    && pip install --no-cache-dir wheel \ 
    && pip install -r /requirements.txt

COPY ./compose/django/entrypoint.sh /entrypoint.sh
RUN sed -i 's/\r$//g' /entrypoint.sh
RUN chmod +x /entrypoint.sh

COPY ./compose/django/start.sh /start.sh
RUN sed -i 's/\r$//g' /start.sh
RUN chmod +x /start.sh

COPY ./compose/django/celery/worker/start.sh /start-celeryworker.sh
RUN sed -i 's/\r$//g' /start-celeryworker.sh
RUN chmod +x /start-celeryworker.sh

COPY ./compose/django/celery/beat/start.sh /start-celerybeat.sh
RUN sed -i 's/\r$//g' /start-celerybeat.sh
RUN chmod +x /start-celerybeat.sh

COPY ./compose/django/celery/flower/start.sh /start-flower.sh
RUN sed -i 's/\r$//g' /start-flower.sh
RUN chmod +x /start-flower.sh

COPY ./e2e/start.sh /start-helper.sh
RUN sed -i 's/\r$//g' /start-helper.sh
RUN chmod +x /start-helper.sh

# Add non root user
ARG USER=default
ENV HOME /app

RUN adduser -D $USER \
    && echo "$USER ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/$USER \
    && chmod 0440 /etc/sudoers.d/$USER

USER $USER

WORKDIR $HOME

RUN sudo chown -R $USER:$USER $HOME

ENTRYPOINT ["sh","/entrypoint.sh"]
