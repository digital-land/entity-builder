#!/usr/bin/env python3

# create a spatialite database for searching and presenting entities
# the geometry table could be moved to a separate database including tiles

import os
import sys
import csv
import json
import logging
from digital_land.package.sqlite import SqlitePackage


tables = {
    "checksum": "dataset",
    "entity": "dataset",
    "old-entity": "dataset",
}


indexes = {
    "entity": [
        "entity",
        "typology",
        "prefix",
        "dataset",
        "reference",
        "organisation-entity",
        "json",
        "start-date",
        "entry-date",
        "name",
        "geometry-geom",
        "point-geom",
    ],
    "old-entity": ["entity", "old-entity", "status"],
}


if __name__ == "__main__":
    level = logging.DEBUG
    level = logging.INFO
    logging.basicConfig(level=level, format="%(asctime)s %(levelname)s %(message)s")

    package = SqlitePackage("entity", path=sys.argv[1], tables=tables, indexes=indexes)
    package.spatialite()
    package.create()
