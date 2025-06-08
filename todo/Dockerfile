FROM python:3.13-alpine

ARG USER_ID=1000
ARG GROUP_ID=1000

RUN apk update && \
    apk add --no-cache --virtual .build-deps \
        g++ \
        python3-dev \
        libffi-dev \
        openssl-dev \
        zlib-dev && \
    apk add --no-cache --update python3
    
RUN pip3 install --upgrade pip setuptools wheel

WORKDIR /srv/

COPY ./requirements.txt .

RUN pip3 install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir alembic

COPY . .

RUN addgroup -g $GROUP_ID usergroup && \
    adduser -D -u $USER_ID -G usergroup docker

RUN chown -R docker:usergroup /srv/ && \
    chmod -R 755 /srv/

USER docker

EXPOSE 3030
EXPOSE 3040
EXPOSE 3050
