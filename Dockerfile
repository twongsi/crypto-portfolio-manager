FROM python:3.9.1-slim

MAINTAINER Aaron Mamparo

WORKDIR /app
ADD . /app
RUN apt-get update && apt-get install -y --no-install-recommends curl
RUN pip install --upgrade pip
RUN pip install pipenv
RUN pipenv install