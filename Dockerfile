FROM python:3.6

RUN apt-get update && apt-get install -y \
  proj-bin \
  libproj-dev \
  libgeos-dev

COPY ./requirements.txt /src/requirements.txt

WORKDIR /src

RUN pip install cython && \
  pip install numpy && \
  pip install pyproj && \
  pip install cartopy && \
  pip install -r /src/requirements.txt

RUN rm /src/requirements.txt
