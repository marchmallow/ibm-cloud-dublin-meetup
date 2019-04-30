# Copyright 2019 IBM Corporation All Rights Reserved.
#
# SPDX-License-Identifier: Apache-2.0

FROM python:3.6-alpine3.8

ARG SERV
ARG VERSION
ENV SERV_DIR=/opt/$SERV
ENV FLASK_APP=/opt/flaskform/__main__.py


RUN pip install --no-cache-dir --upgrade pip \
  && pip install Flask WTForms redis \
	&& rm -fr $HOME/.cache/pip \
    && apk update \
    && apk add bash \
    && apk add --upgrade curl \
    && apk add --upgrade grep \
    && apk add --upgrade coreutils \
    && rm -rf /var/cache/apk/* \
    && mkdir -p /opt/flaskform


ADD flaskform/ /opt/flaskform/

CMD ["flask run"]
