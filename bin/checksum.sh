#!/bin/bash

IFS=' '


echo "path,dataset,line-count,bytes,checksum,entry-date"
for path in var/dataset/*.csv
do
    file=$(basename $path)
    dataset=$(basename $path .csv)
    bytes=$(stat --printf="%s" $path)
    entry_date=$(TZ=UTC stat -c '%y' $path | sed 's/^\([0-9-]*\).\([0-9:]*\).*$/\1T\2Z/')
    rows=$(wc -l $path | cut -d ' ' -f 1)
    md5sum=$(md5sum $path | cut -d ' ' -f 1)
    echo "$file,$dataset,$rows,$bytes,$md5sum,$entry_date"
done
