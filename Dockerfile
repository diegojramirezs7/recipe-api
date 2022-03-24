FROM python:3.7-alpine

LABEL MAINTAINER Diego Ramirez

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt

RUN pip install -r requirements.txt

RUN mkdir app 
WORKDIR /app
COPY ./app /app

# create user that only has permission to run the app
# if we don't do this, docker will run app using root user, 
# if somebody gets access, they can do whatever they want
RUN adduser -D user
USER user



