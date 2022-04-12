#!/bin/bash

#set -e

s3="https://digital-land-production-collection-dataset.s3.eu-west-2.amazonaws.com/"

dir=var/dataset/
mkdir -p $dir

IFS=,
while read dataset collection
do
    # current s3 structure has collection, but should be flattend
    # https://*-collection-dataset.s3.eu-west-2.amazonaws.com/{COLLECTION}-collection/issue/{DATASET}/{DATASET}.sqlite3
    case "$collection" in
    ""|organisation) continue ;;
    esac

    url=$s3$collection-collection/dataset/$dataset.csv
    path=$dir$dataset.csv

    if [ ! -f $path ] ; then
        set -x
        curl -qsfL -o $path "$url"
        set +x
    fi
    # Download old entity files, which may or may not exist
    url=$s3$collection-collection/dataset/$dataset-old-entity.csv
    path=$dir$dataset-old-entity.csv

    if [ ! -f $path ] ; then
        set -x
        curl -qsfL -o $path "$url"
        set +x
    fi
done < <(csvcut -c dataset,collection specification/dataset.csv | tail -n +2)
