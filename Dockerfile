FROM python:3.7-alpine

LABEL MAINTAINER Diego Ramirez

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

COPY ./requirements.txt /requirements.txt

# no-cache means don't store registry index on docker container (minimize number of extra files and packages)
RUN apk add --update --no-cache postgresql-client jpeg-dev
# virtual sets up an alias that we can use to remove the dependencies later
RUN apk add --update --no-cache --virtual .tmp-build-deps \
    gcc libc-dev linux-headers postgresql-dev musl-dev zlib zlib-dev

RUN pip install -r requirements.txt

RUN apk del .tmp-build-deps

RUN mkdir app 
WORKDIR /app
COPY ./app /app


# store files that may me shared wi containers
# if you had an nginx container that servers static files, you'd map this volume and share with the nginx container
# -p option means create needed subdirs
RUN mkdir -p /vol/web/media
RUN mkdir -p /vol/web/static

# create user that only has permission to run the app
# if we don't do this, docker will run app using root user, 
# if somebody gets access, they can do whatever they want
RUN adduser -D user
# sets the ownership of vol and all its children to the user
RUN chown -R user:user /vol/
RUN chmod -R 755 /vol/web

USER user
