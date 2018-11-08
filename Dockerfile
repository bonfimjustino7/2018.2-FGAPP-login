FROM python:3.5.6-slim-stretch
ENV PYTHONUNBUFFERED 1

RUN mkdir /code
ADD . /code
WORKDIR /code/login

RUN pip install --upgrade pip
RUN pip install -r requirements/dev.txt

RUN mkdir -p /usr/share/man/man1 && mkdir -p /usr/share/man/man7
RUN apt-get update && apt-get install -f -y postgresql-client
