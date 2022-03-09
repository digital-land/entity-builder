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


def curie(value):
    if not value:
        return ["", ""]
    s = value.split(":", 2)
    if len(s) == 2:
        return s
    return ["", value]



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
r = csv.DictWriter(
    open("dataset/old-entity.csv", "w", newline=""),
    fieldnames=old_entity_fields,
    extrasaction="ignore",
)

e.writeheader()
r.writeheader()


for path in glob.glob("var/dataset/*.csv"):
    _dataset = Path(path).stem
    row_number = 0
    for row in csv.DictReader(open(path)):

        # handle start_date and start-date columns .. 
        for col in ["start-date", "end-date", "entry-date", "organisation-entity"]:
            row[col] = row.get(col, "") or row.get(col.replace("-", "_"), "")

        # default the dataset
        dataset = row.get("dataset", "") or _dataset
        row_number += 1

        if not row.get("dataset", ""):
            row["dataset"] = dataset

        # the legal entity responsible for managing creating or managing this entity
        if not row.get("organisation-entity", ""):
            if row.get("organisation", ""):
                row["organisation-entity"] = organisations[row["organisation"]]["entity"]

        # default the typeology from the dataset
        typology = row.get("typology", "")
        if not typology:
            typology = specification.field_typology(dataset)
            row["typology"] = typology

        # default the CURIE
        prefix = row.get("prefix", "")
        reference = row.get("reference", "") or row.get(dataset, "") or row.get("site", "")
        key_value = row.get(dataset, "")
        typology_value = row.get(typology, "")

        reference_prefix, reference_reference = curie(reference)
        typology_prefix, typology_reference = curie(typology_value)
        key_prefix, key_reference = curie(key_value)

        row["prefix"] = (
            prefix
            or reference_prefix
            or typology_prefix
            or key_prefix
            or dataset
        )
        row["reference"] = reference_reference or typology_reference or key_reference

        if not row["entity"]:
            print("%s row %d: missing entity, skipping" % (_dataset, row_number))
            continue

        if not row["reference"]:
            print("%s row %d: missing reference" % (_dataset, row_number))

        # migrate wikipedia URLs to a reference compatible with dbpedia CURIEs with a wikipedia-en prefix
        if row.get("wikipedia", ""):
            row["wikipedia"] = row["wikipedia"].replace(
                "https://en.wikipedia.org/wiki/", ""
            )

        # add other fields as JSON properties
        if not row.get("json", ""):
            properties = {
                field: row[field]
                for field in row
                if row[field]
                and field
                not in [
                    "geography",
                    "geometry",
                    "organisation",
                    "organisation-entity",
                    typology,
                    dataset,
                    "point",
                    "slug",
                ]
                + entity_fields
            }
            row["json"] = json.dumps(properties)
            if row["json"] == {}:
                del row["json"]

        # add geometry
        # defaulting point from the shape centroid should probaby be in the pipeline
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

        e.writerow(row)
