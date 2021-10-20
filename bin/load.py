#!/usr/bin/env python3

# create a spatialite database for searching and presenting entities

import os
import sys
import csv
import json
import logging
from digital_land.package.sqlite import SqlitePackage


tables = {
    "entity": "dataset",
    "geometry": "dataset",
}


indexes = {
    "entity": ["entity", "typology", "dataset", "reference", "organisation-entity", "json"],
    "geometry": ["entity", "geometry-geom", "point-geom"],
}


if __name__ == "__main__":
    level = logging.DEBUG 
    level = logging.INFO 
    logging.basicConfig(level=level, format="%(asctime)s %(levelname)s %(message)s")

    package = SqlitePackage("entity", tables=tables, indexes=indexes)
    package.spatialite()
    package.create(sys.argv[1])
