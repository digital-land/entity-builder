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


# organisation responsible for creating, changing or disolving the entity
# TBD: move to organisation-collection
dataset_organisation = {
    "national-park-authority": "government-organisation:D7",
}
organisation_organisation = {
    "development-corporation:Q20648596": "local-authority-eng:GLA",
    "development-corporation:Q6670544": "local-authority-eng:GLA",
}


fieldnames = set()
organisations = {}

for row in csv.DictReader(open("var/cache/organisation.csv")):
    organisation = row["organisation"]

    dataset = organisation.split(":")[0]
    reference = organisation.split(":")[1]

    row["dataset"] = dataset
    row["prefix"] = dataset
    row["reference"] = reference

    row["organisation"] = organisation_organisation.get(
        organisation, dataset_organisation.get(dataset, "")
    )

    fieldnames = fieldnames.union(set(row.keys()))
    organisations[organisation] = row


w = csv.DictWriter(sys.stdout, fieldnames=fieldnames, extrasaction="ignore")
w.writeheader()

for organisation, row in organisations.items():
    w.writerow(row)
