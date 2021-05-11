FROM debian:stable-slim
LABEL maintainer="serverboi@serverboi.org"
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update \
    && apt-get -y --no-install-recommends install apt-utils \
    && apt-get -y dist-upgrade \
    && apt-get -y --no-install-recommends install \
        curl \
        unzip \
        zip \
        python3-minimal \
        python3-pkg-resources \
    && rm -f /bin/sh \
    && ln -s /bin/bash /bin/sh \
    && update-alternatives --install /usr/bin/python python /usr/bin/python3 1 \
    && apt-get clean \
EXPOSE 63725