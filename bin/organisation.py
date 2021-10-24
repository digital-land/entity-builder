#!/usr/bin/env python3

import os
import sys
import csv
import json
import glob
from pathlib import Path
from digital_land.specification import Specification
import geojson
import shapely.wkt


fieldnames = set()
organisations = {}

for row in csv.DictReader(open("var/cache/organisation.csv")):
    organisation = row["organisation"]
    del row["organisation"]

    dataset = organisation.split(":")[0]
    reference = organisation.split(":")[1]

    row["dataset"] = dataset
    row[dataset] = reference
    row["reference"] = reference

    fieldnames = fieldnames.union(set(row.keys()))
    organisations[organisation] = row


w = csv.DictWriter(sys.stdout, fieldnames=fieldnames, extrasaction="ignore")
w.writeheader()

for organisation, row in organisations.items():
    w.writerow(row)
