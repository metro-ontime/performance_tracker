FROM python:3.6

RUN apt-get update && apt-get install -y \
  proj-bin \
  libproj-dev \
  libgeos-dev

COPY ./src /app/src
COPY ./data /app/data
COPY ./tests /app/tests
COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r /app/requirements.txt
