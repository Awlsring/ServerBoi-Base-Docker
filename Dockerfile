FROM debian:stable-slim
#
LABEL maintainer="serverboi@serverboi.org"
#
ARG PUID=1000
#
ENV DEBIAN_FRONTEND=noninteractive
ENV USER steam
#
COPY requirements.txt /tmp
COPY bootstrap.py /opt/serverboi/scripts/
COPY ping_server.py /opt/serverboi/scripts/
COPY patch_wf_embed.py /opt/serverboi/scripts/
#
RUN dpkg --add-architecture i386 \
    && apt-get update \
    && apt-get -y --no-install-recommends install apt-utils \
    && apt-get -y dist-upgrade \
    && apt-get -y --no-install-recommends install \
        libc6-dev \
        lib32gcc1 \
        lib32stdc++6 \
        lib32z1 \
        libsdl2-2.0-0 \
        libsdl2-2.0-0:i386 \
        locales \
        curl \
        wget \
        git \
        python3-pip \
        build-essential \
        python3-dev \
        unzip \
        zip \
        libcurl4 \
        ca-certificates \
        python3-minimal \
        python3-pkg-resources \
    && update-alternatives --install /usr/bin/python python /usr/bin/python3 1 \
    && mkdir -p /opt/serverboi/scripts \
    && apt-get clean \
    && useradd -u "${PUID}" -m "${USER}" \
    && su "${USER}" \
    && chmod 755 /tmp/requirements.txt \
    && chmod 755 /opt/serverboi/scripts/* \
    && pip3 install -r /tmp/requirements.txt \
    && pip3 install setuptools \
    && pip3 install git+https://github.com/Awlsring/ServerBoi-Utils.git \
    && rm /tmp/requirements.txt
#
EXPOSE 63725/tcp