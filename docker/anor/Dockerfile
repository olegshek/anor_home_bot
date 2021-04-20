FROM python:3.7

RUN set -ex \
    && apt-get update \
    && apt-get install -y --no-install-recommends \
        ca-certificates curl netbase wget \
        git openssh-client \
        libcurl4-openssl-dev libpq-dev libjpeg-dev libpng-dev libsqlite3-dev libxml2-dev libyaml-dev \
        libtool libssl-dev build-essential \
        python3-dev python3-virtualenv python3-cffi python3-pip libcairo2 \
        libpango-1.0-0 libpangocairo-1.0-0 libgdk-pixbuf2.0-0 libffi-dev \
        shared-mime-info \
        gettext

COPY . /app/

RUN pip3 install --upgrade pip && pip3 install -r /app/requirements.txt

WORKDIR /app

EXPOSE 8000

