FROM python:3.8.6-slim

MAINTAINER Aaron Mamparo

WORKDIR /app
ADD . /app
RUN apt-get update && apt-get install -y --no-install-recommends curl
RUN pip install --upgrade pip
RUN pip install pipenv
RUN pipenv install