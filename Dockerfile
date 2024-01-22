FROM python:3.8.15-slim-buster

WORKDIR /src

COPY . /src
COPY ./docker/entrypoint.sh /entrypoint.sh
COPY ./docker/server.ini /docker_server.ini
# deploy scripts

RUN apt-get update && apt-get install -y --no-install-recommends  build-essential libgdk-pixbuf2.0-0 \
    libpq-dev libsasl2-dev libldap2-dev libssl-dev libmagic1 redis-tools netcat\
    && pip install -U pip --no-cache-dir \
    && rm -rf /var/lib/{apt,dpkg,cache,log}/ \
    && pip install . --no-cache-dir \
    && chmod +x /entrypoint.sh \
    && rm -rf /src

WORKDIR /home/bugcode

RUN mkdir -p /home/bugcode/.bugcode/config
RUN mkdir -p /home/bugcode/.bugcode/logs
RUN mkdir -p /home/bugcode/.bugcode/session
RUN mkdir -p /home/bugcode/.bugcode/storage


ENV PYTHONUNBUFFERED 1
ENV BUGCODE_HOME /home/bugcode
