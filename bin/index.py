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
from shapely.geometry import MultiPolygon
from decimal import Decimal


def properties(row, fields):
    return {
        field: row[field]
        for field in row
        if row[field]
        and field
        not in ["geography", "geometry", "organisation", "point", "slug"] + fields
    }


organisations = {}
for row in csv.DictReader(open("var/cache/organisation.csv")):
    organisations[row["organisation"]] = row

specification = Specification()
entity_fields = specification.schema_field["entity"]
geometry_fields = specification.schema_field["geometry"]
old_entity_fields = specification.schema_field["old-entity"]

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
r = csv.DictWriter(
    open("dataset/old-entity.csv", "w", newline=""),
    fieldnames=old_entity_fields,
    extrasaction="ignore",
)

e.writeheader()
g.writeheader()
r.writeheader()


for path in glob.glob("var/dataset/*.csv"):
    dataset = Path(path).stem
    for row in csv.DictReader(open(path)):
        if row.get("organisation", ""):
            row["organisation-entity"] = organisations[row["organisation"]]["entity"]

        row.setdefault("dataset", dataset)

        if not row.get("reference", ""):
            if row.get("geography", ""):
                row["reference"] = row["geography"].split(":")[1]
            elif row.get(dataset, ""):
                row["reference"] = row[dataset]
                del row[dataset]

        if not row.get("typology", ""):
            row["typology"] = specification.field_typology(row["dataset"])

        if not row.get("json", ""):
            row["json"] = json.dumps(properties(row, entity_fields))
            if row["json"] == {}:
                del row["json"]

        e.writerow(row)

        # write geometry
        shape = row.get("geometry", "")
        point = row.get("point", "")
        wkt = shape or point

        if wkt:
            geometry = shapely.wkt.loads(wkt)
            row["geojson"] = geojson.Feature(geometry=geometry)
            del row["geojson"]["properties"]

            if not row.get("latitude", ""):
                geometry = geometry.centroid
                row["longitude"] = "%.6f" % round(Decimal(geometry.x), 6)
                row["latitude"] = "%.6f" % round(Decimal(geometry.y), 6)

            if not row.get("point", ""):
                row["point"] = "POINT(%s %s)" % (row["longitude"], row["latitude"])

            g.writerow(row)
