FROM python:3.6

RUN apt-get update && apt-get install -y \
  proj-bin \
  libproj-dev \
  libgeos-dev

COPY ./src /app/src
COPY ./data/GIS /app/data/GIS
COPY ./data/line_info /app/data/line_info
COPY ./tests /app/tests
COPY ./requirements.txt /app/requirements.txt
COPY ./tasks /app/tasks

WORKDIR /app

RUN pip install -r /app/requirements.txt
