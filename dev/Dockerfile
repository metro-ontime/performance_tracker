FROM python:3.6

RUN apt-get update && apt-get install -y \
  proj-bin \
  libproj-dev \
  libgeos-dev

ARG NB_USER="usr"
ARG NB_UID="1000"
ARG NB_GID="100"

RUN useradd -m -s /bin/bash -u $NB_UID $NB_USER
USER $NB_USER
COPY . /home/$NB_USER
WORKDIR /home/$NB_USER

RUN bash setup_venv.sh && mkdir /home/$NB_USER/vol

ENTRYPOINT ["bash"]
CMD ["entrypoint.sh"]
