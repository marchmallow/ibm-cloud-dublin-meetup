# Copyright 2019 IBM Corporation All Rights Reserved.
#
# SPDX-License-Identifier: Apache-2.0

FROM python:3.6-alpine3.8
    
ARG SERV
ARG VERSION
ENV SERV_DIR=/opt/$SERV
ENV SERV_EXEC=$SERV
ENV PYTHONUNBUFFERED=1

COPY dist/$SERV-$VERSION.tar.gz $SERV_DIR/$SERV-$VERSION.tar.gz

RUN apk update \
  && apk add --virtual build-deps gcc python3-dev musl-dev \
  && apk add postgresql-dev \
  && pip install psycopg2 \
  && apk del build-deps

RUN pip install --no-cache-dir --upgrade pip \
	&& pip install --no-cache-dir $SERV_DIR/$SERV-$VERSION.tar.gz \
	&& rm -fr $HOME/.cache/pip \
    && apk add bash \
    && apk add --upgrade curl \
    && apk add --upgrade grep \
    && rm -rf /var/cache/apk/*
    

CMD ["/bin/bash", "-c", "${SERV_EXEC}"]
