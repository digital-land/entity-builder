#!/bin/bash

#set -e

s3="https://files.planning.data.gov.uk/"

dir=var/dataset/
mkdir -p $dir

IFS=,
while read dataset collection
do
    if [ -z "$collection" ] ; then
        continue
    fi
    # current s3 structure has collection, but should be flattend
    # https://*-collection-dataset.s3.eu-west-2.amazonaws.com/{COLLECTION}-collection/issue/{DATASET}/{DATASET}.sqlite3
    url=$s3$collection-collection/dataset/$dataset.csv
    path=$dir$dataset.csv

    if [ ! -f $path ] ; then
        set -x
        curl -qsfL -o $path "$url"
        set +x
    fi
    # Download old entity files, which may or may not exist
    oe_url=https://raw.githubusercontent.com/digital-land/${collection}-collection/main/pipeline/old-entity.csv
    oe_path=${dir}${collection}-old-entity.csv

    if [ ! -f $oe_path ] ; then
        set -x
        curl -qsfL -o $oe_path "$oe_url"
        set +x
    fi
done < <(csvcut -c dataset,collection specification/dataset.csv | tail -n +2)
