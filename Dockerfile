FROM python:3.6

RUN apt-get update && apt-get install -y \
  proj-bin \
  libproj-dev \
  libgeos-dev

COPY ./requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install -r /app/requirements.txt

COPY ./data/GIS /app/data/GIS
COPY ./data/line_info /app/data/line_info
COPY ./tests /app/tests
COPY ./tasks /app/tasks
COPY ./src /app/src
