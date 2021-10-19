#!/usr/bin/env python3

# create a spatialite database for searching and presenting entities

import os
import sys
import csv
import json
from digital_land.datapackage.sqlite import SqlitePackage


tables = {
    "typology": "specification",
    "dataset": "specification",
    "theme": "specification",
    "field": "specification",
    "entity": "dataset",
    #"geometry": "dataset",
    #"schema-field": "dataset",
}


indexes = {
    #"issue": ["resource", "pipeline", "row-number", "field", "issue-type"],
}


if __name__ == "__main__":
    package = SqlitePackage("entity", tables=tables, indexes=indexes)
    package.create(sys.argv[1])
