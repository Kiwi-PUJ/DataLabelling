FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive 

# Add user
RUN adduser --quiet --disabled-password qtuser && usermod -a -G audio qtuser

# [Option] Install Node.js
#ARG INSTALL_NODE="true"
#ARG NODE_VERSION="lts/*"
#RUN if [ "${INSTALL_NODE}" = "true" ]; then su vscode -c "umask 0002 && . /usr/local/share/nvm/nvm.sh && nvm install ${NODE_VERSION} 2>&1"; fi

# This fix: libGL error: No matching fbConfigs or visuals found
ENV LIBGL_ALWAYS_INDIRECT=1

# Requirements
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y python3-pyqt5 \
    build-essential \
    python3-dev \
    python3-pip

# [Optional] If your pip requirements rarely change, uncomment this section to add them to the image.
COPY requirements.txt /tmp/pip-tmp/
RUN pip3 --disable-pip-version-check --no-cache-dir install -r /tmp/pip-tmp/requirements.txt \
    && rm -rf /tmp/pip-tmp

COPY main.py /tmp/main.py
COPY /media /media
COPY labels.txt /tmp/labels.txt

ENTRYPOINT ["/bin/bash", "-c", "python3 /tmp/main.py"]
