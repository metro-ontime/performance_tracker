FROM python:3.6

RUN apt-get update && apt-get install -qq -y \
  build-essential \
  libproj-dev \
  proj-data \
  proj-bin \
  libgeos-dev \
  libgdal-dev \
  python-gdal \
  gdal-bin \
  libpq-dev \
  pdal \
  libpdal-plugin-python \
  libffi-dev \
  tree \
  --no-install-recommends

RUN apt-get update

COPY . ./src/

WORKDIR /src

RUN pip install -r /src/requirements.txt