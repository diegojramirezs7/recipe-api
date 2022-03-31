FROM python:3.7-alpine

LABEL MAINTAINER Diego Ramirez

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

COPY ./requirements.txt /requirements.txt

# no-cache means don't store registry index on docker container (minimize number of extra files and packages)
RUN apk add --update --no-cache postgresql-client
# virtual sets up an alias that we can use to remove the dependencies later
RUN apk add --update --no-cache --virtual .tmp-build-deps \
    gcc libc-dev linux-headers postgresql-dev

RUN pip install -r requirements.txt

RUN apk del .tmp-build-deps

RUN mkdir app 
WORKDIR /app
COPY ./app /app

# create user that only has permission to run the app
# if we don't do this, docker will run app using root user, 
# if somebody gets access, they can do whatever they want
RUN adduser -D user
USER user
