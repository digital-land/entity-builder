FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive

RUN set -xe; \
    apt-get update; \
    apt-get install -y \
        awscli \
        time \
        gosu \
        make \
        git \
        gdal-bin \
        libspatialite-dev \
        libsqlite3-mod-spatialite \
        make \
        python3-pip \
        curl \
        sqlite3

COPY ./ /src
WORKDIR /src
RUN pip install -r /src/requirements.txt
RUN make init

ENTRYPOINT ["make"]
CMD ["dataset/entity.sqlite3"]
