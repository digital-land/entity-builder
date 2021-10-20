#!/usr/bin/env python3

# index entity data

import os
import sys
import csv
import json
import glob
from pathlib import Path
from digital_land.specification import Specification
import geojson
import shapely.wkt


organisation = {}
for row in csv.DictReader(open("var/cache/organisation.csv")):
    organisation[row["organisation"]] = row

specification = Specification()
entity_fields = specification.schema_field["entity"]
geometry_fields = specification.schema_field["geometry"]

e = csv.DictWriter(
    open("dataset/entity.csv", "w", newline=""),
    fieldnames=entity_fields,
    extrasaction="ignore",
)
g = csv.DictWriter(
    open("dataset/geometry.csv", "w", newline=""),
    fieldnames=geometry_fields,
    extrasaction="ignore",
)

e.writeheader()
g.writeheader()

for path in glob.glob("var/dataset/*.csv"):
    dataset = Path(path).stem
    for row in csv.DictReader(open(path)):
        if row.get("organisation", ""):
            row["organisation-entity"] = organisation[row["organisation"]]["entity"]

        row.setdefault("dataset", dataset)
        row.setdefault("status", 200)

        if not row.get("reference", ""):
            if row.get("geography", ""):
                row["reference"] = row["geography"].split(":")[1]

        if not row.get("typology", ""):
            row["typology"] = specification.field_typology(row["dataset"])

        if not row.get("json", ""):
            properties = {
                field: row[field]
                for field in row
                if row[field]
                and field
                not in ["geography", "geometry", "organisation", "point", "slug"]
                + entity_fields
            }
            if properties != {}:
                row["json"] = json.dumps(properties)

        if row.get("geometry", ""):
            wkt = shapely.wkt.loads(row["geometry"])
            row["geojson"] = geojson.Feature(geometry=wkt)
            del row["geojson"]["properties"]

        if not row.get("geojson", ""):
            if row.get("point", ""):
                wkt = shapely.wkt.loads(row["point"])
                row["geojson"] = geojson.Feature(geometry=wkt)
                del row["geojson"]["properties"]

        e.writerow(row)
        g.writerow(row)
